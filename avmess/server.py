import os
import json
import logging

import tornado.concurrent
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avmess.django_settings")
setup()

from avmess.request import Request
from avmess.server_utils import CLIENTS, ROOMS, show_rooms
from avmess.router import Router
from avmess.response import Response
from avmess.rooms_setup import rooms_setup
from avmess.settings import CONF

log = logging.getLogger(__name__)


class WSHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        CLIENTS[self] = None
        log.info("open")

    def on_message(self, message):

        print("on message" + message)
        msg_dict = json.loads(message)

        args = msg_dict.get('args', None)

        req = Request(
            self, msg_dict['id'], msg_dict['verb'], msg_dict['url'],
            body=msg_dict.get('body'), headers=msg_dict.get('headers'), args=args
        )

        def future_done(f):
            try:
                res = f.result()
            except Exception:
                res = Response(req, 500)

            print(ROOMS)
            self.write_message(json.dumps(res.to_dict()))

        handler, handler_kwargs = Router.get_handler(req.url)

        if handler is None:
            result = Response(req, 404)
        else:
            method = getattr(handler, req.verb.lower(), None)

            if method:
                result = method(req, **handler_kwargs)

                if isinstance(result, tornado.concurrent.Future):
                    tornado.ioloop.IOLoop.current().add_future(result, future_done)
                    return
            else:
                result = Response(req, 405)

        show_rooms()

        self.write_message(json.dumps(result.to_dict()))

    def on_close(self):

        CLIENTS.pop(self)

        for room in ROOMS.values():
            if self in room:
                room.remove(self)

        log.info("on_close")


class MainHandler(tornado.web.RequestHandler):

    def get_template_path(self):
        return CONF.web_dir

    def get(self, *args, **kwargs):
        self.render('index.html', cdn='web')


def main():
    rooms_setup()
    settings = dict(
        debug=True,
        static_path=CONF.web_dir
    )

    application = tornado.web.Application([
        (r"/ws/?", WSHandler),
        (r"^/(.*)", MainHandler),
        (r"/static/(.*)/?", tornado.web.StaticFileHandler, {'path': CONF.web_dir}),
    ], **settings)

    application.listen(CONF.port)
    log.info('Incepem')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
