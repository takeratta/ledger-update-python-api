import json

from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import viewsets

from api import retrievingTools
from api.ledgerUpdateApi import getConfig, getDevices
from api.serializers import UserSerializer, GroupSerializer
from .models import Application, Device
from django.core import serializers


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer



from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import Firmware
from api.serializers import FirmwareSerializer
from rest_framework.views import APIView


from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from api.permissions import IsAdminOrReadOnly


class FirmwareList(generics.ListCreateAPIView):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FirmwareDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)


def legacy_applications(request):
    response = retrievingTools.get_applications_legacy(request)
    return HttpResponse(json.dumps(response[1]),status_code = response[0], content_type = 'application/json')


def legacy_firmwares(request):
    response = retrievingTools.get_firmwares_legacy(request)
    return HttpResponse(json.dumps(response[1]),status_code = response[0], content_type = 'application/json')


def new_applications(request):
    response  = retrievingTools.get_new_app(request)
    return HttpResponse(json.dumps(response[1]),status_code = response[0], content_type = 'application/json')

'''
def manage_devices(request):
    devices = Device.objects.all()
    return render(request, 'api/manage_devices.html',{'devices':devices})


def manage_device(request,device_id):
    device = Device.objects.filter(id=device_id)[0]
    return render(request, 'api/manage_device.html',{'device':device})
'''

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


