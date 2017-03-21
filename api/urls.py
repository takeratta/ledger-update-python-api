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
    #legacy support
    url(r'^update/firmwares', views.legacy_firmwares, name='legacy_firmwares'),
    url(r'^update/applications', views.legacy_applications, name='legacy_applications'),
    # end legacy support
    url(r'^firmwares/$', views.FirmwareList.as_view()),
    url(r'^firmwares/(?P<pk>[0-9]+)/$', views.FirmwareDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]