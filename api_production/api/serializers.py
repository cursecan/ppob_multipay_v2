from rest_framework.serializers import ModelSerializer

from api_production.models import ProductVersion


class ProductVersionSerializer(ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = [
            'version', 'description'
        ]