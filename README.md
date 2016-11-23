# CrunchyBot
## Description:
This is a simple bot I made to publish my CrunchyRoll Guest Passes to Reddit. It uses Selenium and PhantomJS to extract the valid guest passes from CrunchyRoll and PRAW to publish it /r/Crunchyroll's weekly Megathread. This is not a bot made to run indefinitely; however, it can be altered to do so if one so desried. It was intended for use in conjunction with a task scheduler to check once every month (or four if you wish to publish them in sets before guest passes expire) for new guest passes.

## Requirement:
* Selenium
* PhantomJS (Could be changed to a browser of your preference. This project uses PhantomJS for headless data collection)
* PRAW
* Python 3.0+

Install PRAW and Selenium by running the following command:
```
 $ pip install -r requirements.txt
```

## How to Use:
  1. Navigate to where CrunchyBot.py is located in your local repository in the command line.
    * **Note:** Execute the script in the `src` directory. Otherwise, the script will complain about not finding `phantomjs.exe` file.
  2. Run `$ python CrunchyBot.py /path/to/botData.txt`

## Automating:
Add the Python script to the Windows Task Scheduler with monthly frequency.
Here is a [link](http://blogs.esri.com/esri/arcgis/2013/07/30/scheduling-a-scrip/) to setup the Task Scheduler.
