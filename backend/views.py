from django.http import HttpResponse


def server_up(request):
    return HttpResponse(status=200)
