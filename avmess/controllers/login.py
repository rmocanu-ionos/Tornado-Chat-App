import bcrypt
import jwt
import logging
import time

from django.core.exceptions import ObjectDoesNotExist

from avmess.controllers.handler import Handler
from avmess.models.user_model import UserModel
from avmess.response import Response
from avmess.server_utils import CLIENTS
from avmess.settings import secret

log = logging.getLogger(__name__)


class LoginHandler(Handler):

    # id:...
    # verb: POST
    # url: /connect
    # body: {
    #     username:...
    #     password:...
    # }

    @classmethod
    def post(cls, request, *args, **kwargs):

        print("solving login request")
        log.info(request)

        try:
            username = request.body['username']
            password = request.body['password']
            web_socket = request.web_socket

        except KeyError:
            log.error('KeyError')
            return Response(request, 400, error='Missing argument')

        # TODO: not necessary
        if CLIENTS[web_socket] is not None:
            return Response(request, 400, error='Already logged in')

        try:
            user = UserModel.objects.get(name=username)

        except ObjectDoesNotExist:
            log.error('ObjectDoesNotExist')
            return Response(request, 404, error='username or password wrong')

        password = password.encode('utf-8')
        password_hash = user.password.encode('utf-8')

        if not bcrypt.checkpw(password, password_hash):
            return Response(request, 401)

        enc = jwt.encode({'uid': user.id, 'cat': time.time()}, secret)
        CLIENTS[web_socket] = user.id

        response_body = user.serialize()
        response_body['token'] = enc

        return Response(request, status_code=200, body=response_body)
