from __future__ import absolute_import, division, print_function, unicode_literals
from rest_framework.reverse import reverse
from rest_framework_swagger import renderers
from rest_framework.renderers import JSONRenderer


class MyRenderer(JSONRenderer):
    media_type = 'application/json'


class MyOpenAPIRenderer(renderers.OpenAPIRenderer):
    def get_customizations(self):
        data = super(MyOpenAPIRenderer, self).get_customizations()
        data['host'] = 'localhost:8000'
        return data


class JSONOpenAPIRenderer(MyOpenAPIRenderer):
    media_type = 'application/json'

