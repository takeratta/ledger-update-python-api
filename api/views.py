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


#class based
from django.http import Http404



@api_view(['GET','POST'])
def firmware_list(request):
    """
    List all firmware, or create a new firmware.
    """
    if request.method == 'GET':
        firmwares = Firmware.objects.all()
        serializer = FirmwareSerializer(firmwares, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FirmwareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def firmware_detail(request, pk):
    """
    Retrieve, update or delete a  firmware.
    """
    try:
        firmware = Firmware.objects.get(pk=pk)
    except Firmware.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FirmwareSerializer(firmware)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FirmwareSerializer(firmware, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        firmware.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


