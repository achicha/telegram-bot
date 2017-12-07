import json
import traceback
import asyncio
import aiohttp
from aiohttp import web
from settings import TOKEN, CHAT_ID, PORT, CHAT_WHITE_LIST, GROUP_WHITE_LIST


class Api(object):
    URL = 'https://api.telegram.org/bot%s/%s'

    def __init__(self, token, loop):
        self._token = token
        self._loop = loop

    async def _request(self, method, message):
        headers = {
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession(loop=self._loop) as session:
            async with session.post(self.URL % (self._token, method),
                                    data=json.dumps(message),
                                    headers=headers) as resp:
                try:
                    assert resp.status == 200
                except:
                    print(traceback.format_exc())
                    return web.Response(status=500)

    async def _handler(self, message):
        pass

    async def handler(self, request):
        try:
            message = await request.json()
        except:
            print('data should be in JSON format')
            return web.Response(status=500)

        asyncio.ensure_future(self._handler(message['message']))
        return aiohttp.web.Response(status=200)

    async def sendMessage(self, chat_id, text):
        """

        :param chat_id: ChatId of telegram user/channel
        :param text: JSON message
        :return:
        """
        message = {
            'chat_id': chat_id,
            'text': text
        }
        await self._request('sendMessage', message)


class ChannelConversation(Api):
    def __init__(self, token, loop, chat_id=None):
        super().__init__(token, loop)
        self._chat_id = chat_id

    async def _handler(self, message):
        _id = self._chat_id or message['chat']['id']
        await self.sendMessage(_id, message['text'])


@web.middleware
async def middleware_handler(request, handler):
    data = await request.json()

    # skip internal bot command
    try:
        if data['message']['entities'][0]['type'] == 'bot_command':
            print('skip bot_command ', data)
            return web.Response(status=200)
    except:
        pass
    # skip not my messages
    if data['message']['from']['id'] not in (CHAT_WHITE_LIST + GROUP_WHITE_LIST):
        print('chat_id NOT in white list ', data)
        return web.Response(status=200)
    # skip bot requests
    if data['message']['from']['is_bot'] == True:
        print('skip bots ', data)
        return web.Response(status=200)

    return await handler(request)  # should return response instance


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    channel_bot = ChannelConversation(TOKEN, loop, CHAT_ID)

    try:
        app = web.Application(loop=loop, middlewares=[middleware_handler])
        app.router.add_post('/api/v1', channel_bot.handler)
        web.run_app(app, host='0.0.0.0', port=PORT)
    except:
        print(traceback.format_exc())
    finally:
        loop.close()
