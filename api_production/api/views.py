from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api_production.models import ProductVersion
from .serializers import *


class ProductVersionApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        product = ProductVersion.objects.latest('timestamp')
        serializers = ProductVersionSerializer(product)

        return Response(serializers.data)
