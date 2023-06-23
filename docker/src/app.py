import praw
from praw.util.token_manager import FileTokenManager
import os
import logging
import secrets
import string
from random import random,randint
from datetime import datetime
from time import sleep, time

REQUEST_DELAY_IN_SECONDS=5

logger = logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    format='[%(asctime)s|%(levelname)s|%(funcName)s]: %(message)s',
    datefmt='%Y%m%d-%H%M%S'
)

settings = {
    'REDDIT_API_CLIENT_ID': os.getenv('REDDIT_API_CLIENT_ID'),
    'REDDIT_API_CLIENT_SECRET': os.getenv('REDDIT_API_CLIENT_SECRET'),
    'REDDIT_USER': os.getenv('REDDIT_USER'),
    'REDDIT_PASS': os.getenv('REDDIT_PASS'),
    'APP_USER_AGENT': os.getenv('APP_USER_AGENT') or "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/114.0",
    'APP_REPLACE_STRING': os.getenv('APP_REPLACE_STRING') or "#random#",
    'APP_RUN_ONCE': os.getenv('APP_RUN_ONCE') or "no",
    'APP_MIN_SLEEP': os.getenv('APP_MIN_SLEEP') or "300",
    'APP_MAX_SLEEP': os.getenv('APP_MAX_SLEEP') or "3600"
}

# check all settings are configured
for key in settings:
    if ((settings[key] is None) or (not isinstance(settings[key], str)) or (len(settings[key]) == 0)):
        logging.error(f'Missing setting from environment: {key}')
        exit(1)

# sanitize sleep integer
try:
    settings['APP_MIN_SLEEP'] = int(settings['APP_MIN_SLEEP'])
except Exception as e:
    logging.error(f'Failed to parse APP_MIN_SLEEP as an integer')
    raise e
try:
    settings['APP_MAX_SLEEP'] = int(settings['APP_MAX_SLEEP'])
except Exception as e:
    logging.error(f'Failed to parse APP_MAX_SLEEP as an integer')
    raise e

while True:
    # sign in to reddit
    logging.info('Signing in to reddit as user "{user}" using app clientid "{clientid}"'.format(user=settings['REDDIT_USER'], clientid=settings['REDDIT_API_CLIENT_ID']))
    try:
        reddit = praw.Reddit(
            client_id=settings['REDDIT_API_CLIENT_ID'],
            client_secret=settings['REDDIT_API_CLIENT_SECRET'],
            username=settings['REDDIT_USER'],
            password=settings['REDDIT_PASS'],
            user_agent=settings['APP_USER_AGENT']
        )
        redditor = reddit.redditor(settings['REDDIT_USER'])
    except Exception as e:
        logging.error(f'Failed to sign in to reddit: ' + str(e))
    else:

        if settings['APP_REPLACE_STRING'] == '#random#':
            logging.debug('Performing action: Edit (with random string) and delete comments')
            replaceAlphabet = string.ascii_letters + string.digits + '     '
        else:
            logging.debug('Performing action: Edit (with:{string}) and delete comments'.format(string=settings['APP_REPLACE_STRING']))

        # remove deprecation warning
        reddit.validate_on_submit = True

        # edit and delete comments
        comments = 0
        for comment in redditor.comments.new():
            sleep(REQUEST_DELAY_IN_SECONDS)
            comments += 1
            replaceString = settings['APP_REPLACE_STRING']
            if (replaceString == '#random#'):
                replaceString = ''.join(secrets.choice(replaceAlphabet) for i in range(random.randint(32,64)))
                logging.info(f'Nuking comment id:{comment.id} ({replaceString})')
            else:
                logging.info(f'Nuking comment id:{comment.id}')
            try:
                comment.edit(replaceString, )
            except Exception as e:
                logging.warn(f'Failed to edit comment {comment.id}: {str(e)}')
            try:
                comment.delete()        
            except Exception as e:
                logging.warn(f'Failed to delete comment {comment.id}: {str(e)}')

        # edit and delete posts
        logging.debug('Performing action: Delete posts')
        posts = 0
        for post in redditor.submissions.new():
            sleep(REQUEST_DELAY_IN_SECONDS)
            posts += 1
            logging.info(f'Nuking post id:{post.id}')
            try:
                post.delete()        
            except Exception as e:
                logging.warn(f'Failed to delete post {post.id}: {str(e)}')

        logging.info(f'Nuked {comments} comments and {posts} posts.')

    # break out the loop if only running once
    if settings['APP_RUN_ONCE'] == "yes":
        break

    # wait until next iteration
    t = randint(settings['APP_MIN_SLEEP'], settings['APP_MAX_SLEEP'])
    logging.info(f'Next wake at {str(datetime.fromtimestamp(time() + t))} ({t}s)')
    sleep(t)

logging.info('Exiting')