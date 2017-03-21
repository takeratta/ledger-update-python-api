from django.conf.urls import url,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


app_name = 'api'
urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #legacy support **********************
    url(r'^update/firmwares/$', views.legacy_firmwares, name='legacy_firmwares'),
    url(r'^update/applications/$', views.legacy_applications, name='legacy_applications'),
    #url(r'^update/install/$', views.legacy_install),
    #url(r'^update/uninstall/$', views.legacy_uninstall),
    # end legacy support ******************
    url(r'^firmwares/$', views.FirmwareList.as_view()),
    url(r'^firmwares/(?P<pk>[0-9]+)/$', views.FirmwareDetail.as_view()),
    url(r'^firmwareCompatibilities/$', views.FirmwareCompatibilityList.as_view()),
    url(r'^firmwareCompatibilities/(?P<pk>[0-9]+)/$', views.FirmwareCompatibilityDetail.as_view()),
    url(r'^applications/$', views.ApplicationList.as_view()),
    url(r'^applications/(?P<pk>[0-9]+)/$', views.ApplicationDetail.as_view()),
    url(r'^applicationReleases/$', views.ApplicationReleaseList.as_view()),
    url(r'^applicationReleases/(?P<pk>[0-9]+)/$', views.ApplicationReleaseDetail.as_view()),
    url(r'^firmwareDistributions/$', views.FirmwareDistributionList.as_view()),
    url(r'^firmwareDistributions/(?P<pk>[0-9]+)/$', views.FirmwareDistributionDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    #new api calls ***********************
    url(r'^get/new_applications/$', views.new_applications),
    url(r'^get/last_firmware/$', views.last_firmware),
    url(r'^get/app_updates/$', views.updatable_applications),
]