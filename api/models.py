from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible  # only if you need to support Python 2

class Provider(models.Model):
    name = models.CharField(max_length=200)
    #provider_id = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=200)
    target_id = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Firmware(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=20)
    notes = models.CharField(max_length=5000)
    perso = models.CharField(max_length=200)
    firmware_osu = models.CharField(max_length=200)
    firmwareKey_osu = models.CharField(max_length=200)
    hash_osu = models.CharField(max_length=200)
    firmware_final = models.CharField(max_length=200)
    firmwareKey_final = models.CharField(max_length=200)
    hash_final = models.CharField(max_length=200)
    firmware_version = models.CharField(max_length=20)
    target_id = models.ForeignKey(Device)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    provider = models.ManyToManyField(Provider,
                                      through='FirmwareDistribution',
                                      through_fields=('firmware','provider'),
                                      blank=True,
                                      null=True)
    def __str__(self):
        return '%s %s' % (self.name, self.firmware_version)

class ApplicationRelease(models.Model):
    application = models.ForeignKey(Application)
    version = models.CharField(max_length=20)
    hash = models.CharField(max_length=200)
    minimum_firmware = models.ForeignKey(Firmware)
    maximum_firmware = models.ForeignKey(Firmware, blank=True)  #possibly replace by 1 single manytomany relation
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    changelog = models.CharField(max_length=5000)
    firmware = models.CharField(max_length=200)
    firmwareKey = models.CharField(max_length=200)
    perso = models.CharField(max_length=50)
    legacy_flag = models.NullBooleanField
    compatible_firmwares= models.ManyToManyField(Firmware,
                                      through='FirmwareCompatibility',
                                      through_fields=('app','firmware'))
    def __str__(self):
        return '%s %s' % (self.application.name, self.version)

class Application(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=50)
    #icon ....
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

class FirmwareCompatibility(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    app = models.ForeignKey(ApplicationRelease, on_delete=models.CASCADE)
    production = models.BooleanField
    def __str__(self):
        return 'app production state: %s for %s' % (self.production, self.firmware.name)

