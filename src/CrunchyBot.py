from selenium import webdriver
import praw
import getpass
import sys
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from praw.errors import InvalidUserPass


def main():
    if (len(sys.argv) != 2):
        print("[ ERROR ] missing parameters")
        print("CrunchyBot.py <data.txt>")
        sys.exit()

    # Make directory for logs and images if necessary.
    if (not os.path.isdir("../logs/")):
        os.makedirs("../logs/")

    # Constants (for automated use).
    CRUNCHY_USER_INDEX = 0
    CRUNCHY_PASS_INDEX = 1
    REDDIT_USER_INDEX = 2
    REDDIT_PASS_INDEX = 3

    # Get data from text file (for automated use).
    print("Fetching Account Data...", end="")
    accountDataFile = open(sys.argv[1], "r")
    accountData = accountDataFile.read().split("\n")
    accountDataFile.close()
    print("Completed")

    # Grab account data (for non-automated use).
#     crunchyUsername = input("CrunchyRoll Username: ")
#     crunchyPassword = getpass.getpass("CrunchyRoll Password: ")
#     redditUsername = input("Reddit Username: ")
#     redditPassword = getpass.getpass("Reddit Password: ")

    # For automated use.
    crunchyUsername = accountData[CRUNCHY_USER_INDEX]
    crunchyPassword = accountData[CRUNCHY_PASS_INDEX]
    redditUsername = accountData[REDDIT_USER_INDEX]
    redditPassword = accountData[REDDIT_PASS_INDEX]

    # Main Script.
    print("Fetching Data...", end="")
    try:
        guestPass = crunchyDataFetch(crunchyUsername, crunchyPassword)
    except (NoSuchElementException):
        print("Error\nUnable to obtain Guest Passes. Please check your CrunchyRoll username and password.")
        sys.exit()

    print("Completed")

    # Ensures that there is something to actually print.
    if (len(guestPass) == 0):
        print("No Valid Guest Passes...Quitting")
        sys.exit()

    print("Building Comment Text...", end="")
    commentText = buildCommentText(guestPass)
    print("Completed")

    print("Posting to Reddit...", end="")
    try:
        submissionStatus = redditPost(
            redditUsername, redditPassword, commentText)

        if (submissionStatus):
            print("Completed")
        else:
            print("Failed")
    except(InvalidUserPass):
        print("Error\nUnable to login to Reddit. Please check your Reddit username and password.")
        driver.close()
        sys.exit()

    print("All Processes Completed.")


def crunchyDataFetch(username, password):
    """
        Fetch Guest Passes from given CrunchyRoll Account.

        Arguments:
            username: String of the CrunchyRoll username to login to
            password: String of the CrunchyRoll password to login to

        Returns a list of Guest Passes as Strings.
    """
    # Constants.
    VALID_KEY_OFFSET = 2
    GUEST_PASS_TABLE_INDEX = 0

    # List to be returned. Will hold all valid guest passes.
    validGuestPass = []
    driver = webdriver.PhantomJS(
        "./phantomjs.exe", service_log_path="../logs/phantom.log")
    driver.get("https://www.crunchyroll.com/login?next=%2F")

    # Login to CrunchyRoll
    driver.find_element_by_id("login_form_name").send_keys(username)
    passwordField = driver.find_element_by_id("login_form_password")
    passwordField.send_keys(password)
    passwordField.send_keys(Keys.ENTER)

    # Navigate to the last page of the Guest Pass page.~
    driver.get("https://www.crunchyroll.com/acct/?action=guestpass")
    driver.find_element_by_link_text("Last").click()

    # Grabs HTML data.
    guestPassTables = driver.find_elements_by_class_name("acct-guestpass-tl")

    # Ensure user was able to login.
    if (not guestPassTables):
        raise(NoSuchElementException)

    rowList = guestPassTables[
        GUEST_PASS_TABLE_INDEX].find_elements_by_tag_name("tr")

    # Parse HTML table data.
    for row in rowList:
        cellList = row.find_elements_by_tag_name("td")
        for k in range(len(cellList)):
            cell = cellList[k]
            if (cell.text == "Valid"):
                validGuestPass.append(cellList[k - VALID_KEY_OFFSET].text)

    # Close the Driver.
    driver.quit()
    return validGuestPass


def redditPost(username, password, commentText):
    """
        Post Guest Passes to Reddit on given user account.

        Arguments:
            username: String of the Reddit Account username to login to
            password: String of the Reddit ACcount password to login to
            commentText: Reddit formatted String to post.

        Returns boolean of completion.
    """
    # Return boolean.
    submissionStatus = False

    # Key words to look for.
    searchList = ["weekly", "guest", "pass", "megathread"]

    # Bot login.
    bot = praw.Reddit("Post CrunchRoll GuestPasses when script is called.")
    bot.login(username, password, disable_warning=True)
    subreddit = bot.get_subreddit("Crunchyroll")

    # Find weekly guest pass submission.
    for submission in subreddit.get_hot(limit=10):
        submissionText = submission.title.lower()
        hasSearch = all(string in submissionText for string in searchList)
        if (hasSearch):
            submission.add_comment(commentText)
            submissionStatus = True
            break

    return submissionStatus


def buildCommentText(guestPass):
    """
        Generates a Reddit formatted text to display the code.

        Arguments:
            guestPass: List of valid guest passes in String form

        Returns a String that has been formatted for Reddit submission.
    """
    text = "Here are some valid passes:  \n\n"
    for gPass in guestPass:
        passCode = " * " + gPass + "\n"
        text += passCode

    text += "  \n*Disclaimer: This is a bot. Here is a [link](https://github.com/lamdaV/CrunchyBot/tree/master) for more detail.*"
    return text


if __name__ == "__main__":
    main()
