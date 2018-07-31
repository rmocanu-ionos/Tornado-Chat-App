from functools import wraps
import time

from django.core.exceptions import ObjectDoesNotExist
import jwt

from avmess.models.user_model import UserModel
from avmess.response import Response
from avmess.server_utils import CLIENTS
from avmess.settings import secret


def check_authorization(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        request = args[1]
        headers = request.headers
        web_socket = request.web_socket

        token = headers.get('Authorization', None)

        if token is None:
            return Response(request, status_code=401)

        data = jwt.decode(token.split(' ')[1], secret)

        try:
            if time.time() - data['cat'] > 36000:
                return Response(request, status_code=401)

        except KeyError:
            return Response(request, status_code=401)

        uid = data['uid']
        CLIENTS[web_socket] = uid

        try:
            user = UserModel.objects.get(id=uid)
        except ObjectDoesNotExist:
            return Response(request, status_code=404, error='User does not exist')
        else:
            request.user = user

        return f(*args, **kwargs)

    return wrapper
