![my badge](https://action-badges.now.sh/lamdaV/CrunchyBot?workflow=test)
# CrunchyBot
## Description:
This is a simple bot/script I made to publish my CrunchyRoll Guest Passes to Reddit.
It uses Selenium and Chromedriver to extract valid guest passes from CrunchyRoll
and PRAW to publish it /r/Crunchyroll's weekly Megathread. This is not a bot made
to run indefinitely; however, it can be altered to do so if one so desired.
It was intended for use in conjunction with a task scheduler/cronjob to check once every month
(or four if you wish to publish them in sets before guest passes expire) for new guest passes.

## Changes:
Due to how the PRAW library has changed, all users now must create a 
[reddit script app](https://github.com/reddit/reddit/wiki/OAuth2). 
As such, the data file now must include additional data. See below for a quick guide on how to set this up.

As of `4.0.0`, binaries for `chromedriver` and other tooling will not be included. 
Please refer to [link](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver#quick-installation)
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

## Prerequisites:
You will need to have Chrome installed on your system at its default installation path.
This is due to the `chromedriver` working with your Chrome installation to retrieve
Crunchyroll Guest Pass.

**Note** As of `4.0.0`, `chromedriver` will not be provided. 
Please refer to [link](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver#quick-installation)
on setting up.

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

## Development
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
This will use the `Pipfile` and `Pipfile.lock` to fetch and verify dependencies. Run `pipenv shell` to 
execute a shell into the generated virtual environment.

### Without Pipenv
Install PRAW and Selenium by running the following command:
```
$ pip install -r requirements.txt
```

Once setup with or without `pipenv`, run `pip install -e .` within the repository. This
should install a local version of `crunchy_bot` and its cli. This will also generate
a `version.py` using `setuptools_scm`.

Make and test your changes locally. Pull Request are welcome. 


## Automating:
### OSX/Linux
Run `crontab -e` and add
```
0 0 1 * * zsh -lc "/path/to/crunchy publish"
```
You can replace `zsh -lc` with your shell's equivalent. This is mainly to execute any of your profile
presets that may handle setting up `PATH` and other required environment variables to run.

### Windows
Add the Python script to the Windows Task Scheduler with monthly frequency.
Here is a [link](https://blog.netwrix.com/2018/07/03/how-to-automate-powershell-scripts-with-task-scheduler/)
to setup the Task Scheduler.

### Github
You can also fork this repository and utilize `Github Actions` to run this task on the first of each month.
You must add the required data as all cap snake case secret variables.

