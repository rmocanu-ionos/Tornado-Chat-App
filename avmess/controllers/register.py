import bcrypt
import logging

from django.core.exceptions import ObjectDoesNotExist

from avmess.controllers.handler import Handler
from avmess.models.user_model import UserModel
from avmess.response import Response

log = logging.getLogger(__name__)


class RegisterHandler(Handler):

    # headers: {}
    # verb: POST
    # url: /register
    # body: {
    #     username: ...
    #     password: ...
    # }

    @classmethod
    def post(cls, request, *args, **kwargs):

        log.info("solving register request")
        log.info(request)

        try:
            username = request.body['username']
            password = request.body['password']

        except KeyError:
            log.error('KeyError')
            return Response(request, status_code=400)

        try:
            UserModel.objects.get(name=username)

        except ObjectDoesNotExist:

            log.error('ObjectDoesNotExist')
            user = UserModel()
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user.add_entry(username, hash_password)
            user.save()

            return Response(request, status_code=200, body=user.serialize())

        return Response(request, status_code=400, error='User already in database')
