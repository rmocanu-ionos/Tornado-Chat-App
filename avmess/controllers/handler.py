from avmess.response import Response


class Handler(object):

    @classmethod
    def post(cls, request, *args, **kwargs):
        return Response(request, status_code=405)

    @classmethod
    def get(cls, request, *args, **kwargs):
        return Response(request, status_code=405)

    @classmethod
    def put(cls, request, *args, **kwargs):
        return Response(request, status_code=405)

    @classmethod
    def delete(cls, request, *args, **kwargs):
        return Response(request, status_code=405)
