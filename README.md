RedditUserMonitor
=

RedditUserMonitor is a lightweight Reddit bot designed 
to monitor all new comments on specified subreddits, 
looking for specified users and/or specified user flairs.

When a comment is made matching either of these conditions,
a specified flair is added to the post. This allows you to 
monitor and flair posts based on who is commenting on them.

An example of this would be for a gaming subreddit. A special 
developer flair and/or a list of developer Reddit accounts can
be configured, and when a developer comments on a post, you can
flair the post as something like 'Dev Response'. This allows 
users to see posts that a developer has responded to in an easy and
obvious way.

Usage
-

When downloading and running this bot, there are two files
that you will need to configure before starting the application. 

1. praw.ini
    * This file is used to configure the Reddit credentials and application
    keys that will be used to run the tool.
    * You can define more than one account to use, and could, for example, 
    set up a separate entry for each subreddit that required monitoring.
    
    This file will need to be added with the following format:

    ```ini
    [my_reddit_user]
    client_id=CLIENT ID HERE
    client_secret=CLIENT SECRET HERE
    password=REDDIT ACCOUNT PASSWORD HERE
    username=REDDIT ACCOUNT USERNAME HERE
    ```

    If you need help obtaining the client id and client secret, 
    follow the [Reddit guide.](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps)

2. config.yaml
    * This file is used to configure the 
    subreddits and specific subreddit settings
    that this tool will use to monitor.
    * You can define as many subreddits as you'd like.
    
    This file will need to be added with the following format:
    
    ```yaml
    - SomeSubreddit:
     users:
       - SomeUserAccount
     flairs:
       - special user
     desired_flair: special user response
     reddit_user: my_reddit_user 
     days_in_past: 1 
    ```
   
   * SomeSubreddit: The name of the subreddit to monitor.
   * users: A list of Reddit user names to monitor for.
   * flairs: A list of subreddit user flairs to monitor for.
   * desired_flair: The flair to set on the post when a user/flair is matched.
   * reddit_user: The name of the profile set up in the praw.ini to use 
   to monitor and make changes to this subreddit.
   * days_in_past: Timeline to check posts in the past when service is run. [Optional]
   
   You can define users, flairs, or both, but you will need at least 
   one of these for the service to function.
   
Help
-

For any bugs/feature improvements, please use the issue system on this repository.

For help using the tool, feel free to contact myself on danny.wilson.development@gmail.com