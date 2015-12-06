from selenium import webdriver
import praw
import getpass

def main():
    # Constants (for automated use).
#     CRUNCHY_USER_INDEX = 0
#     CRUNCHY_PASS_INDEX = 1
#     REDDIT_USER_INDEX = 2
#     REDDIT_PASS_INDEX = 3
    
    # Get data from text file (for automated use).
#     print("Fetching Account Data...", end = "")
#     accountDataFile = open("botData.txt", "r")
#     accountData = accountDataFile.read().split("\n")
#     accountDataFile.close()
#     print("Completed")
    
    # Grab account data.
    crunchyUsername = input("CrunchyRoll Username: ")
    crunchyPassword = getpass.getpass("CrunchyRoll Password: ")
    redditUsername = input("Reddit Username: ")
    redditPassword = getpass.getpass("Reddit Password: ")
    
    # For automated use.
#     crunchyUsername = accountData[CRUNCHY_USER_INDEX]
#     crunchyPassword = accountData[CRUNCHY_PASS_INDEX]
#     redditUsername = accountData[REDDIT_USER_INDEX]
#     redditPassword = accountData[REDDIT_PASS_INDEX]
    
    # Main Script.
    print("Fetching Data...", end = "")
    guestPass = crunchyDataFetch(crunchyUsername, crunchyPassword)
    print("Completed")
    
    # Ensures that there is something to actually print.
    if (len(guestPass) == 0):
        print("No Valid Guess Passes...Quitting")
        return
    
    print("Building Comment Text...", end = "")
    commentText = buildCommentText(guestPass)
    print("Completed")
    
    print("Posting to Reddit...", end = "")
    redditPost(redditUsername, redditPassword, commentText)
    print("Completed")
    
    print("All Processes Completed.")
    
def crunchyDataFetch(username, password):
    """
        Fetch Guess Passes from given CrunchyRoll Account.
        
        Arguments:
            username: String of the CrunchyRoll username to login to
            password: String of the CrunchyRoll password to login to
    """
    # Constants.
    PASSWORD_INPUT_INDEX = 1
    SUBMIT_INDEX = 1
    VALID_KEY_OFFSET = 2
    
    # List to be returned. Will hold all valid guess passes.
    validGuestPass = []
    driver = webdriver.PhantomJS()
    driver.get("https://www.crunchyroll.com/login?next=%2F")
    
    # Login to CrunchyRoll
    driver.find_element_by_name("name").send_keys(username) 
    passwordInputBoxes = driver.find_elements_by_name("password")
    passwordInputBoxes[PASSWORD_INPUT_INDEX].send_keys(password) 
    submitButtons = driver.find_elements_by_class_name("submit")
    submitButtons[SUBMIT_INDEX].click()
    
    # Navigate to Guess Pass page.
    driver.get("https://www.crunchyroll.com/acct/?action=guestpass")
    
    # Grabs HTML data.
    guestPassTable = driver.find_element_by_class_name("acct-guestpass-tl")
    rowList = guestPassTable.find_elements_by_tag_name("tr")
    
    # Parse HTML data
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
    """
    # Key words to look for.
    searchList = ["weekly", "guess", "pass", "megathread"]
    
    # Bot login.
    bot = praw.Reddit("Post CrunchRoll GuestPasses when script is called.")
    bot.login(username, password, disable_warning = True)
    subreddit = bot.get_subreddit("Crunchyroll")
    
    # Find weekly guest pass submission.
    for submission in subreddit.get_hot(limit = 10):
        submissionText = submission.title.lower()
        hasSearch = all(string in submissionText for string in searchList)
        if (hasSearch):
            submission.add_comment(commentText)
            
def buildCommentText(guestPass):
    """
        Generates a Reddit formatted text to display the code.
        
        Arguments:
            guestPass: List of valid guest passes in String form
    """
    text = "Here are some valid passes:  \n\n"
    for gPass in guestPass:
        passCode  = " * " + gPass + "\n"
        text += passCode
        
    text += "  \n*Disclaimer: This is a bot. Here is a [link](https://github.com/lamdaV/CrunchyBot/tree/master) for more detail.*"
    return text

if __name__ == "__main__":
    main()