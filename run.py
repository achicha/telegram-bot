import json
import traceback
import asyncio
import aiohttp
from aiohttp import web
from settings import TOKEN, CHAT_ID, PORT


API_URL = 'https://api.telegram.org/bot%s/sendMessage' % TOKEN


async def handler(request):
    try:
        data = await request.json()
    except:
        print('data should be in JSON format')

    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        'chat_id': CHAT_ID,     # post messages to the public channel
        'text': data['message']['text']
    }

    try:
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.post(API_URL,
                                    data=json.dumps(message),
                                    headers=headers) as resp:
                try:
                    assert resp.status == 200
                except:
                    print(traceback.format_exc())
                    return web.Response(status=500)
    except:
        print(traceback.format_exc())
    return web.Response(status=200)


async def init_app(loop):
    try:
        app = web.Application(loop=loop, middlewares=[])
        app.router.add_post('/api/v1', handler)
    except:
        print(traceback.format_exc())
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        app = loop.run_until_complete(init_app(loop))
        web.run_app(app, host='0.0.0.0', port=PORT)
    except Exception as e:
        print('Error create server: %r' % e)
        print(traceback.format_exc())
    finally:
        pass
    loop.close()
