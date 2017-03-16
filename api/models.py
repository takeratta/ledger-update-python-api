from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible  # only if you need to support Python 2

class Provider(models.Model):
    name = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=200)
    app_id = models.CharField(max_length=20)
    version = models.CharField(max_length=20)
    hash = models.CharField(max_length=200)
    target_id = models.CharField(max_length=200)
    minimum_firmware = models.ForeignKey(Firmware.firmware_version)
    maximum_firmware = models.ForeignKey(Firmware.firmware_version)  #possibly replace by 1 single manytomany relation
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    changelog = models.CharField(max_length=5000)
    provider = models.ManyToManyField(Provider,
                                      through='AppDistribution',
                                      through_fields=('app','provider'))
    def __str__(self):
        return self.name



class Firmware(models.Model):
    name = models.CharField(max_length=200)
    firm_id = models.CharField(max_length=20)
    firmware_version = models.CharField(max_length=20)
    hash = models.CharField(max_length=200)
    target_id = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    changelog = models.CharField(max_length=5000)
    provider = models.ManyToManyField(Provider,
                                      through='FirmwareDistribution',
                                      through_fields=('firmware','provider'))
    def __str__(self):
        return '%s %s' % (self.name, self.firmware_version)

class AppDistibution(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    production = models.BooleanField

class FirmawareDistibution(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    production = models.BooleanField