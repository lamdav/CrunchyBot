# CrunchyBot
## Description:
This is a simple bot/script I made to publish my CrunchyRoll Guest Passes to Reddit.
It uses Selenium and Chromedriver to extract the valid guest passes from CrunchyRoll
and PRAW to publish it /r/Crunchyroll's weekly Megathread. This is not a bot made
to run indefinitely; however, it can be altered to do so if one so desired.
It was intended for use in conjunction with a task scheduler/cronjob to check once every month
(or four if you wish to publish them in sets before guest passes expire) for new guest passes.

## Changes:
Due to how the PRAW library has changed, all users now must create a 
[reddit script app](https://github.com/reddit/reddit/wiki/OAuth2). 
As such, the data file now must include additional data. See below for a quick guide on how to set this up.

As of `4.0.0`, binaries for `chromedriver` and other tooling will not be included. Please refer to [link](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver#quick-installation)
on setting up and installing `chromedriver`.

## Setting Up Reddit Account:
  1. Log on to the bot account.
  2. Go the bot account's `preferences` from the upper-right corner.
  3. Click the `apps` tab.
  4. Click the `create another app`.
    - The button test may appear differently if you have no apps setup.
  5. In the prompts, ensure that the `script` radio button is toggled and 
     `redirected uri` is is set to `http://localhost:8080`. The other fields
     can be filled with whatever you want.
  6. Click `create app` button when done.
  7. You should now see the app created. Right below the name and below `personal use script` will be your
     `client_id`. Within the box, to the right of the word `secret`, is your `client_secret`.

## Install:
`pip install crunchy-bot`

## Setup:
Run `crunchy init` to generate config file:
```json
{
  "crunchy_username": "crunchy_user",
  "crunchy_password": "crunchy_pass",
  "reddit_client_id": "client_id",
  "reddit_client_secret": "client_secret",
  "reddit_user_agent": "CrunchyBot:v4.0.0 (hosted by /u/{YOUR_USERNAME})",
  "reddit_username": "reddit_user",
  "reddit_password": "reddit_pass",
  "log_dir": "/tmp/crunchybot/logs"
}
```
or save this to `~/.crunchybot`.

Execute `crunchy publish [--config path/to/.crunchybot] [--debug/-d]` to start scrapping and publishing.

## Requirement:
* Selenium
* Chrome
* PRAW 6.1.0+
* Python 3.5+

### Prerequisites:
You will need to have Chrome installed on your system at its default installation path.
This is due to the `chromedriver` working with your Chrome installation to retrieve
Crunchyroll Guest Pass.

**Note** As of `4.0.0`, `chromedriver` will not be provided. Please refer to [link](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver#quick-installation)
on setting up.

~~If you would rather use bring in `chromedriver` yourself, the version of `chromedriver` 
that has been verified to work is `2.45`. Replace the `chromedriver` under the `bin/`
directory.~~

### With Pipenv
Assuming you have `pipenv` installed on your system, run the following within the repo:
```
$ pipenv --three
```
This will setup a virtual environment for Crunchybot to work in without interferring your
other python projects.

With `pipenv` initialized, run:
```
$ pipenv install
```
This will use the `Pipfile` and `Pipfile.lock` to fetch and verify dependencies.

### Without Pipenv
Install PRAW and Selenium by running the following command:
```
 $ pip install -r requirements.txt
```


The other requirements are included in the `bin` directory of the project.

## How to Use:
  1. Clone the project
     ```
        git clone https://github.com/lamdaV/CrunchyBot.git
     ```
  2. Navigate to where you clone the repository
     ```
         cd CrunchyBot
     ```
  3. Update the templated `botData.json` with your information.
  4. Run 
     ```
         pipenv run python src/CrunchyBot.py [--debug/-d] /path/to/botData.json
         // or
         python src/CrunchyBot.py [--debug/-d] /path/to/botData.json
      ```

## Automating:
Add the Python script to the Windows Task Scheduler with monthly frequency.
Here is a [link](http://blogs.esri.com/esri/arcgis/2013/07/30/scheduling-a-scrip/) to setup the Task Scheduler.
