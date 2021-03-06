import json
import traceback
import asyncio
from abc import abstractmethod
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

    @abstractmethod
    async def _handler(self, message):
        """
        message transferring:
            1. find recipient (chat_id)
            2. create message for delivery

        :param message: dictionary message
        :return:
        """
        pass

    async def handler(self, request):
        """
            Use this handler with routing
        :param request:
        :return:
        """
        try:
            message = await request.json()
        except:
            print('data should be in JSON format')
            return web.Response(status=500)

        asyncio.ensure_future(self._handler(message['message']))
        return aiohttp.web.Response(status=200)


class ChannelConversation(Api):
    def __init__(self, token, loop, chat_id=None):
        super().__init__(token, loop)
        self._chat_id = chat_id

    async def _handler(self, message):
        _id = self._chat_id or message['chat']['id']
        message = {
            'chat_id': _id,
            'text': message['text']
        }
        await self._request('sendMessage', message)


@web.middleware
async def middleware_handler(request, handler):
    # try to convert to json
    try:
        data = await request.json()
    except Exception:
        print('data should be in JSON format')
        return web.Response(status=500)

    try:
        # only messages from WHITE LIST can be passed
        if data['message']['from']['id'] in (CHAT_WHITE_LIST + GROUP_WHITE_LIST):
            try:
                if data['message']['entities'][0]['type'] == 'bot_command':
                    print('internal bot command', data)
            except Exception:
                pass

            return await handler(request)  # should return response instance

        # SKIP FOREIGNERS
        else:
            try:
                # internal bot command
                if data['message']['entities'][0]['type'] == 'bot_command':
                    print('skip bot_command ', data)
                    return web.Response(status=200)
                # bot requests
                elif data['message']['from']['is_bot'] == True:
                    print('skip bots ', data)
                    return web.Response(status=200)
                # another case
                else:
                    return web.Response(status=200)
            except Exception:
                print('error from foreigner', data)
                return web.Response(status=500)

    except Exception:
        print('request without chat_id', data)
        return web.Response(status=500)


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
