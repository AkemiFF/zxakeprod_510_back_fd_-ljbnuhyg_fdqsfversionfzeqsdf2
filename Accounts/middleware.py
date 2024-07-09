from django.http import JsonResponse


class CSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/api/info/client/create/' and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if 'HTTP_X_CSRFTOKEN' not in request.META:
                print(request.META)
                return JsonResponse({'detail': 'CSRF token missing or incorrect.'}, status=403)

        response = self.get_response(request)
        return response
