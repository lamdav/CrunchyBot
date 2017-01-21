from selenium import webdriver
import praw
import argparse
import sys
import os
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prawcore.exceptions import OAuthException


def parse_arguments():
    """
        Returns the arguments from the command line.
    """
    parser = argparse.ArgumentParser(description="Executes the CrunchyBot.")
    parser.add_argument("data", help="Path to data txt")
    arguments = parser.parse_args()
    return arguments


def setup_log_directory():
    """
        Setup the selenium webdriver log directory if needed.
    """
    # Make directory for logs if necessary.
    if (not os.path.isdir("../logs/")):
        os.makedirs("../logs/")


def get_data(path):
    """
        Returns the account data from the file at the given path.

        Args:
            path:       String of path to data file.
        Returns:
            Dictionary of account data.
    """
    # Constants (for automated use).
    CRUNCHY_USER_INDEX = 0
    CRUNCHY_PASS_INDEX = 1
    CLIENT_ID_INDEX = 2
    CLIENT_SECRET_INDEX = 3
    USER_AGENT_INDEX = 4
    REDDIT_USER_INDEX = 5
    REDDIT_PASS_INDEX = 6

    # Get data from text file (for automated use).
    print("Fetching Account Data...", end="")
    data_file = open(path, "r")
    account_data = data_file.read().split("\n")
    data_file.close()
    print("Completed")

    # Grab relevant data and store it in the data_dictionary
    data_dictionary = {}
    data_dictionary["crunchy_username"] = account_data[CRUNCHY_USER_INDEX]
    data_dictionary["crunchy_password"] = account_data[CRUNCHY_PASS_INDEX]
    data_dictionary["reddit_client_id"] = account_data[CLIENT_ID_INDEX]
    data_dictionary["reddit_client_secret"] = account_data[CLIENT_SECRET_INDEX]
    data_dictionary["reddit_user_agent"] = account_data[USER_AGENT_INDEX]
    data_dictionary["reddit_username"] = account_data[REDDIT_USER_INDEX]
    data_dictionary["reddit_password"] = account_data[REDDIT_PASS_INDEX]

    return data_dictionary


def crunchy_data_fetch(username, password):
    """
        Fetch Guest Passes from given CrunchyRoll Account.

        Args:
            username:   String of the CrunchyRoll username to login to
            password:   String of the CrunchyRoll password to login to
        Returns:
            List of Guest Passes as Strings.
    """
    # Constants.
    VALID_KEY_OFFSET = 2
    GUEST_PASS_TABLE_INDEX = 0

    # List to be returned. Will hold all valid guest passes.
    valid_guest_pass = []
    driver = webdriver.PhantomJS(
        "./phantomjs.exe", service_log_path="../logs/phantom.log")
    # Uncomment the line below to run with Chromedrive. Be sure to comment the above line if so.
    # driver = webdriver.Chrome("./chromedriver.exe",
    #                           service_log_path="../logs/chrome.log")
    driver.get("https://www.crunchyroll.com/login?next=%2F")

    # Login to CrunchyRoll
    try:
        # Since CloudFlare stalls the login page, this is to wait the estimated
        # 5 seconds (10 seconds to be sure) for CloudFlare to approve of
        # browser.
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_form_name")))
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_form_password")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
    except (TimeoutException):
        driver.quit()
        raise(TimeoutException)

    # Navigate to the last page of the Guest Pass page.~
    driver.get("https://www.crunchyroll.com/acct/?action=guestpass")
    try:
        last = driver.find_element_by_link_text("Last")
        last.click()
    except (NoSuchElementException):
        # This means that user does not have a multipage guest_pass table.
        pass

    # Grabs HTML data.
    guest_pass_tables = driver.find_elements_by_class_name("acct-guestpass-tl")

    # Ensure user was able to login.
    if (not guest_pass_tables):
        raise(NoSuchElementException)

    row_list = guest_pass_tables[
        GUEST_PASS_TABLE_INDEX].find_elements_by_tag_name("tr")

    # Parse HTML table data.
    for row in row_list:
        cell_list = row.find_elements_by_tag_name("td")
        for k in range(len(cell_list)):
            cell = cell_list[k]
            if (cell.text == "Valid"):
                valid_guest_pass.append(cell_list[k - VALID_KEY_OFFSET].text)

    # Close the driver.
    driver.close()

    return valid_guest_pass


def build_comment_text(guest_pass):
    """
        Generates a Reddit formatted text to display the code.

        Args:
            guest_pass:      List of valid guest passes in String form
        Returns:
            String that has been formatted for Reddit submission.
    """
    text = "Here are some valid passes:  \n\n"
    for gPass in guest_pass:
        pass_code = " * " + gPass + "\n"
        text += pass_code

    text += "  \n*Disclaimer: This is a bot. Here is a [link](https://github.com/lamdaV/CrunchyBot/tree/master) for more detail.*"
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
            password:        String of the Reddit ACcount password to login
                             to.
            comment_text:    Reddit formatted String to post.
        Returns:
            Boolean of completion status.
    """
    # Return boolean.
    submission_status = False

    # Key words to look for.
    searchList = ["weekly", "guest", "pass", "megathread"]

    # Bot login.
    bot = praw.Reddit(client_id=client_id, client_secret=client_secret,
                      user_agent=user_agent, username=username, password=password)
    print("Logged in as {0}...".format(bot.user.me()), end="")

    # Navigate to subreddit.
    subreddit = bot.subreddit('Crunchyroll')

    # Find weekly guest pass submission.
    for submission in subreddit.hot(limit=10):
        submissionText = submission.title.lower()
        hasSearch = all(string in submissionText for string in searchList)
        if (hasSearch):
            submission.reply(comment_text)
            submission_status = True
            break

    return submission_status


def main():
    # Parse command line arguments and setup_log_directory logs directory.
    arguments = parse_arguments()
    setup_log_directory()

    # Get data from file.
    data_dictionary = get_data(arguments.data)

    # Fetch CrunchyRoll guest passes.
    print("Fetching Data...", end="")
    try:
        guest_pass = crunchy_data_fetch(
            data_dictionary["crunchy_username"], data_dictionary["crunchy_password"])
    except (NoSuchElementException):
        print("[ ERROR ]: Unable to obtain Guest Passes. Please check your CrunchyRoll username and password.")
        sys.exit(1)
    print("Completed")

    # Ensures that there is something to actually print.
    if (len(guest_pass) == 0):
        print("No Valid Guest Passes...Quitting")
        sys.exit(0)

    # Build the Reddit Markdown comment.
    print("Building Comment Text...", end="")
    comment_text = build_comment_text(guest_pass)
    print("Completed")

    # Post it to reddit.
    print("Posting to Reddit...", end="")
    try:
        submission_status = reddit_post(
            data_dictionary["client_id"], data_dictionary["client_secret"], data_dictionary["reddit_user_agent"], data_dictionary["reddit_username"], data_dictionary["reddit_password"])

        if (submission_status):
            print("Completed")
        else:
            print("Failed")
    except (OAuthException):
        print(
            "[ ERROR ]: Unable to login to Reddit. Please check your Reddit username and password.")
        sys.exit(1)

    print("All Processes Completed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
