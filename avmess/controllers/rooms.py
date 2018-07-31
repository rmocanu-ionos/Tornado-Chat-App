import logging

from django.core.exceptions import ObjectDoesNotExist

from avmess.controllers.handler import Handler
from avmess.decorators import check_authorization
from avmess.models.room_model import RoomModel
from avmess.response import Response
from avmess.server_utils import ROOMS

log = logging.getLogger(__name__)


class RoomHandler(Handler):

    # headers: {
    #     Authorization: token <token>
    # }
    # verb: POST
    # url: /rooms
    # body: {
    #     name: ...
    #     topic: ...
    # }

    @classmethod
    @check_authorization
    def post(cls, request, *args, **kwargs):

        log.info("solving create room request")
        log.info(request)

        try:
            body = request.body
            room_name = body['name']
            room_topic = body['topic']

        except KeyError:
            log.error('KeyError')
            return Response(request, status_code=400)

        try:
            room = RoomModel.objects.get(name=room_name)
            return Response(request, status_code=400, body=room.serialize())

        except ObjectDoesNotExist:

            log.error('ObjectDoesNotExist')
            new_room = RoomModel()
            new_room.add_entry(room_name, room_topic)
            new_room.save()

            created_room = RoomModel.objects.get(name=room_name)
            ROOMS[created_room.id] = set()
            ROOMS[created_room.id].add(request.web_socket)

            return Response(request, status_code=200, body=created_room.serialize())


    # headers: {
    #     Authorization: token <token>
    # }
    # verb: DELETE
    # url: /rooms
    # body: {
    #     id: ...
    # }

    @classmethod
    @check_authorization
    def delete(cls, request, *args, **kwargs):

        log.info("solving delete room request")
        log.info(request)

        try:
            room_id = kwargs['id']

        except KeyError:
            log.error('KeyError')
            return Response(request, status_code=400)

        try:
            room = RoomModel.objects.get(id=room_id)

        except ObjectDoesNotExist:
            log.error('ObjectDoesNotExist')
            return Response(request, status_code=404, error='Room does not exist')

        if len(ROOMS[room.id]) > 0:
            return Response(request, status_code=400, error='Room must be empty to be deleted')
        ROOMS.pop(room.id)
        room.delete()

        return Response(request,  status_code=200)

    # headers: {
    #     Authorization: token <token>
    # }
    # verb: GET
    # url: /rooms or /rooms/<id>
    # body: {}

    @classmethod
    @check_authorization
    def get(cls, request, *args, **kwargs):

        log.info("solving get room request")
        log.info(request)

        response_body = []

        if kwargs.get('id', None) is not None:
            room_id = kwargs['id']
            room = RoomModel.objects.get(id=room_id)

            return Response(request, status_code=200, body=room.serialize())

        for room in RoomModel.objects.all():
            response_body.append(room.serialize())

        return Response(request, status_code=200, body=response_body)

    # headers: {
    #     Authorization: token <token>
    # }
    # verb: PUT
    # url: /rooms
    # body: {
    #     id: ...
    #     topic: ...
    # }

    @classmethod
    @check_authorization
    def put(cls, request, *args, **kwargs):

        log.info("solving put room request")
        log.info(request)

        try:
            body = request.body
            room_id = kwargs['d']
            room_topic = body['topic']

        except KeyError:
            log.error('KeyError')
            return Response(request, status_code=400)

        try:
            room = RoomModel.objects.get(id=room_id)

        except ObjectDoesNotExist:
            log.error('ObjectDoesNotExist')
            return Response(request, status_code=404, error='Room does not exist')

        room.topic = room_topic
        room.save()

        return Response(request, status_code=200, body=room.serialize())
