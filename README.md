# Useful Scripts for the Looker Admin

I've used [poetry](https://python-poetry.org/) for package management, to create your .venv with the same dependencies, install poetry and type `poetry install` to install the dependencies.

## Delinquent Content and Users

* Finding users who haven't logged in via saml for x days and taking some action on them, *delete_users_90_days.py*
* Finding content that hasn't been accessed for x days *delinquent_content.py* (this also backs up your content assuming [gzr](https://github.com/looker-open-source/gzr) installation and deletes that content)

## UAT Looker Parameter Finder
* Finding content on your instance that has applications of a specific lookml parameter, e.g. all the content with an 'html' parameter applied on your instance. Output is a table that has the content, the id and the element id where the parameter is applied.
* Built as a command line tool with the flags: 
1. ini identify your ini credentials for api access (see looker sdk for details, assumes a github api token
2. repo iterate through a remote repo of lookml or a local folder of your lookml 
3. lookml_param the parameter you're trying to find

## Validate Content
* The idea here is to find all broken content with a content validator call and then send out an email using lookers `send_schedule_once` api endpoint. 

* Caveats with this one are to have your custom message show up create a dummy dimension called `broken_content` and give a sql value of 1, then create a look of that. It will always return true and allow you to put in any custom message you like into the message of the schedule.

## Access System Activity
* Assuming you want to etl data out of the new `system__activity` model, the one way is to use this `sys_activity_table.py` to generate the initial data, then do some kind of incremental load every x days to a stage table, then merge those data with the real table. n.b. it's recommended that you be very careful accessing your backend db as excessive use can cause looker system slowness.