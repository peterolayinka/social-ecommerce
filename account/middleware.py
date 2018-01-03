from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

# class SetLastVisitMiddleware(object):
#     def process_response(self, request, response):
#         if request.user.is_authenticated():
#             # Update last visit time after request finished processing.
#             User.objects.filter(pk=request.user.pk).update(last_login=now())
#         return response


class SetLastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            User.objects.filter(pk=request.user.pk).update(last_login=now())
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
