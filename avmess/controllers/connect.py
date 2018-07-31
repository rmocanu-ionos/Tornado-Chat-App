import logging

from django.core.exceptions import ObjectDoesNotExist

from avmess.controllers.handler import Handler
from avmess.decorators import check_authorization
from avmess.models.message_model import MessageModel
from avmess.models.room_model import RoomModel
from avmess.response import Response
from avmess.server_utils import ROOMS

log = logging.getLogger(__name__)


class ConnectionHandler(Handler):

    # headers: {
    #     Authorization: token <token>
    # }
    # id:...
    # verb: POST
    # url: /connect
    # body: {
    #     room_id:...
    # }

    @classmethod
    @check_authorization
    def post(cls, request, *args, **kwargs):

        print("solving join request")
        print(request)

        try:
            body = request.body
            room_id = body['room_id']

        except KeyError:
            log.error('KeyError')
            return Response(request, status_code=400)

        try:
            room = RoomModel.objects.get(id=room_id)

        except ObjectDoesNotExist:
            log.error('ObjectDoesNotExist')
            return Response(request, status_code=404, error='Room does not exist')

        if ROOMS.get(room.id, None) is None:
            ROOMS[room.id] = set()

        ROOMS[room.id].add(request.web_socket)
        messages = MessageModel.objects.filter(room_id=room).order_by('-created_at')[:5]

        response_body = []
        for message in messages:
            response_body.append(message.serialize())

        return Response(request, status_code=200, body=response_body)

    # headers: {
    #     Authorization: token <token>
    # }
    # verb: DELETE
    # url: /connect
    # body: {
    #
    #     room_id:...
    # }

    @classmethod
    @check_authorization
    def delete(cls, request, *args, **kwargs):

        print("solving leave request")
        log.info(request)

        try:
            body = request.body
            room_id = body['room_id']

        except KeyError:
            log.error('KeyError')
            return Response(request, status_code=400)

        try:
            room = RoomModel.objects.get(id=room_id)

        except ObjectDoesNotExist:
            log.error('ObjectDoesNotExist')
            return Response(request, status_code=404, error='Room does not exist')

        if request.web_socket not in ROOMS[room.id]:
            return Response(request, status_code=400, error='User was not joined')
        ROOMS[room.id].remove(request.web_socket)

        return Response(request, status_code=200)
