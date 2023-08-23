import quart
import argparse
import aiohttp
import time
import os
import types

try:
    fcm_token = os.environ['FCM_TOKEN']
except KeyError:
    raise RuntimeError("Missing FCM_TOKEN from env")

api_token = os.environ.get('API_TOKEN')

timeout = os.environ.get('TIMEOUT')
if timeout is not None:
    timeout = int(timeout)

app = quart.Quart(__name__)
app.cli.allow_extra_args = True


@app.before_serving
async def app_setup():
    app.http = types.SimpleNamespace()
    app.http.client = aiohttp.ClientSession()
    app.cache = {}

@app.post('/api/fcm/send')
async def api_send():
    data = await quart.request.json
    to = data['to']
    token = quart.request.headers.get('Authorization')
    throttled = (token is None) or (token != f'Bearer {api_token}')
    if throttled and (timeout is not None):
        now = time.time()
        try:
            time_last = app.cache[to]
            time_delta = now - time_last
            if time_delta <= timeout:
                return f'Please wait for {int(timeout - time_delta)} seconds', 429
        except KeyError:
            pass
        app.cache[to] = now

    response = await app.http.client.post(
        'https://fcm.googleapis.com/fcm/send',
        json=await quart.request.json,
        headers={
            'Authorization': f'key={fcm_token}'
        }
    )
    return quart.Response(
        await response.text(),
        response.status,
        {'Content-Type': 'application/json'}
    )
