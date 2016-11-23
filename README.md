# CrunchyBot
# Description:
This is a simple bot I made to publish my CrunchyRoll Guest Passes to Reddit. It uses Selenium and PhantomJS to extract the valid guest passes from CrunchyRoll and PRAW to publish it /r/Crunchyroll's weekly Megathread. This is not a bot made to run indefinitely; however, it can be altered to do so if one so desried. It was intended for use in conjunction with a task scheduler to check once every month (or four if you wish to publish them in sets before guest passes expire) for new guest passes.

# Requirement:
Selenium
PhantomJS (Could be changed to a browser of your preference. This project uses PhantomJS for headless data collection)
PRAW
Python 3.0+

Install PRAW and Selenium by running the following command:
```
 $ pip install -r requirements.txt
```

# How to Use:
Either run this within an IDE environment and provide the data the console ask for or (as intended) run it via console by:

  * Navigate to where main.py is located in your local repository in the command line.
  * Run `$ python main.py`
  * Insert required data.

**Note:** You will not see anything as you type your password. This is an intended effect to hide your data. Key strokes are still being read; however, there will be no visual feedback.

# Automating:
As previously stated, this was intended for use with Windows Task Scheduler. To set it up, you need to edit the Python files (the sample code below is in the comments) and have it read from a text file with your account data on it. For example: assuming you have your data in `botData.txt` located where `main.py` is and locate the following commented code:
```python
  accountDataFile = open("botData.txt", "r")
  accountData = accountDataFile.read().split("\n")
  accountDataFile.close()

  # Each index constant is up to how you formatted your text file.
  crunchyUsername = accountData[CRUNCHY_USER_INDEX]
  crunchyPassword = accountData[CRUNCHY_PASS_INDEX]
  redditUsername = accountData[REDDIT_USER_INDEX]
  redditPassword = accountData[REDDIT_PASS_INDEX]
```

Example `botData.txt` file:
```
  crunchyUser
  crunchyPass
  redditUser
  redditPass
```

Once the Python file is setup, you can follow this helpful guide to set up your Windows Task Scheduler [link](http://blogs.esri.com/esri/arcgis/2013/07/30/scheduling-a-scrip/)
