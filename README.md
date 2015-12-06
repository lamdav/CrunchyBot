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
  * Run $ python main.py  
  * Insert required data.  
  
**Note:** You will not see anything as you type your password. This is an intended effect to hide your data. Key strokes are still being read; however, there will be no visual feedback.  
