from tornado import httputil


class Response(object):

    def __init__(self, request, status_code=200, headers=None, body=None, error=None):
        self.request = request
        self.status_code = status_code
        self.headers = request.headers if not headers else request.headers.update(headers)
        self._body = body
        self.error = error or httputil.responses.get(status_code, "Unknown")

    @property
    def body(self):
        body = {}
        if 200 <= self.status_code <= 299:
            body = {
                'data': self._body
            }
        elif self.error is not None:
            body = {
                'error': self.error
            }
        return body

    def __str__(self):
        return "[ {} {} {} {} {} ]".format(
            self.request.id, self.status_code,
            self.request.headers, self.body, self.request.verb
        )

    def to_dict(self):
        return {
            'id': self.request.id,
            'status_code': self.status_code,
            'header': self.request.headers,
            'body': self.body,
            'verb': self.request.verb.upper(),
            'url': self.request.url
        }
