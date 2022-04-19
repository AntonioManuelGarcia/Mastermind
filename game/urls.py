from django.urls import path  # , include
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
# from django.contrib import admin
from .views import *
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('Boardgame', BoardGameViewset)
router.register('Guest',GuestViewset)
router.register('Game', GameViewset)

urlpatterns = [
    path('', include(router.urls)),
]
