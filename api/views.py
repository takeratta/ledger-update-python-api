import json

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

from api import retrievingTools
from api.ledgerUpdateApi import getConfig, getDevices
from api.serializers import UserSerializer, GroupSerializer
from .models import Application, Device
from django.core import serializers


#legacy api
def legacy_applications(request):
    response = retrievingTools.get_applications_legacy(request)
    return HttpResponse(json.dumps(response[1]),status_code = response[0], content_type = 'application/json')


def legacy_firmwares(request):
    response = retrievingTools.get_firmwares_legacy(request)
    return HttpResponse(json.dumps(response[1]),status_code = response[0], content_type = 'application/json')


def new_applications(request):
    response  = retrievingTools.get_new_app(request)
    return HttpResponse(json.dumps(response[1]),status_code = response[0], content_type = 'application/json')



def index(request):
    latest_updates = Application.objects.order_by('updated')[:5]
    context = {
        'latest_updates': latest_updates,
    }
    return render(request,'api/index.html',context)


def manage_devices(request):
    devices = Device.objects.all()
    return render(request, 'api/manage_devices.html',{'devices':devices})


def manage_device(request,device_id):
    device = Device.objects.filter(id=device_id)[0]
    return render(request, 'api/manage_device.html',{'device':device})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


