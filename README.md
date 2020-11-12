# Useful Scripts for the Looker Admin

## Delinquent Content and Users

* Finding users who haven't logged in via saml for x days and taking some action on them, *delete_users_90_days.py*
* Finding content that hasn't been accessed for x days *delinquent_content.py* (this also backs up your content assuming [gzr](https://github.com/looker-open-source/gzr) installation and deletes that content)

## UAT Looker Parameter Finder
* Finding content on your instance that has applications of a specific lookml parameter, e.g. all the content with an 'html' parameter applied on your instance. Output is a table that has the content, the id and the element id where the parameter is applied.
* Built as a command line tool with the flags: 
1. -ini identify your ini credentials for api access (see looker sdk for details, assumes a github api token
2. -repo iterate through a remote repo of lookml or a local folder of your lookml 
3. -lookml_param the parameter you're trying to find
