import pathlib
from enum import Enum
from typing import Sequence, Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crunchy_bot.config.config_parser import Config
from crunchy_bot.fetcher.fetcher import Fetcher
from crunchy_bot.logging.logger import Logger
from crunchy_bot.logging.noop_logger import NoopLogger


class GuestPassStatus(Enum):
    UNKNOWN = "UNKNOWN"
    VALID = "VALID"
    EXPIRED = "EXPIRED"
    REDEEMED = "REDEEMED"

    @staticmethod
    def to_enum(value: str) -> Enum:
        value = value.upper()
        if value == GuestPassStatus.VALID.value:
            return GuestPassStatus.VALID
        elif value == GuestPassStatus.EXPIRED.value:
            return GuestPassStatus.EXPIRED
        elif value == GuestPassStatus.REDEEMED.value:
            return GuestPassStatus.REDEEMED
        return GuestPassStatus.UNKNOWN


class Row(object):
    """
    Representation of a row of the Guest Pass Table
    """

    def __init__(
        self,
        created_at: str,
        guest_pass: str,
        description: str,
        status: str,
        expiration: str,
        redeemer: str,
        action: str,
    ):
        self.created_at = created_at
        self.guest_pass = guest_pass
        self.description = description
        self.status = GuestPassStatus.to_enum(status)
        self.expiration = expiration
        self.redeemer = redeemer
        self.action = action


class GuestPassFetcher(Fetcher):
    def __init__(self, config: Config, logger: Optional[Logger] = None):
        self.config = config
        self.logger = logger if logger is not None else NoopLogger()

    def fetch(self, debug: bool = False) -> Sequence[str]:
        """
        Fetch CrunchyRoll Guest Passes if any.

        Args:
            debug: Boolean dictating to use ChromeDriver for debugging purposes or not.

        Returns:
            List of Guest Passes.
        """
        self.logger.info("Fetching Guest Passes...")
        guest_passes = self._crunchy_data_fetch(debug=debug)
        self.logger.info("Fetched Guest Passes")

        return guest_passes

    def _crunchy_data_fetch(self, debug=False) -> Sequence[str]:
        """
            Fetch Guest Passes from given CrunchyRoll Account.

            Args:
                debug:      Boolean used to dictate whether to use ChromeDriver or not.
            Returns:
                List of Guest Passes as Strings.
        """
        # Constants.
        GUEST_PASS_TABLE_INDEX = 0
        GUEST_PASS_TABLE_COLUMNS = 7

        # List to be returned. Will hold all valid guest passes.
        valid_guest_passes = []

        log_path = pathlib.Path(self.config.log_dir)
        if not log_path.exists():
            log_path.mkdir(parents=True)
        chrome_options = Options()
        chrome_options.add_argument(
            f"--log-path={log_path.joinpath('chrome.log').as_posix()}"
        )
        if not debug:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.crunchyroll.com/login?next=%2F")

        # Login to CrunchyRoll
        try:
            # Since CloudFlare stalls the login page, this is to wait the estimated
            # 5 seconds (20 seconds to be sure) for CloudFlare to approve of
            # browser.
            username_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "login_form_name"))
            )
            username_field.send_keys(self.config.crunchy_username)

            password_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "login_form_password"))
            )
            password_field.send_keys(self.config.crunchy_password)
            password_field.send_keys(Keys.ENTER)
        except TimeoutException:
            driver.quit()
            raise TimeoutException(
                "Unable to find username/password field: Crunchyroll took too long to load"
            )

        # Navigate to the last page of the Guest Pass page.~
        driver.get("https://www.crunchyroll.com/acct/?action=guestpass")

        # Grabs HTML data.
        guest_pass_tables = driver.find_elements_by_class_name("acct-guestpass-tl")

        # Ensure user was able to login.
        if not guest_pass_tables:
            raise NoSuchElementException

        row_list = guest_pass_tables[GUEST_PASS_TABLE_INDEX].find_elements_by_tag_name(
            "tr"
        )

        # Parse HTML table data.
        for row in row_list:
            cell_list = row.find_elements_by_tag_name("td")
            if len(cell_list) == GUEST_PASS_TABLE_COLUMNS:
                cell_list = list(map(lambda cell: cell.text, cell_list))
                row_entry = Row(*cell_list)
                if row_entry.status is GuestPassStatus.VALID:
                    valid_guest_passes.append(row_entry.guest_pass)
                    break

        # Close the driver.
        driver.close()
        return valid_guest_passes
