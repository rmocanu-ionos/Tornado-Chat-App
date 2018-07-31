import time
import logging

from django.core.exceptions import ObjectDoesNotExist
import tornado.ioloop
from tornado import gen

from avmess.response import Response
from avmess.parser import Parser
from avmess.controllers.handler import Handler
from avmess.decorators import check_authorization
from avmess.models.user_model import UserModel
from avmess.models.room_model import RoomModel
from avmess.models.message_model import MessageModel
from avmess.server_utils import ROOMS, send_notification, get_preview, broadcast

log = logging.getLogger(__name__)


class MessageHandler(Handler):

    # headers: {
    #     Authorization: token <token>
    # }
    # verb: POST
    # url: /messages
    # body: {
    #     message: ...
    #     room_id: ...
    # }
    @classmethod
    @check_authorization
    @gen.coroutine
    def post(cls, request,  *args, **kwargs):

        log.info("solving message request")
        log.info(request)

        try:
            body = request.body
            uid = request.user.id
            msg = body['message']
            room_id = body['room_id']

        except KeyError:
            raise gen.Return(Response(request, status_code=400))

        try:
            RoomModel.objects.get(id=room_id)

        except ObjectDoesNotExist:
            raise gen.Return(Response(request, status_code=404, error='Room does not exist'))

        if request.web_socket not in ROOMS[room_id]:
            raise gen.Return(Response(request, status_code=400, error='User must be in this room'))

        handler, kw_args = Parser.get_handler(msg)
        if handler == send_notification:
            tornado.ioloop.IOLoop.current().add_timeout(time.time() + float(kw_args.get('seconds')),
                                                        handler, request.web_socket)
            raise gen.Return(Response(request, status_code=200))

        preview = None

        if handler == get_preview:
            preview = yield get_preview(kw_args.get('url'))

        message = MessageModel()
        message.add_entry(UserModel.objects.get(id=uid), RoomModel.objects.get(id=room_id), msg)
        message.save()

        # update headers before broadcast
        request.headers = {}
        msg = message.serialize()
        msg['preview'] = {'code': preview.code if preview else None,
                          'length': len(preview.body)if preview else 0}

        message_to_send = Response(request, 200,
                                   body=msg)

        # get users connected to the room
        try:
            sockets_to_broadcast = ROOMS[room_id]
        except KeyError:
            raise gen.Return(Response(request, status_code=400, error='Room not active'))

        # send each of them a message
        broadcast(sockets_to_broadcast, message_to_send, request.web_socket)

        raise gen.Return(Response(request, status_code=200, body=msg))

    # headers: {
    #     Authorization: token <token>
    # }
    # verb: GET
    # url: /messages or /messages/<id>
    # body: {}
    # args {
    #     room_id:..
    # }

    @classmethod
    @check_authorization
    def get(cls, request, *args, **kwargs):

        log.info("solving get message request")
        log.info(request)

        if kwargs.get('id', None) is not None:
            msg_id = kwargs['id']

            message = MessageModel.objects.get(id=msg_id)

            return Response(request, status_code=200, body=message.serialize())

        try:
            room_id = request.args['room_id']

        except KeyError:
            return Response(request, status_code=400)

        except TypeError:
            return Response(request, status_code=400)

        room = RoomModel.objects.get(id=room_id)
        messages = MessageModel.objects.filter(room_id=room).order_by('-created_at')[:50]

        response_body = []
        for message in messages:
            response_body.append(message.serialize())

        return Response(request, status_code=200, body=response_body)
