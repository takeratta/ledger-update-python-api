from api.models import Firmware, FirmwareDistribution, ApplicationRelease, Application, FirmwareCompatibility
from django.core.exceptions import ValidationError


def add_support(release,firmware, production=False):
    try:
        app = ApplicationRelease.objects.get(hash=release)
        firmware = Firmware.objects.get(hash_final=firmware)
        new=FirmwareCompatibility(firmware=firmware,app=app,production=production)
        new.full_clean()
        new.save()
    except:
        return False
    return True