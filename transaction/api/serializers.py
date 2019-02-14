from rest_framework import serializers

from transaction.models import InstanSale
from product.models import Product
from userprofile.models import Wallet

class InstanSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanSale
        fields = [
            'id',
            'code',
            'customer', 'product',
            'price', 'commision',
            'create_by', 'closed'
        ]



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
            is_active=True, code=prod_code
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