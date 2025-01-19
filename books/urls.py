from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'', BookViewSet, basename='book')



urlpatterns = [
    path('search/', SearchViewSet.as_view({'get': 'list'}), name='search'),
    path('', include(router.urls)),

]