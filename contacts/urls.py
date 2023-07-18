from django.urls import include, path
from rest_framework import routers
from .views import ContactViewSet

router = routers.DefaultRouter()
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    # Other URL patterns for your project
    path('', include(router.urls)),
]
