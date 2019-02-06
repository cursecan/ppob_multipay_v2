from rest_framework import serializers

from product.models import (
    Product, Operator, Group, Prefix
)


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = [
            'id',
            'code', 'operator_name'
        ]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'code', 'group_name'
        ]

class ProductSerializer(serializers.ModelSerializer):
    operator = OperatorSerializer()
    group = GroupSerializer()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'code', 'product_name',
            'operator', 'group',
            'nominal', 'price', 'commision',
            'is_active'
        ]