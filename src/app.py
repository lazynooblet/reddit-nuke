import praw
from praw.util.token_manager import FileTokenManager
import os
import logging
import secrets
import string
from time import sleep

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
    'APP_REPLACE_STRING': os.getenv('APP_REPLACE_STRING') or "#random#"
}

# check all settings are configured
for key in settings:
    if ((settings[key] is None) or (not isinstance(settings[key], str)) or (len(settings[key]) == 0)):
        logging.error(f'Missing setting from environment: {key}')
        exit(1)

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
except Exception as e:
    logging.error(f'Failed to sign in to reddit: ' + str(e))
    exit(1)

# announce user
logging.debug(f'Signed in as user: {reddit.user.me()}')

# check scopes
scopes = reddit.auth.scopes()
if scopes != {"*"}:
    logging.warn(f'Required scope (all: *) not obtained, scopes are: {scopes}')
    replaceAlphabet = string.ascii_letters + string.digits

logging.debug("Fetching user data")
try:
    redditor = reddit.redditor(settings['REDDIT_USER'])
except Exception as e:
    logging.error(f'Failed to fetch user data: {str(e)}')
    exit (1)

if settings['APP_REPLACE_STRING'] == '#random#':
    logging.debug('Performing action: Edit (with random string) and delete comments')
    replaceAlphabet = string.ascii_letters + string.digits
else:
    logging.debug('Performing action: Edit (with:{string}) and delete comments'.format(string=settings['APP_REPLACE_STRING']))

# remove deprecation warning
reddit.validate_on_submit = True

comments = 0
for comment in redditor.comments.new():
    sleep(REQUEST_DELAY_IN_SECONDS)
    comments += 1
    replaceString = settings['APP_REPLACE_STRING']
    if (replaceString == '#random#'):
        replaceString = ''.join(secrets.choice(replaceAlphabet) for i in range(32))
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

logging.info(f'Nuked {comments} comments and {posts} posts. Exiting.')