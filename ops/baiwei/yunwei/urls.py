#coding=utf-8
from django.conf.urls import patterns, url,include
from yunwei import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view()

router = DefaultRouter()
router.register(r'AESSLIST', views.AESSLISTViewSet)



urlpatterns = patterns('',
    url(r'^swagger/', schema_view),
    url(r'^api/', include(router.urls)),

    url(r'api/deploy$',views.deploy),
    url(r'api/deployResoult$',views.deployResoult),
)
