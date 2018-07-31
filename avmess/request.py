class Request(object):

    def __init__(self, web_socket, id, verb, url, body=None, headers=None, args=None):

        self.web_socket = web_socket

        self.id = id
        self.verb = verb
        self.url = url
        self.headers = headers or {}
        self.body = body or {}
        self.args = args or {}

        self._user = None

    def __str__(self):
        return "[ {} {} {} {} {} ]".format(
            self.id, self.verb, self.url, self.body, self.headers
        )

    def to_dict(self):
        return {
            'id': self.id,
            'verb': self.verb,
            'url': self.url,
            'headers': self.headers,
            'body': self.body,
            'args': self.args
        }
