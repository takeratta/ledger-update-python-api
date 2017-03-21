import json
from api import retrievingTools
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from rest_framework.response import Response
from api.models import Firmware, FirmwareDistribution, FirmwareCompatibility, ApplicationRelease, Application
from api.serializers import FirmwareSerializer,FirmwareCompatibilitySerializer,FirmwareDistributionSerializer, ApplicationReleaseSerializer,ApplicationSerializer
from rest_framework import generics
from rest_framework import permissions
from api.permissions import IsAdminOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.core import serializers


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('firmware-list', request=request, format=format)
    })





class FirmwareList(generics.ListCreateAPIView):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ApplicationList(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ApplicationReleaseList(generics.ListCreateAPIView):
    queryset = ApplicationRelease.objects.all()
    serializer_class = ApplicationReleaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FirmwareDistributionList(generics.ListCreateAPIView):
    queryset = FirmwareDistribution.objects.all()
    serializer_class = FirmwareDistributionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FirmwareCompatibilityList(generics.ListCreateAPIView):
    queryset = FirmwareCompatibility.objects.all()
    serializer_class = FirmwareCompatibilitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FirmwareDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)


class ApplicationReleaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationRelease.objects.all()
    serializer_class = ApplicationReleaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)


class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)


class FirmwareDistributionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FirmwareDistribution.objects.all()
    serializer_class = FirmwareDistributionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)


class FirmwareCompatibilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FirmwareCompatibility.objects.all()
    serializer_class = FirmwareCompatibilitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)


def legacy_applications(request):
    response = retrievingTools.get_applications_legacy(request)
    return HttpResponse(json.dumps(response[1]),status_code = response[0], content_type = 'application/json')


def legacy_firmwares(request):
    response = retrievingTools.get_firmwares_legacy(request)
    return HttpResponse(json.dumps(response[1]),status_code = response[0], content_type = 'application/json')


def updatable_applications(request):
    response  = retrievingTools.get_updatable_app(request)
    return HttpResponse(serializers.serialize('json',response[1]),status_code = response[0], content_type = 'application/json')


def new_applications(request):
    response  = retrievingTools.get_new_app(request)
    return HttpResponse(serializers.serialize('json',response[1]),status_code = response[0], content_type = 'application/json')


def last_firmware(request):
    response  = retrievingTools.get_last_firmware(request)
    return HttpResponse(serializers.serialize('json',response[1]),status_code = response[0], content_type = 'application/json')

'''
def manage_devices(request):
    devices = Device.objects.all()
    return render(request, 'api/manage_devices.html',{'devices':devices})


def manage_device(request,device_id):
    device = Device.objects.filter(id=device_id)[0]
    return render(request, 'api/manage_device.html',{'device':device})
'''

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
