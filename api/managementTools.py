from api.models import Firmware, FirmwareDistribution, ApplicationRelease, Application, FirmwareCompatibility
from django.core.exceptions import ValidationError



def add_firmware(data):
    new_firmware = Firmware(data)
    #MAYBE : include some automatic field completion
    try:
        new_firmware.full_clean()
    except ValidationError as e:
        return e.message_dict
    try:
        new_firmware.save()
    except:
        return False
    return True


def add_app_release(data):
    new_release = ApplicationRelease(data)
    #MAYBE : include some automatic field completion
    try:
        new_release.full_clean()
    except ValidationError as e:
        return e.message_dict
    try:
        new_release.save()
    except:
        return False
    return True


def add_application(data):
    new = Application(data)
    #MAYBE : include some automatic field completion
    try:
        new.full_clean()
    except ValidationError as e:
        return e.message_dict
    try:
        new.save()
    except:
        return False
    return True


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
