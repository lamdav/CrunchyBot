import argparse
import json
import sys
from pathlib import Path

import praw
from prawcore.exceptions import OAuthException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def parse_arguments():
    """
        Returns the arguments from the command line.

        Returns:
            arguments parsed from the command line.
    """
    parser = argparse.ArgumentParser(description="Executes the CrunchyBot.")
    parser.add_argument("data", help="Path to data txt")
    parser.add_argument("--debug", "-d", action="store_true")
    arguments = parser.parse_args()
    return arguments

def get_script_path():
    """
        Retrieve Path of this script.

        Returns:
            Path object to this script
    """
    return Path(__file__).resolve()

def get_log_directory():
    """
        Retrieve log base directory

        Returns:
            Path object to the log directory
    """
    script_path = get_script_path()
    return script_path.parent.parent.joinpath("logs")

def setup_log_directory():
    """
        Setup the selenium webdriver log directory if needed.
    """
    # Make directory for logs if necessary.
    logs_path = get_log_directory()
    if not logs_path.exists():
        logs_path.mkdir(parents=True, exists_ok=True)


def get_data(path):
    """
        Returns the account data from the file at the given path.

        Args:
            path:       String of path to data file.
        Returns:
            Dictionary of account data.
    """
    # Get data from text file (for automated use).
    print("Fetching Account Data...", end="")
    with open(path, "r") as data_file:
        data_dictionary = json.load(data_file)
    print("Completed")
    return data_dictionary


def crunchy_data_fetch(username, password, debug):
    """
        Fetch Guest Passes from given CrunchyRoll Account.

        Args:
            username:   String of the CrunchyRoll username to login to
            password:   String of the CrunchyRoll password to login to
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
    script_path = get_script_path()
    executable_base = script_path.parent.parent.joinpath("bin")
    if sys.platform == "darwin":
        executable_path = executable_base.joinpath("osx", "chromedriver")
    else:
        executable_path = executable_base.joinpath("windows", "chromedriver")

    log_path = get_log_directory()
    chrome_options = Options()
    chrome_options.add_argument("--log-path={}".format(log_path.joinpath("chrome.log").as_posix()))
    if not debug:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=executable_path.as_posix(),
                              options=chrome_options)

    driver.get("https://www.crunchyroll.com/login?next=%2F")

    # Login to CrunchyRoll
    try:
        # Since CloudFlare stalls the login page, this is to wait the estimated
        # 5 seconds (20 seconds to be sure) for CloudFlare to approve of
        # browser.
        username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "login_form_name")))
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "login_form_password")))
        password_field.send_keys(password)
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


def fetch_guest_passes(data_dictionary, debug):
    """
    Fetch CrunchyRoll Guest Passes if any.

    Args:
        data_dictionary: Dictionary of credentials.
        debug: Boolean dictating to use ChromeDriver for debugging purposes or not.

    Returns:
        List of Guest Passes.
    """
    print("Fetching Data...", end="")
    try:
        guest_passes = crunchy_data_fetch(data_dictionary["crunchy_username"],
                                          data_dictionary["crunchy_password"],
                                          debug)
    except NoSuchElementException:
        print("[ ERROR ]: Unable to obtain Guest Passes. Please check your CrunchyRoll credentials")
        sys.exit(1)
    print("Completed")

    # Ensures that there is something to actually print.
    if len(guest_passes) == 0:
        print("No Valid Guest Passes...Quitting")
        sys.exit(0)

    return guest_passes


def build_comment_text(guest_pass):
    """
        Generates a Reddit formatted text to display the code.

        Args:
            guest_pass:      List of valid guest passes in String form
        Returns:
            String that has been formatted for Reddit submission.
    """
    print("Building Comment Text...", end="")

    text = "Here are some valid passes:  \n\n"
    for gPass in guest_pass:
        pass_code = " * " + gPass + "\n"
        text += pass_code

    text += "  \n*Disclaimer: This is a bot. " \
            "Here is a [link](https://github.com/lamdaV/CrunchyBot/tree/master) for more detail.*"

    print("Completed")
    return text


def reddit_post(client_id, client_secret, user_agent, username, password, comment_text):
    """
        Post Guest Passes to Reddit on given user account.

        Args:
            client_id:       String of Reddit Account Script Client ID.
            client_secret:   String of Reddit Account Script Client Secret.
            user_agent:      String of Reddit Account Script User Agent.
            username:        String of the Reddit Account username to login
                             to.
            password:        String of the Reddit Account password to login
                             to.
            comment_text:    Reddit formatted String to post.
        Returns:
            Boolean of completion status.
    """
    # Return boolean.
    submission_status = False

    # Key words to look for.
    search_list = ["weekly", "guest", "pass", "megathread"]

    # Bot login.
    bot = praw.Reddit(client_id=client_id,
                      client_secret=client_secret,
                      user_agent=user_agent,
                      username=username,
                      password=password)
    print("Logged in as {0}...".format(bot.user.me()), end="")

    # Navigate to subreddit.
    subreddit = bot.subreddit('Crunchyroll')

    # Find weekly guest pass submission.
    for submission in subreddit.hot(limit=100):
        submission_text = submission.title.lower()
        has_search = all(string in submission_text for string in search_list)
        if has_search:
            submission.reply(comment_text)
            submission_status = True
            break

    return submission_status


def post_to_reddit(comment_text, data_dictionary):
    print("Posting to Reddit...", end="")
    try:
        submission_status = reddit_post(data_dictionary["reddit_client_id"],
                                        data_dictionary["reddit_client_secret"],
                                        data_dictionary["reddit_user_agent"],
                                        data_dictionary["reddit_username"],
                                        data_dictionary["reddit_password"],
                                        comment_text)

        if submission_status:
            print("Completed")
        else:
            print("Failed")
    except OAuthException:
        print("[ ERROR ]: Unable to login to Reddit. Please check your Reddit credentials")
        sys.exit(1)


def main():
    # Parse command line arguments and setup_log_directory logs directory.
    arguments = parse_arguments()
    setup_log_directory()
    data_dictionary = get_data(arguments.data)
    guest_passes = fetch_guest_passes(data_dictionary, arguments.debug)
    comment_text = build_comment_text(guest_passes)
    post_to_reddit(comment_text, data_dictionary)

    print("All Processes Completed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
