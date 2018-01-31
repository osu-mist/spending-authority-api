# Spending Authority API Demo

A demo app for Spending Authority API built with [Flask](http://flask.pocoo.org/) framework and Python 3.

## Configuration

1. Register an application via [OSU Developer Portal](https://developer.oregonstate.edu/)
2. Get `client_id` and `client_secret` from your app, then copy
[config-example.py](./config-example.py) as config.py and modify it as necessary.

## Usage

1. To install app dependencies, simply run:

```
$ pip install -r requirements.txt
```

2. Start the app at [localhost:5000](http://localhost:5000):

```
$ python app.py
```

## Docker

[Dockerfile](Dockerfile) is also provided. To run this app in a container, just simply install [Docker](https://www.docker.com/) first, then:

1. Build the docker image:

```
$ docker build -t spend-auth-api-demo .
```

2. Run the app in a container:

```
$ docker run -d \
             -p 5000:5000 \
             -v "$PWD"/config.py:/usr/src/app/config.py:ro \
             --name spend-auth-api-demo \
             spend-auth-api-demo
```
