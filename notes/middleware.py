from django.utils import timezone

import pytz


class TimezoneMiddleware(object):
    def __init__(self, get_response): # otherwise, django middleware error with middleware takes no argument
            self.get_response = get_response

    def __call__(self, request): # otherwise, django middleware error with middleware takes no argument
        return self.get_response(request)

    def process_request(self, request):
        if request.user.is_authenticated():
            timezone.activate(pytz.timezone(request.user.profile.timezone))
        else:
            timezone.deactivate()
