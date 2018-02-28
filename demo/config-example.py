class Config(object):
    API_URL = 'https://api.example.com/v1/spendingauthority'
    TOKEN_URL = 'https://api.oregonstate.edu/oauth2/token'
    CLIENT_ID = 'client_id'
    CLIENT_SECRET = 'client_secret'
    SECRET_KEY = 'secret_key'  # this secret key is for CSRF prevention
    CAS_URL = 'https://login.oregonstate.edu/cas-dev'
    SERVICE_URL = 'http://localhost:5000/' # url used by cas to redirect after authenticating
    AUTHORIZED_USERS = ['doejohn'] # list of users authorized to use the application
