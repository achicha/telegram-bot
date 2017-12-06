HowTo:

1. Create your own bot using Telegram's [BotFather](https://core.telegram.org/bots#3-how-do-i-create-a-bot) and grab your `TOKEN`
2. Clone this repository
    - `git clone https://github.com/achicha/telegram-bot`
3. Virtual Environment (optional):
    - `cd telegram-bot`
    - `pip install` [pipenv](https://github.com/kennethreitz/pipenv)
4. Install all dependencies:
    - `pipenv install` or `pip install -r Pipfile`
5. Try local [heroku](https://devcenter.heroku.com/articles/deploying-python)
    - install: `wget -qO- https://cli-assets.heroku.com/install-ubuntu.sh | sh`
    - create entry point. `touch Procfile` with `web: python run.py` inside it.
    - login: `heroku login`
    - create app: `heroku create`
    - create `.env` file and add there config vars from `settings.py`
    - run local heroku: `heroku local web`
6. Deploy to remote heroku:
    - add heroku remote branch: `heroku git:remote -a MyHerokuAppName` if it is not there `git remote -v`
    - copy .env params to the server: `heroku config:push`
    - deploy: `git push heroku master`
    - check logs: `heroku logs -n 10`
    - restart app if needed: `heroku restart MyHerokuAppName`
    

Links:

- https://habrahabr.ru/post/322078/
- https://habrahabr.ru/post/300942/
- https://devcenter.heroku.com/articles/deploying-python
- https://github.com/volodymyrlut/heroku-node-telegram-bot