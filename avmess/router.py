import re

from avmess.controllers.login import LoginHandler
from avmess.controllers.register import RegisterHandler
from avmess.controllers.messages import MessageHandler
from avmess.controllers.connect import ConnectionHandler
from avmess.controllers.rooms import RoomHandler


class Router(object):

    urlpatterns = [
        (r'^/login/?$', LoginHandler),
        (r'^/register/?$', RegisterHandler),
        (r'^/messages/?$', MessageHandler),
        (r'^/messages(/?(?P<id>[0-9]*))/?$', MessageHandler),
        (r'^/connect/?$', ConnectionHandler),
        (r'^/rooms/?$', RoomHandler),
        (r'^/rooms(/?(?P<id>[0-9]*))/?$', RoomHandler),
    ]

    @classmethod
    def get_handler(cls, url):

        for url_regex, handler in cls.urlpatterns:

            match = re.match(url_regex, url)

            if match:
                return handler, match.groupdict()

        return None, None
