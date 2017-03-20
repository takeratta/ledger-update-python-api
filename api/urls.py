from django.conf.urls import url,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


app_name = 'api'
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^devices/$', views.manage_devices, name='manage_devices'),
    url(r'^device/(?P<device_id>[0-9]+)/$',views.manage_device, name='manage_device'),
    #legacy support
    url(r'^update/firmwares', views.legacy_firmwares, name='legacy_firmwares'),
    url(r'^update/applications', views.legacy_applications, name='legacy_applications'),
    url(r'^applications', views.applications, name='list_applications'),
    url(r'^firmwares/$', views.firmware_list),
    url(r'^firmwares/(?P<pk>[0-9]+)/$', views.firmware_detail),
]