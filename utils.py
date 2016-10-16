import requests
import json
import random


def get_users(access_token, user_ids):
    print(type(user_ids[0]))
    print()
    params = {
        'access_token': access_token,
        'user_ids': ','.join([str(id) for id in user_ids]),
        'v': '5.57'
    }
    print(params['user_ids'])
    r = requests.get('https://api.vk.com/method/users.get',
                     params=params)
    return json.loads(r.text)['response']


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
    users = get_users(access_token, random_ids)
    print(users)
    return users
