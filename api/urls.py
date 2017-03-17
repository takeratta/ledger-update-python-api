from django.conf.urls import url

from . import views
app_name = 'api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^devices/$', views.manage_devices, name='manage_devices'),
    url(r'^device/(?P<device_id>[0-9]+)/$',views.manage_device, name='manage_device'),
    #legacy support
    url(r'^update/firmwares', views.legacy_firmwares, name='legacy_firmwares'),
    url(r'update/applications', views.legacy_applications, name='legacy_applications'),
    url(r'update/devices', views.legacy_devices, name='legacy_devices'),
]