import json
import requests

from flask import Flask

app = Flask(__name__)


def get_token():
    config = json.load(open('configuration.json'))
    api_url = config['hostname'] + config['version'] + config['api']
    token_url = config['token_url']
    client_id = config['client_id']
    client_secret = config['client_secret']

    res = requests.post(token_url, data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'})

    print(res)

    return api_url, res.json()['access_token']


@app.route('/')
def index():
    api_url, token = get_token()
    print(api_url)
    print(token)
    return 'Hello World'


if __name__ == '__main__':
    app.run()
