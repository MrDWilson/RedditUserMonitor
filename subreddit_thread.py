import logging
import time
import praw
from psaw import PushshiftAPI


def get_flair_id(comment, desired_flair, subreddit_name):
    # We want the actual ID of the flair, not just the text, so lets get it
    flair_id = ''

    for flair_option in comment.submission.flair.choices():
        if flair_option['flair_text'] == desired_flair:
            flair_id = flair_option['flair_template_id']
            break

    if flair_id == '':
        logging.fatal(f'Defined desired flair could not be found on subreddit {subreddit_name}')
        return None
    else:
        return flair_id


def check_comment(comment, desired_flair, subreddit_name, users, flairs, flair_id, reddit):
    # Process an individual comment to check against flair and user list

    if comment.submission.link_flair_text == desired_flair:
        # We have already flagged this post, just ignore this comment
        return

    if comment.author.name in users:
        # The user is in our approved list, lets flair this post
        logging.info(f'Flairing post {comment.submission.id} '
                     f'because of a comment from {comment.author.name}')
        comment.submission.flair.select(flair_id)
        return

    for user_flair in reddit.subreddit(subreddit_name).flair(comment.author):
        if user_flair['flair_text'] in flairs:
            # The user has an approved flair, lets flair this post
            logging.info(f'Flairing post {comment.submission.id} '
                         f'because of a comment from {comment.author.name}')
            comment.submission.flair.select(flair_id)
            break

    return


def run_subreddit(subreddit_name, desired_flair, reddit_user, users, flairs):
    # Let's process all new comments to this subreddit, as we need to check against
    # our user and flair list

    flair_id = ''

    if len(users) == 0 and len(flairs) == 0:
        logging.fatal(f'No users or flairs defined for subreddit {subreddit_name}')
        return

    reddit = praw.Reddit(reddit_user, user_agent="script:redditusermonitor.wlsn.xyz:v1.0 (by u/MrDWilson)")

    while True:
        try:
            for comment in reddit.subreddit(subreddit_name).stream.comments(skip_existing=True):
                # Swap out our flare name for its ID
                if flair_id == '':
                    flair_id = get_flair_id(comment, desired_flair, subreddit_name)
                    if flair_id is None:
                        return

                check_comment(comment, desired_flair, subreddit_name, users, flairs, flair_id, reddit)

            time.sleep(10)

        except Exception as err:
            logging.error(subreddit_name + ': ' + str(err))
            time.sleep(10)


def run_subreddit_in_past(subreddit_name, desired_flair, reddit_user, users, flairs, days_in_past):
    # Check all posts and comments for a certain amount of days in the past
    flair_id = ''

    if len(users) == 0 and len(flairs) == 0:
        logging.fatal(f'No users or flairs defined for subreddit {subreddit_name}')
        return

    reddit = praw.Reddit(reddit_user, user_agent="script:redditusermonitor.wlsn.xyz:v1.0 (by u/MrDWilson)")

    try:
        current_timestamp = time.time()
        # 60 seconds * 60 minutes * 24 hours * x days
        in_past_timestamp = int(current_timestamp - (60 * 60 * 24 * days_in_past))
        api = PushshiftAPI(reddit)
        for post in list(api.search_submissions(after=in_past_timestamp,
                                                subreddit=subreddit_name)):

            if post.link_flair_text == desired_flair:
                # We have already flagged this post, just ignore it
                continue

            post.load_more_comments(limit=None, threshold=1)

            for comment in praw.helpers.flatten_tree(post.comments):
                # Swap out our flare name for its ID
                if flair_id == '':
                    flair_id = get_flair_id(comment, desired_flair, subreddit_name)
                    if flair_id is None:
                        return

                check_comment(comment, desired_flair, subreddit_name, users, flairs, flair_id, reddit)

    except Exception as err:
        logging.error(subreddit_name + ' failed past check: ' + str(err))
