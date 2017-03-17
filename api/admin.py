from django.contrib import admin

# Register your models here.
from .models import Provider
from .models import Device
from .models import Application
from .models import Firmware
from .models import FirmwareDistribution

admin.site.register(Device)
admin.site.register(Firmware)
admin.site.register(FirmwareDistribution)
admin.site.register(Provider)
admin.site.register(Application)