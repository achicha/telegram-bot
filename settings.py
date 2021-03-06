"""
register our bot in telegram:
1. go to @BotFather
    - /start
    - /newbot
    - create name endswith "bot".
    - get unique toke like 311825528:AAE3r8V7iaIiXzJY_s0-9brG6JMWbT126qB
    - add bot to your telegram contacts
2. get bot's id and name:
    - id and first_name from page: api.telegram.org/bot<TOKEN>/getMe
3. get chat_id:
    - id from page://api.telegram.org/botXXXX:TOKEN/getUpdates
4. check. send your msg to bot.
    curl --header 'Content-Type: application/json' -X POST \
    --data '{"chat_id":"281724313","text":"your_message"}' \
    "https://api.telegram.org/bot311825528:AAE3r8V7iaIiXzJY_s0-9brG6JMWbT126qB/sendMessage"
5. example webhook:
    - https://habrahabr.ru/post/322078/
"""

import os
import sys
from envparse import env

path = os.path.abspath(os.path.dirname(sys.argv[0]))

if os.path.isfile(os.path.join(path, '.env')):
    env.read_envfile(os.path.join(path, '.env'))

TOKEN = env.str('TOKEN')
CHAT_ID = env.str('CHAT_ID')
PORT = int(env.str('PORT'))
CHAT_WHITE_LIST = [int(i) for i in env.str('CHAT_WHITE_LIST').split(',')]
GROUP_WHITE_LIST = env.str('GROUP_WHITE_LIST').split(',')

str_command = 'heroku info -s | grep web_url | cut -d= -f2'
HEROKU_URL = os.system(str_command)
#DATABASE_URL = os.environ['DATABASE_URL']
