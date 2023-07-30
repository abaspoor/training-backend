from . import views
from .views import GroupViewset , EventViewset, UserViewSet, UserProfileViewset, MemberViewset
from django.conf.urls import include
from rest_framework import routers
from django.urls import path,re_path
# from rest_framework.authtoken.views import obtain_auth_token

router  = routers.DefaultRouter()
router.register(r'groups', GroupViewset)
router.register(r'events', EventViewset)
router.register(r'users', UserViewSet)
router.register(r'profile', UserProfileViewset)
router.register(r'members', MemberViewset)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('authenticate/', views.CustomObtainAuthTooken.as_view())
]