from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer
from .models import User
from rest_framework import exceptions, permissions, status, viewsets
from django.http import HttpRequest
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
import logging
import jwt


jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class UsersViewset(viewsets.ModelViewSet):
    """
    retrieve:
        Return a user instance.

    list:
        Return all users, ordered by most recently joined.

    create:
        Create a new user.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginViewSet(ObtainJSONWebToken):
    """
    post:
        JWT login.
    """
    queryset = User.objects.filter(is_active=True)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = {
            "success":False,
            "result":"",
            "message":""
        }

        try:

            if request.data.get('username') is None or request.data.get('password') is None:
                raise User.DoesNotExist()

            try:
                data_login =  {
                    "username": request.data.get('username'),
                    "password": request.data.get('password')
                }
                REQ = HttpRequest()
                REQ.data = data_login
                r = super().post(REQ)
                token_user = r.data
                if r.status_code==200:
                    data['success'] = True
                    data['result'] = token_user
                if r.status_code>=400:
                    data['message'] = token_user['non_field_errors']
            except:
                raise User.DoesNotExist()

        except User.DoesNotExist:
            data['message'] = "USER_NOT_EXIST"
        except Exception as e:
            logging.warning(str(e))

        if not data['success']:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
