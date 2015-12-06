# CrunchyBot  
# Description:
This is a simple bot I made to publish my CrunchyRoll Guess Passes to Reddit. It uses Selenium and PhantomJS to extract the valid guess passes from CrunchyRoll and PRAW to publish it /r/Crunchyroll's weekly Megathread. This is not a bot made to run indefinitely. It was intended for use in conjunction with a task scheduler to check once every month for new guess passes.
  
# Requirement:
Selenium  
PhantomJS  
PRAW  
Python 3.0+  
  
# How to Use:  
Either run this within an IDE environment and provide the data the console ask for or (as intended) run it via console by:  
  
  * Navigate to where main.py is located in your local repository in the command line.  
  * Run `$ python main.py`  
  * Insert required data.  
  
**Note:** You will not see anything as you type your password. This is an intended effect to hide your data. Key strokes are still being read; however, there will be no visual feedback.  

# Automating:
As previously stated, this was intended for use with Windows Task Scheduler. To set it up, you need to edit the Python files (I chose not to do this for everyone as some may choose to manually do this instead) and have it read from a text file with your account data on it. For example: assuming you have your data in botData.txt located where main.py is
```
  accountDataFile = open("botData.txt", "r")
  accountData = accountDataFile.read().split("\n")
  accountDataFile.close()
  
  # Replace what is there with this. Each index constant is up to how you formatted your text file.
  crunchyUsername = accountData[CRUNCHY_USER_INDEX]
  crunchyPassword = accountData[CRUNCHY_PASS_INDEX]
  redditUsername = accountData[REDDIT_USER_INDEX]
  redditPassword = accountData[REDDIT_PASS_INDEX]
```
  
Example text file:
```
  crunchyUser
  crunchyPass
  redditUser
  redditPass
```
  
Once the Python file is setup, you can follow this helpful guide to setting up your Windows Task Scheduler (http://blogs.esri.com/esri/arcgis/2013/07/30/scheduling-a-scrip/) 
