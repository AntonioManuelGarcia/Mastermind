from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from django.shortcuts import render
from .renderers import MyOpenAPIRenderer, MyRenderer, JSONOpenAPIRenderer
from django.views.generic import TemplateView
from rest_framework.schemas import AutoSchema


class DocumentationView(TemplateView):  
    template_name = "swagger-ui.html"


class SwaggerSchemaView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    permission_classes = [AllowAny]
    renderer_classes = [
        MyOpenAPIRenderer,
        JSONOpenAPIRenderer,
    ]

    def get(self, request):
        generator = SchemaGenerator(title='API DOCUMENTATION', url="/")
        schema = generator.get_schema(request=request)
        if not schema:
            raise exceptions.ValidationError(
                'The schema generator did not return a schema Document'
            )
        return Response(schema)
