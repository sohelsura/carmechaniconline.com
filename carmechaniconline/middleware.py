from django.http import HttpResponsePermanentRedirect

class ForceWWWMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().lower()
        if not host.startswith('www.'):
            return HttpResponsePermanentRedirect(
                'https://www.%s%s' % (host, request.path)
            )
        return self.get_response(request)