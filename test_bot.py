import json
import requests
from settings import TOKEN, HEROKU_URL

URL = 'https://api.telegram.org/bot{}/setWebhook'.format(TOKEN)


def add_webhook(URL):
    """
        add new webhook for our bot from URL
    :param URL:
    :return:
    """
    params = {
        "Content-Type": "application/json",
        "url": "{}api/v1".format(HEROKU_URL)
    }

    resp = requests.post(URL, params=params)
    return resp


def remove_webhook(URL):
    """
        to remove webhook, need just to send empty string to URL
    :param URL:
    :return:
    """

    resp = requests.get(URL)
    return resp


def send(URL, chat_id, msg):
    """
     send message to remote host
    :param URL: https://my_instance_name.herokuapp.com/my_api_version
    :param chat_id: telegram chat_id or @channel_id
    :param msg: text
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    data = {'message':
                {'from': {'id': chat_id},
                 'text': msg}
            }
    jdata = json.dumps(data)
    requests.post(URL, headers=headers, data=jdata)
