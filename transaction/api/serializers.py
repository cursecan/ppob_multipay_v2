from rest_framework import serializers

from transaction.models import (
    InstanSale, PpobSale
)

from product.api.serializers import ProductInfoSerializer
from userprofile.api.serializers import UserSimpleSerializer

from product.models import Product
from userprofile.models import Wallet

class InstanSaleSerializer(serializers.ModelSerializer):
    product = ProductInfoSerializer(read_only=True)
    create_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = InstanSale
        fields = [
            'id',
            'code',
            'customer', 'product',
            'price', 'commision',
            'create_by', 'closed'
        ]

class PpobSaleSerializer(serializers.ModelSerializer):
    product = ProductInfoSerializer(read_only=True)
    create_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = PpobSale
        fields = [
            'id',
            'code',
            'customer', 'product',
            'price', 'commision',
            'create_by', 'closed'
        ]


class PpobInquerySerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(write_only=True)
    customer_number = serializers.CharField(write_only=True)
    # customer_name = serializers.SerializerMethodField(read_only=True)
    customer_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PpobSale
        fields = [
            'id', 'code',
            # 'customer_name',
            'product_code', 'customer_number', 'customer_detail'
        ]
        read_only_fields = [
            'id', 'code',
            'customer_name',
        ]

    # def get_customer_name(self, obj):
    #     return obj.get_customer_name()

    def get_customer_detail(self, obj):
        return obj.get_customer_detail()

    def validate(self, data):
        prod_code = data.get('product_code')
        product_objs = Product.objects.filter(
            is_active=True, code=prod_code, type_product='QU'
        )
        if not product_objs.exists():
            raise serializers.ValidationError({
                'error': 'Product not found.'
            })
        return data

    def create(self, validated_data):
        user_obj = self.context.get('user')
        prod_code = validated_data.get('product_code')
        customer_num = validated_data.get('customer_number')

        product_obj = Product.objects.get(
            is_active=True, code=prod_code, type_product='QU'
        )

        ppob_sale = PpobSale.objects.create(
            product = product_obj, customer = customer_num,
            create_by = user_obj
        )
        ppob_sale.refresh_from_db()
        return ppob_sale


class PpobSaleCustomSerializer(PpobSaleSerializer):
    product_code = serializers.CharField(write_only=True)
    customer_number = serializers.CharField(write_only=True)
    inquery = serializers.CharField(write_only=True)

    class Meta(PpobSaleSerializer.Meta):
        fields = [
            'id',
            'code',
            'customer', 'product',
            'price', 'commision',
            'create_by', 'closed',
            'product_code', 'customer_number', 'inquery'
        ]
        read_only_fields = [
            'id',
            'code',
            'customer', 'product',
            'price', 'commision',
            'create_by', 'closed'
        ]

    def validate(self, data):
        prod_code = data.get('product_code')
        user_obj = self.context.get('user')
        inquery = data.get('inquery', None)
        
        product_objs = Product.objects.filter(
            is_active=True, code=prod_code, type_product='QU'
        )

        inquery_objs = PpobSale.objects.filter(
            code = inquery
        )
        if not inquery_objs.exists():
            raise serializers.ValidationError({
                'error': 'Inquery request not found.'
            })
        inquery_obj = inquery_objs.get()

        if not product_objs.exists():
            raise serializers.ValidationError({
                'error': 'Product not exists.'
            })

        product_obj = product_objs.get()

        if user_obj.profile.wallet.get_saldo() <  inquery_obj.price:
            unprice = inquery_obj.price - user_obj.profile.wallet.get_saldo()
            # JIKA USER PUNYA AGEN
            if user_obj.profile.agen.profile.user_type == 2: #2 = AGEN
                if user_obj.profile.wallet.limit < user_obj.profile.wallet.loan + unprice:
                    raise serializers.ValidationError({
                        'error': 'User loan on limit.'
                    })
                if user_obj.profile.agen.profile.wallet.saldo < unprice:
                    raise serializers.ValidationError({
                        'error': 'Saldo agen not enough.'
                    })
            else :
                raise serializers.ValidationError({
                    'error': 'Related agen not found.'
                })
        return data

    def create(self, validated_data):
        prod_code = validated_data.get('product_code')
        customer_num = validated_data.get('customer_number')
        inquery = validated_data.get('inquery', None)
        user_obj = self.context.get('user')

        product_obj = Product.objects.get(
            code = prod_code, is_active=True
        )

        inquery_obj = PpobSale.objects.get(
            code = inquery, sale_type = 'IN'
        )
        
        sale_obj = PpobSale.objects.create(
            product = product_obj,
            customer = customer_num,
            inquery = inquery_obj,
            create_by = user_obj
        )

        sale_obj.refresh_from_db()

        return sale_obj


class InstanSaleCustomSerializer(InstanSaleSerializer):
    product_code = serializers.CharField(write_only=True)
    customer_number = serializers.CharField(write_only=True)

    class Meta(InstanSaleSerializer.Meta):
        fields = [
            'id',
            'code',
            'customer', 'product',
            'price', 'commision',
            'create_by', 'closed',
            'product_code', 'customer_number'
        ]
        read_only_fields = [
            'id',
            'code',
            'customer', 'product',
            'price', 'commision',
            'create_by', 'closed'
        ]

    def validate(self, data):
        prod_code = data.get('product_code')
        user_obj = self.context.get('user')
        
        product_objs = Product.objects.filter(
            is_active=True, code=prod_code, type_product='IN'
        )

        if not product_objs.exists():
            raise serializers.ValidationError({
                'error': 'Product not exists.'
            })

        product_obj = product_objs.get()
        if user_obj.profile.wallet.get_saldo() <  product_obj.price:
            unprice = product_obj.price - user_obj.profile.wallet.get_saldo()
            if user_obj.profile.agen.profile.user_type == 2:
                if user_obj.profile.wallet.limit < user_obj.profile.wallet.loan + unprice:
                    raise serializers.ValidationError({
                        'error': 'User loan on limit.'
                    })
                if user_obj.profile.agen.profile.wallet.saldo < unprice:
                    raise serializers.ValidationError({
                        'error': 'Saldo agen not enough.'
                    })
            else :
                raise serializers.ValidationError({
                    'error': 'Related agen not found.'
                })
        return data

    def create(self, validated_data):
        prod_code = validated_data.get('product_code')
        customer_num = validated_data.get('customer_number')
        user_obj = self.context.get('user')

        product_obj = Product.objects.get(
            code = prod_code, is_active=True
        )
        instansale_obj = InstanSale.objects.create(
            product = product_obj,
            customer = customer_num,
            create_by = user_obj,
        )
        return instansale_obj