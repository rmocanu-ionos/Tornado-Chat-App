import json

import websocket

from avmess.request import Request


def send_request(webS, id, verb, url, body, headers, args=None):

    webS.send(json.dumps(Request(None, id, verb, url, body, headers, args).to_dict()))

    message = webS.recv()
    msg_dict = json.loads(message)

    print(msg_dict)

    if (url == '/login' or url == '/login/') and (verb == 'POST' or verb == 'post'):
        try:
            token = msg_dict['body']['data']['token']

            return token

        except KeyError:

            return None

    return None


def senda_request(webS, id, verb, url, body, headers, args=None):

    webS.send(json.dumps(Request(None, id, verb, url, body, headers, args).to_dict()))


def reset():
    ws.connect("ws://192.168.10.55:8889/ws")


ws = websocket.WebSocket()
ws.connect("ws://192.168.10.55:8889/ws")

test_user = {'username': 'test', 'password': 'test'}

test_user2 = {'username': 'test2', 'password': 'test2'}
