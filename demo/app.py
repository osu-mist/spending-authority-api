import json
import requests
import flask
import urllib
import xml.etree.ElementTree as elementtree

from config import Config
from flask import render_template, Flask
from forms import OnidForm


app = Flask(__name__)
app.config.from_object(Config)

request = flask.request
session = flask.session

def get_access():
    res = requests.post(app.config['TOKEN_URL'], data={
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
        'grant_type': 'client_credentials'})

    header = {'Authorization': 'Bearer {}'.format(res.json()['access_token'])}

    return header


@app.route('/', methods=['GET', 'POST'])
def index():
    cas_url = app.config['CAS_URL']
    service_url = app.config['SERVICE_URL']
    authorized_users = app.config['AUTHORIZED_USERS']

    if u'ticket' in request.args:
        # got cas; validate ticket
        try:
            user = validate_cas(cas_url, request.args[u'ticket'], service_url)
        except CASError as e:
            return u'login failed (%s)' % str(e), 403
        except Exception as e:
            return u'login failed', 403

        # save user
        session['user'] = user
    elif u'user' not in session:
        # redirect to cas
        return flask.redirect(cas_url+"/login?service="+urllib.parse.quote(service_url))

    if session['user'] not in authorized_users:
        return render_template('unauthorized.html')

    onid, response = None, {}
    onid_form = OnidForm()

    if onid_form.validate_on_submit():
        onid = onid_form.onid.data

        header = get_access()
        payload = {'onid': onid}
        res = requests.get(app.config['API_URL'], headers=header, params=payload)
        response['code'] = res.status_code
        response['data'] = json.loads(res.text)['data']

    return render_template('index.html', form=onid_form, onid=onid, res=response)

class CASError(Exception):
    def __init__(self, msg, code=''):
        self.msg = msg
        self.code = code
    def __str__(self):
        if self.code and self.msg:
            return str(self.msg) + " (" + str(self.code) + ")"
        if self.msg:
            return str(self.msg)
        return str(self.code)

def validate_cas(cas_url, ticket, service):
    r = requests.get(cas_url+'/serviceValidate', params={'ticket': ticket, 'service': service})
    if r.status_code != 200:
        raise CASError('invalid response')

    # note: processing xml from untrusted sources is unsafe
    # https://docs.python.org/2/library/xml.html#xml-vulnerabilities
    try:
        root = elementtree.fromstring(r.text)
    except elementtree.ParseError:
        raise CASError('invalid response')

    ns = '{http://www.yale.edu/tp/cas}'
    if root.tag != ns+'serviceResponse':
        raise CASError('invalid response')

    authenticationFailure = root.find(ns+'authenticationFailure')
    authenticationSuccess = root.find(ns+'authenticationSuccess')

    if authenticationFailure is not None:
        raise CASError(authenticationFailure.text.strip(), authenticationFailure.get('code'))

    if authenticationSuccess is not None:
        user = authenticationSuccess.find(ns+'user')
        return user.text

    raise CASError('invalid response')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
