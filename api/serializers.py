from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Firmware, Device, Provider, ApplicationRelease, Application, FirmwareCompatibility, FirmwareDistribution

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class ApplicationReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationRelease
        fields = '__all__'

class FirmwareDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmwareDistribution
        fields = '__all__'

class FirmwareCompatibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmwareCompatibility
        fields = '__all__'
