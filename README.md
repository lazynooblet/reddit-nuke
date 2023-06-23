# reddit-nuke
- Python script using PRAW with docker build
- Will edit, then delete all comments, and delete all posts
- By default edits comments with a random string
- Logs to stdout
- Each deletion request is delayed by 5 seconds to prevent reaching API limit (edit REQUEST_DELAY_IN_SECONDS constant to adjust)

Reddit is periodically restoring comments, this will continuously remove them.

This was created as a basis to learn how to package a python script into a docker container.

## Run using docker-compose
1. Clone this repo
2. Copy the example docker-compose.yml,example to docker-compose.yml
3. Add reddit credentials, and edit any other options
4. docker-compose up --build

## Setting up Reddit user API
1. Visit Reddit app preferences at https://www.reddit.com/prefs/apps
2. Click [create another app...] at the bottom
3. Give your app a name
4. Choose "script" as the type
5. Put whatever you want as the redirect uri (ie. http://localhost/)
6. Click create app
7. You will then be given a clientid (its the random string under the name of your app), and a client secret
