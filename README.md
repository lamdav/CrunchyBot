# CrunchyBot
## Description:
This is a simple bot I made to publish my CrunchyRoll Guest Passes to Reddit. It uses Selenium and PhantomJS to extract the valid guest passes from CrunchyRoll and PRAW to publish it /r/Crunchyroll's weekly Megathread. This is not a bot made to run indefinitely; however, it can be altered to do so if one so desried. It was intended for use in conjunction with a task scheduler to check once every month (or four if you wish to publish them in sets before guest passes expire) for new guest passes.

## Changes:
Due to how the PRAW library has changed, all users now must create a [reddit script app](https://github.com/reddit/reddit/wiki/OAuth2). As such, the data file now must include additional data. See below for a quick guide on how to set this up.

## Setting Up Reddit Account:
  1. Log on to the bot account.
  2. Go the bot account's `preferences` from the upper-right corner.
  3. Click the `apps` tab.
  4. Click the `create another app`.
    - The button test may appear differently if you have no apps setup.
  5. In the prompts, ensure that the `script` radio button is toggled and `redirected uri` is is set to `http://localhost:8080`. The other fields can be filled with whatever you want.
  6. Click `create app` button when done.
  7. You should now see the app created. Right below the name and below `personal use script` will be your `client_id`. Within the box, to the right of the word `secret`, is your `client_secret`.

## Requirement:
* Selenium
* PhantomJS
* PRAW 4.0+
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
