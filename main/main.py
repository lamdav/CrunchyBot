from selenium import webdriver
import praw
import getpass

def main():
    # Grab account data.
    crunchyUsername = input("CrunchyRoll Username: ")
    crunchyPassword = getpass.getpass("CrunchyRoll Password: ")
    redditUsername = input("Reddit Username: ")
    redditPassword = getpass.getpass("Reddit Password: ")
    
    # Main.
    guessPass = crunchyDataFetch(crunchyUsername, crunchyPassword)
    commentText = buildCommentText(guessPass)
    redditPost(redditUsername, redditPassword, commentText)
    
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
    
    # List to be returned. Will hold all valid guess passes.
    validGuessPass = []
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
    guessPassTable = driver.find_element_by_class_name("acct-guestpass-tl")
    rowList = guessPassTable.find_elements_by_tag_name("tr")
    
    # Parse HTML data
    for row in rowList:
        cellList = row.find_elements_by_tag_name("td")
        for k in range(len(cellList)):
            cell = cellList[k]
            if (cell.text == "Valid"):
                print("valid key: ", cellList[k - 2].text)
                validGuessPass.append(cellList[k - 2].text)
    
    # Close the Driver.
    driver.quit()
    return validGuessPass

def redditPost(username, password, commentText):
    """
        Post Guess Passes to Reddit on given user account.
        
        Arguments:
            username: String of the Reddit Account username to login to
            password: String of the Reddit ACcount password to login to
            commentText: Reddit formatted String to post.
    """
    # Key words to look for.
    searchList = ["weekly", "guess", "pass", "megathread"]
    
    # Bot login.
    bot = praw.Reddit("Post CrunchRoll GuestPasses at regular intervals")
    bot.login(username, password)
    subreddit = bot.get_subreddit("Crunchyroll")
    
    # Find weekly guess pass submission.
    for submission in subreddit.get_hot(limit = 10):
        submissionText = submission.title.lower()
        hasSearch = any(string in submissionText for string in searchList)
        if (hasSearch):
            submission.add_comment(commentText)
            
def buildCommentText(guessPass):
    """
        Generates a Reddit formatted text to display the code.
        
        Arguments:
            guessPass: List of valid guess passes in String form
    """
    text = "Here are some valid passes:  \n\n"
    for gPass in guessPass:
        passCode  = " * " + gPass + "\n"
        text += passCode
    return text
                
main()
    
    