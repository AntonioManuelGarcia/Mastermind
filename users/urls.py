from django.urls import path  # , include
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
# from django.contrib import admin
from .views import UsersViewset, LoginViewSet, RegisterView
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('User', UsersViewset)


urlpatterns = [

    path('auth/login/', LoginViewSet.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('auth/change-password/', auth_views.PasswordChangeView.as_view(success_url='localhost:8000')),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]