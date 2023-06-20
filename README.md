# reddit-nuke
- Python script using PRAW with docker build
- Will edit, then delete all comments, and delete all posts
- By default edits comments with a random string
- Logs to stdout

Reddit is periodically restoring comments, so suggest to run this on cron

## Run using docker-compose
1. Clone this repo into ./build
2. Copy the example docker-compose.yml, add reddit credentials (notice it references ./build)
3. docker-compose up

## Setting up Reddit user API
1. Visit Reddit app preferences at https://www.reddit.com/prefs/apps
2. Click [create another app...] at the bottom
3. Give your app a name
4. Choose "script" as the type
5. Put whatever you want as the redirect uri (ie. http://localhost/)
6. Click create app
7. You will then be given a clientid (its the random string under the name of your app), and a client secret
