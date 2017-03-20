from api.models import Application,Provider,ApplicationRelease,Firmware,FirmwareDistribution
from django.db.models import Q

def get_new_app(firmware,installed_apps, ):
    compatible_apps =


def get_applications_legacy(request):
    try:
        provider = request.GET.get('provider',[''])[0]
        provider = Provider.models.filter(name=provider)
        data = {}
        applications = ApplicationRelease.objects.filter(legacy_flag=True)
        for app in applications:
            if provider in FirmwareDistribution.objects.filter(firmware=app.minimum_firmware,production=True):
                app_data = {}
                app_data['name'] = app.application.name
                app_data['identifier'] = app.application.identifier
                app_data['icon'] = app.application.icon
                app_data['version'] = app.version
                app_data['bolos_version']['min'] = app.minimum_firmware.version
                release_data={}
                release_data['hash']=app.hash
                release_data['perso']=app.perso
                release_data['target_id']=app.minimum_firmware.target_id
                release_data["firmware"] = app.firmware
                release_data["firmwareKey"] = app.firmwareKey
                app_data['app']=release_data
                data[app.minimum_firmware.target_id.name].append(app_data)
        code =200
    except:
        code=404
        data= {"error": "Provider: "+str(provider)+" not found"}
    return code,data

def get_firmwares_legacy(request):
    try:
        data = {}
        provider = request.GET.get('provider', [''])[0]
        provider = Provider.models.filter(name=provider)
        firmwares = Firmware.objects.filter(legacy_flag=True)
        for firm in firmwares:
            if provider in FirmwareDistribution.objects.filter(firmware=firm,production=True):
                firm_data = {}
                firm_data['name'] = firm.name
                firm_data['notes'] = firm.notes
                firm_data['identifier'] = firm.identifier
                firm_data['bolos_version']['min'] = firm.version
                osu_data={}
                osu_data['hash']=firm.hash_osu
                osu_data['perso']=firm.perso
                osu_data['target_id']=firm.target_id
                osu_data["firmware"] = firm.firmware_osu
                osu_data["firmwareKey"] = firm.firmwareKey_osu
                final_data = {}
                final_data['perso'] = firm.perso
                final_data['target_id'] = firm.target_id
                final_data["firmware"] = firm.firmware_final
                final_data["firmwareKey"] = firm.firmwareKey_final
                firm_data['osu']=osu_data
                firm_data['final']=final_data
                data[firm.minimum_firmware.target_id.name].append(firm_data)
        code =200
    except:
        code=404
        data= {"error": "Provider: "+str(provider)+" not found"}
    return code,data



