import pathlib
from typing import Sequence

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


class GuestPassFetcher(Fetcher):
    def __init__(self, config: Config, logger: Logger = None):
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
        VALID_KEY_OFFSET = 2
        GUEST_PASS_TABLE_INDEX = 0

        # List to be returned. Will hold all valid guest passes.
        valid_guest_pass = []

        # Determine the executable.
        # executable_base = self._get_bin()
        # if sys.platform == "darwin":
        #     executable_path = executable_base.joinpath("osx", "chromedriver")
        # else:
        #     executable_path = executable_base.joinpath("windows", "chromedriver")

        log_path = pathlib.Path(self.config.log_dir)
        if not log_path.exists():
            log_path.mkdir(parents=True)
        chrome_options = Options()
        chrome_options.add_argument("--log-path={}".format(log_path.joinpath("chrome.log").as_posix()))
        if not debug:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.crunchyroll.com/login?next=%2F")

        # Login to CrunchyRoll
        try:
            # Since CloudFlare stalls the login page, this is to wait the estimated
            # 5 seconds (20 seconds to be sure) for CloudFlare to approve of
            # browser.
            username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "login_form_name")))
            username_field.send_keys(self.config.crunchy_username)

            password_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "login_form_password")))
            password_field.send_keys(self.config.crunchy_password)
            password_field.send_keys(Keys.ENTER)
        except TimeoutException:
            driver.quit()
            raise TimeoutException

        # Navigate to the last page of the Guest Pass page.~
        driver.get("https://www.crunchyroll.com/acct/?action=guestpass")

        # Grabs HTML data.
        guest_pass_tables = driver.find_elements_by_class_name("acct-guestpass-tl")

        # Ensure user was able to login.
        if not guest_pass_tables:
            raise NoSuchElementException

        row_list = guest_pass_tables[GUEST_PASS_TABLE_INDEX].find_elements_by_tag_name("tr")

        # Parse HTML table data.
        for row in row_list:
            cell_list = row.find_elements_by_tag_name("td")
            for k in range(len(cell_list)):
                cell = cell_list[k]
                if cell.text == "Valid":
                    valid_guest_pass.append(cell_list[k - VALID_KEY_OFFSET].text)

        # Close the driver.
        driver.close()
        return valid_guest_pass
