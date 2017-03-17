from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible  # only if you need to support Python 2

class Provider(models.Model):
    name = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=200)
    target_id = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Firmware(models.Model):
    name = models.CharField(max_length=200)
    #firm_id = models.CharField(max_length=20)
    firmware_version = models.CharField(max_length=20)
    hash = models.CharField(max_length=200)
    target_id = models.ForeignKey(Device)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    changelog = models.CharField(max_length=5000)
    provider = models.ManyToManyField(Provider,
                                      through='FirmwareDistribution',
                                      through_fields=('firmware','provider'),
                                      blank=True,
                                      null=True)
    def __str__(self):
        return '%s %s' % (self.name, self.firmware_version)

class Application(models.Model):
    name = models.CharField(max_length=200)
    #app_id = models.CharField(max_length=20)
    version = models.CharField(max_length=20)
    hash = models.CharField(max_length=200)
    minimum_firmware = models.ForeignKey(Firmware, related_name='min_version')
    maximum_firmware = models.ForeignKey(Firmware, related_name='max_version', blank=True, null=True)  #possibly replace by 1 single manytomany relation
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    changelog = models.CharField(max_length=5000)
    '''provider = models.ManyToManyField(Provider,
                                      through='AppDistribution',
                                      through_fields=('app','provider'),
                                      blank=True,
                                      null=True)'''
    def __str__(self):
        return self.name


'''class AppDistribution(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    production = models.BooleanField
    def __str__(self):
        return 'production state: %s for %s' % (self.production, self.app.name)
'''
class FirmwareDistribution(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    production = models.BooleanField
    def __str__(self):
        return 'production state: %s for %s' % (self.production, self.firmware.name)
