from django.http import HttpResponse

def top_home(request):
    return HttpResponse("Hello, world. You're at the TOP home.")

