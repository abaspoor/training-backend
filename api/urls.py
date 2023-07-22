from .views import GroupViewset , EventViewset
from django.conf.urls import include
from rest_framework import routers
from django.urls import path,re_path

router  = routers.DefaultRouter()
router.register(r'groups', GroupViewset)
router.register(r'events', EventViewset)

urlpatterns = [
    re_path(r'^', include(router.urls)),
]