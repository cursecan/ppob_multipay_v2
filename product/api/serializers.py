from rest_framework import serializers

from product.models import (
    Product, Operator, Group, Prefix
)


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = [
            'id',
            'code', 'operator_name', 'hint'
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

class ProductAgenSerializer(serializers.ModelSerializer):
    operator = OperatorSerializer()
    group = GroupSerializer()
    price = serializers.SerializerMethodField()
    commision = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'code', 'product_name',
            'operator', 'group',
            'nominal', 'price', 'commision',
            'is_active'
        ]

    def get_price(self, obj):
        return obj.agen_price()

    def get_commision(self, obj):
        return obj.agen_commision()


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'code', 'product_name',
        ]