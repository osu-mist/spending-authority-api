import json
import requests

from config import Config
from flask import render_template, Flask
from forms import OnidForm


app = Flask(__name__)
app.config.from_object(Config)


def get_access():
    res = requests.post(app.config['TOKEN_URL'], data={
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
        'grant_type': 'client_credentials'})

    header = {'Authorization': 'Bearer {}'.format(res.json()['access_token'])}

    return header


@app.route('/', methods=['GET', 'POST'])
def index():
    onid = None
    onid_form = OnidForm()

    if onid_form.validate_on_submit():
        onid = onid_form.onid.data

    header = get_access()
    payload = {'onid': onid}
    res = json.loads(requests.get(
        app.config['API_URL'],
        headers=header,
        params=payload).text
    )

    return render_template('index.html', form=onid_form, onid=onid, res=res)


if __name__ == '__main__':
    app.run()
