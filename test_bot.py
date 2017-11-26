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
