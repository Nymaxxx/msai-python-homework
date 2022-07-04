import time

from django.http import HttpResponse


def wait(req):
    time.sleep(1)
    return HttpResponse("Hello, world!")