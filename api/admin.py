from django.contrib import admin
from django.utils.html import format_html
from imagekit.admin import AdminThumbnail

# Register your models here.

import models

admin.site.register(models.View)

class DeviceAdmin(admin.ModelAdmin):
	filter_horizontal = ("views",)

class VersionAdmin(admin.ModelAdmin):
	filter_horizontal = ("views", "devices", )
	def compatible_devices(self, obj):
		return ", ".join(list(str(device) for device in obj.devices.all()))
	list_display = ('app', '__str__', 'compatible_devices')
	list_filter = (
        'app', 'devices'
    )

class FirmwareAdmin(admin.ModelAdmin):
	filter_horizontal = ("views",)

class AppAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'icon_thumbnail')
	fields = ('icon_preview', 'name', 'category', 'icon')
	readonly_fields = ('icon_preview', )
	list_filter = (
        'category',
    )
	def icon_thumbnail(self, obj):
		return format_html("<img src=\"" + obj.icon.url + '" width="20" height="20"/>')

	def icon_preview(self, obj):
		return format_html("<img src=\"" + obj.icon.url + '"/>')


admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.Version, VersionAdmin)
admin.site.register(models.Firmware, FirmwareAdmin)
admin.site.register(models.App, AppAdmin)
admin.site.register(models.Category)
