import requests
import json
import random


def get_user_info(access_token, user_id):
    params = {
        'access_token': access_token,
        'user_ids': user_id,
        'v': '5.57'
    }
    r = requests.get('https://api.vk.com/method/users.get',
                     params=params)
    return json.loads(r.text)['response'][0]


def get_friend_ids(access_token, user_id):
    params = {
        'access_token': access_token,
        'user_id': user_id,
        'v': '5.57'
    }
    r = requests.get('https://api.vk.com/method/friends.get',
                     params=params)
    return json.loads(r.text)['response']


def get_five_random_friends(access_token, user_id):
    ids = get_friend_ids(access_token, user_id)['items']
    random_ids = random.sample(ids, 5)
    users = []
    for id in random_ids:
        users.append(get_user_info(access_token, id))
    return users
