from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer
from api.ledgerUpdateApi import getConfig, getDevices
# Create your views here.

from .models import Application,Firmware,Device,FirmwareDistribution

#legacy api
def legacy_firmwares(request):
    try:
        return (200, getConfig(request.GET.get('provider', [""])[0], dict(request.GET)) ["firmwares"])
    except:
        return (404, {"error": "Provider not found"})

def legacy_applications(request):
    try:
        return (200, getConfig(request.GET.get('provider', [""])[0], dict(request.GET)) ["applications"])
    except:
        return (404, {"error": "Provider not found"})

def legacy_devices(request):
    try:
        return (200, getDevices(request.GET.get('provider', [""])[0], dict(request.GET)))
    except:
        return (404, {"error": "Provider not found"})

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