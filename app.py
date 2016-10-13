from flask import Flask, redirect, request, session, url_for
from flask import render_template
from functools import wraps
from utils import get_user_info, get_five_random_friends
import urllib
import requests
import json
import os


CLIENT_ID = os.environ.get('VK_CLIENT_ID')
CLIENT_SECRET = os.environ.get('VK_CLIENT_SECRET')
API_VERSION = '5.57'
REDIRECT_URI = 'http://vk-oauth-test.herokuapp.com/get_token'


app = Flask(__name__, static_url_path='')
app.secret_key = CLIENT_SECRET

auth_params = {
    'client_id': CLIENT_ID,
    'display': 'page',
    'redirect_uri': REDIRECT_URI,
    'scope': 'friends',
    'response_type': 'code',
    'v': API_VERSION,
}

access_token_params = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': REDIRECT_URI,
}


def build_url(url, params_dict):
    full = url + '?' + urllib.parse.urlencode(params_dict)
    return full


def require_vk_token(func):

    @wraps(func)
    def check_token(*args, **kwargs):
        if 'vk_token' not in session:
            return redirect(url_for('authorize'))
        return func(*args, **kwargs)

    return check_token


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/authorize')
def authorize():
    auth_url = build_url('https://oauth.vk.com/authorize', auth_params)
    return redirect(auth_url)


@app.route('/get_token')
def get_token():
    access_token_params['code'] = request.args['code']
    r = requests.get('https://oauth.vk.com/access_token',
                     params=access_token_params)

    response = json.loads(r.text)

    if (r.status_code == 200):
        session['vk_token'] = response['access_token']
        session['vk_user_id'] = response['user_id']
        return redirect(url_for('index'))

    return 'Error'


@app.route('/')
@require_vk_token
def index():
    token = session['vk_token']
    user_id = session['vk_user_id']

    user = get_user_info(token, user_id)
    friends = get_five_random_friends(token, user_id)

    data = {'user': user, 'friends': friends}
    return render_template('index.html', data=data)


@app.route('/logout')
@require_vk_token
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
