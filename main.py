import logging
import threading
import yaml
import subreddit_thread


if __name__ == "__main__":
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info('Acquired reddit instance')

    logging.info('Checking config file for subreddits and associated settings')

    with open('config.yaml', 'r') as config_file:
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as err:
            logging.error(err)

    threads = []

    for config_entry in config:
        subreddit_name = ''
        desired_flair = ''
        reddit_user = ''
        days_in_past = 0
        users = []
        flairs = []
        for key, item in config_entry.items():
            if key == 'users':
                users = item
            elif key == 'flairs':
                flairs = item
            elif key == 'desired_flair':
                desired_flair = item
            elif key == 'reddit_user':
                reddit_user = item
            elif key == 'days_in_past':
                days_in_past = item
            else:
                subreddit_name = key

        logging.info(f'Starting service for {subreddit_name}')

        thread = threading.Thread(target=subreddit_thread.run_subreddit,
                                  args=(subreddit_name, desired_flair, reddit_user, users, flairs))
        threads.append(thread)
        thread.start()

        # If we need to check in the past, lets kick off that thread too
        if days_in_past != 0:
            thread_past = threading.Thread(
               target=subreddit_thread.run_subreddit_in_past,
               args=(subreddit_name, desired_flair, reddit_user, users, flairs, days_in_past))
            threads.append(thread_past)
            thread_past.start()

    # Wait for all of the threads to exit (if ever)
    for t in threads:
        t.join()

    logging.info('All threads have stopped, exiting program')
