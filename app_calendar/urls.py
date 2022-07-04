from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register(r'', MeetingsViewSet, basename='meeting')

urlpatterns = [
    path('', include(router.urls)),
]
