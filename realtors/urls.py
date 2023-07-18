from django.urls import path, include
from rest_framework import routers
from .views import RealtorViewSet

router = routers.DefaultRouter()
router.register(r'realtors', RealtorViewSet, basename='realtor')

urlpatterns = [
    path('',include(router.urls)),
]
