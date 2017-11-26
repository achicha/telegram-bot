# set webhook
from grab import Grab
from settings import TOKEN, HEROKU_URL

g = Grab()
params = {
    "Content-Type": "application/json",
    "url": "{}api/v1".format(HEROKU_URL)
}
g.go('https://api.telegram.org/bot{}/setWebhook'.format(TOKEN), post=params)
