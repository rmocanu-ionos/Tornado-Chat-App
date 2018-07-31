import json
import logging

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from avmess.request import Request
from avmess.response import Response

CLIENTS = {}
ROOMS = {}
log = logging.getLogger(__name__)


def send_notification(web_socket):
    req = Request(web_socket, id=-1, verb='POST', url='/notifications',
                  body='Timer expired')


    web_socket.write_message(json.dumps(Response(req, status_code=200, body=req.body).to_dict()))


@gen.coroutine
def get_preview(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)

    raise gen.Return(response)


def broadcast(sockets_to_broadcast, message, request_socket=None):
    for socket in sockets_to_broadcast:
        if socket != request_socket:
            socket.write_message(json.dumps(message.to_dict()))


def get_users_in_room(room_sockets):

    s = '['

    for socket in room_sockets:
        s += str(CLIENTS[socket])
        s += ', '

    s += ']'

    return s


def show_rooms():

    s = ''

    for (room_id, room) in ROOMS.iteritems():
        s += '[room_id: {}, members: {}] '.format(room_id, get_users_in_room(room))

    log.info(s)
