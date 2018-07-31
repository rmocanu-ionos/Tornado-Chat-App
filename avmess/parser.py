import re

from avmess.server_utils import send_notification, get_preview


class Parser(object):

    patterns = [
        (r'^/timer *(?P<seconds>[0-9]*)', send_notification),
        (r'(?P<url>https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)', get_preview),
    ]

    @classmethod
    def get_handler(cls, url):

        for url_regex, handler in cls.patterns:

            match = re.search(url_regex, url)

            if match:
                return handler, match.groupdict()

        return None, None
