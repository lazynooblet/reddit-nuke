# latest 3.x version of python on latest debian
FROM python:3-slim

# set arg
ARG PIP_ROOT_USER_ACTION=ignore
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBCONF_NOWARNINGS="yes"

# install packages from apt
RUN apt-get clean && apt-get update && apt-get install --no-install-recommends -y dumb-init && apt-get clean

# change to this folder in the container
WORKDIR /app

# install python app requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# copy our app files
COPY src/ .

# create app user
RUN useradd --no-create-home --home-dir /app --shell /bin/bash app

# run as non-privileged user
USER app

# use our init daemon as entrypoint
ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]

# run the app
CMD [ "python", "./app.py" ]