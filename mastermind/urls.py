"""mastermind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from django.conf.urls.static import static
from django.conf import settings
from commons.views import SwaggerSchemaView, DocumentationView

schema_view = get_schema_view(title='Mastermind API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/game/', include('game.urls')),
    path('api/documentation/', DocumentationView.as_view(
        extra_context={'schema_url': 'docu'}
    ), name='swagger-ui'),
    path('api/documentation/schema/', SwaggerSchemaView.as_view(), name='docu'),
]
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
