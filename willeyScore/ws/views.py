from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
#from django.template import Context, loader

from ws.models import *

def home(request):
    event_list = Event.objects.all().order_by('-sort_order')[:5]
    context = {'event_list': event_list}
    return render(request, 'ws/index.html', context)

def event_sub(request, event_short_name):
    e = get_object_or_404(Event, short_name=event_short_name)
    return render(request, 'ws/event.html', {'e': e})

def event(request, event_short_name):
    e = get_object_or_404(Event, short_name=event_short_name)
    return render(request, 'ws/event.html', {'e': e})

def oa(request, event_short_name):
    e = get_object_or_404(Event, short_name=event_short_name)
    return render(request, 'ws/oa.html', {'e': e})

def comp_class(request):
    return HttpResponse("You're setting comp_classes")

def scoring_rules(request):
    return HttpResponse("You're setting scoring_rules")

def cars(request, event_short_name):
    return HttpResponse("You're setting cars for %s" % event_short_name)

def detail(request, event_short_name):
    return HttpResponse("You're looking at checkpoint %s." % event_short_name)

def stats(request, event_short_name):
    data = serializers.serialize("xml", EventResults.objects.all())
    return HttpResponse("You're looking at the summary %s that has the data: %s." % (event_short_name, data))

def inout(request, event_short_name):
    file = ("/tmp/%s_event.xml" % event_short_name)
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    with open(file, "w") as out:
        xml_serializer.serialize(Event.objects.all(), stream=out)
    return HttpResponse("%s was dumped to %s." % (event_short_name, file))

