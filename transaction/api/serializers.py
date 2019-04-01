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


# PPOB Transaksi Inquery Serializer 1
class PpobInquerySerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(write_only=True)
    customer_number = serializers.CharField(write_only=True)
    customer_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PpobSale
        fields = [
            'id', 'code',
            'product_code', 'customer_number', 'customer_detail'
        ]
        read_only_fields = [
            'id', 'code',
            'customer_name',
        ]

    def get_customer_detail(self, obj):
        return obj.get_customer_detail()

    def validate(self, data):
        prod_code = data.get('product_code')
        
        # Filter produk aktif & ppob
        product_objs = Product.objects.filter(
            is_active=True, code=prod_code, type_product='QU'
        )
        if not product_objs.exists():
            # Jika produk tidak aktif / tidak ditemukan
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


# PPOB Transaksi Payment Serializer Ext.1
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

        # Transaksi PPOB payment harus memiliki Inquery Code
        inquery_objs = PpobSale.objects.filter(
            code = inquery
        )
        if not inquery_objs.exists():
            # Retur error jika inquery tidak ada
            raise serializers.ValidationError({
                'error': 'Inquery request not found.'
            })
        inquery_obj = inquery_objs.get()

        # Produk hasu aktif & type query ppob
        product_objs = Product.objects.filter(
            is_active=True, code=prod_code, type_product='QU'
        )
        if not product_objs.exists():
            # Return error jika produk tidak aktif / ditemukan
            raise serializers.ValidationError({
                'error': 'Product not exists.'
            })

        # Spesifik produk obj
        product_obj = product_objs.get()
        price_product = product_obj.price
        if price_product == 0 :
            # Jika price 0, artinya harga diambil dari inquery produknya
            price_product = inquery_obj.responseppobsale.get_price()

        
        # Filter jika saldo tidak cukup
        cur_saldo = user_obj.profile.wallet.get_saldo()
        if  cur_saldo <  price_product:
            unprice = price_product - cur_saldo
            
            # Jika terdaftar menggunakan Agen
            # User_type 2 artinya ada agennya
            if user_obj.profile.agen.profile.user_type == 2:
                cur_limit = user_obj.profile.wallet.limit
                cur_loan = user_obj.profile.wallet.get_loan()

                # Cek jika total utang sudah melebihi limit yang diberikan
                if cur_limit < cur_loan + unprice:
                    raise serializers.ValidationError({
                        'error': 'User loan on limit.'
                    })

                # Jika user adalah agan itu sendiri, tidak diizinkan mengutang pada diri sendiri
                if user_obj == user_obj.profile.agen:
                    raise serializers.ValidationError({
                        'error': 'Saldo user not enough.'
                    })
                else:
                    # Cek jika saldo Agen sudah tidak mencukupi unutk membayar tagihan membernya
                    if user_obj.profile.agen.profile.wallet.get_saldo() < unprice:
                        raise serializers.ValidationError({
                            'error': 'Saldo agen not enough.'
                        })
            else :
                # User tidak memiliki Agen
                raise serializers.ValidationError({
                    'error': 'Related agen not found.'
                })

        return data

    def create(self, validated_data):
        prod_code = validated_data.get('product_code')
        customer_num = validated_data.get('customer_number')
        inquery = validated_data.get('inquery', None)
        user_obj = self.context.get('user')

        # Product Obj
        product_obj = Product.objects.get(
            code = prod_code, is_active=True
        )

        # Inquery Obj
        inquery_obj = PpobSale.objects.get(
            code = inquery, sale_type = 'IN'
        )
        
        # Create sale obj / transaksi
        # Penctatan utang / kurang bayar diprocess triger PpobSale
        sale_obj = PpobSale.objects.create(
            product = product_obj,
            customer = customer_num,
            inquery = inquery_obj,
            create_by = user_obj
        )

        sale_obj.refresh_from_db()

        return sale_obj


# Inputer Instan Sale Serializer
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
        
        # Produk terdaftar & aktif
        product_objs = Product.objects.filter(
            is_active=True, code=prod_code, type_product='IN'
        )

        if not product_objs.exists():
            raise serializers.ValidationError({
                'error': 'Product not exists.'
            })

        product_obj = product_objs.get()

        # Pengecekan saldo user
        cur_saldo = user_obj.profile.wallet.get_saldo()
        
        # Saldo tidak cukup
        if cur_saldo <  product_obj.price:
            unprice = product_obj.price - cur_saldo

            # Type user 2 memiliki Agen
            if user_obj.profile.agen.profile.user_type == 2:
                cur_limit = user_obj.profile.wallet.limit
                cur_loan = user_obj.profile.wallet.get_loan()

                # Cek jika user loan melebihi limit yg diberikan
                if cur_limit < cur_loan + unprice:
                    raise serializers.ValidationError({
                        'error': 'User loan on limit.'
                    })

                # Tidak berlaku jika user sendiri adalah Agen
                if user_obj == user_obj.profile.agen:
                    raise serializers.ValidationError({
                        'error': 'Saldo user not enough.'
                    })

                else:
                    # Cek jika saldo agen masih mencukupi
                    if user_obj.profile.agen.profile.wallet.get_saldo() < unprice:
                        raise serializers.ValidationError({
                            'error': 'Saldo agen not enough.'
                        })

            # Jika user tidak memiliki agen
            else :
                raise serializers.ValidationError({
                    'error': 'Related agen not found.'
                })
        return data

    def create(self, validated_data):
        prod_code = validated_data.get('product_code')
        customer_num = validated_data.get('customer_number')
        user_obj = self.context.get('user')

        # Produk obj
        product_obj = Product.objects.get(
            code = prod_code, is_active=True
        )

        # Sale produk / Transaksi
        # Proces utang / loan dilakukan triger Instan Sale
        instansale_obj = InstanSale.objects.create(
            product = product_obj,
            customer = customer_num,
            create_by = user_obj,
        )
        return instansale_obj