from django.urls import path, include
from rest_framework import routers 
from .views import ListingView

router = routers.DefaultRouter()
router.register(r'listings', ListingView, basename='listings')
#router.register(r'Search', SearchView)

urlpatterns = [
    path('',include(router.urls)),
    
]

