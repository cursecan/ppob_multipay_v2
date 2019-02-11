from django.contrib.auth.models import User
from rest_framework import serializers

from userprofile.models import (
    Profile, Wallet
)

class UserSerializer(serializers.ModelSerializer):
    saldo = serializers.DecimalField(
        max_digits=12, decimal_places=2, 
        source='profile.wallet.get_saldo', read_only=True
    )
    commision = serializers.DecimalField(
        max_digits=12, decimal_places=2, 
        source='profile.wallet.commision', read_only=True
    )
    limit = serializers.DecimalField(
        max_digits=12, decimal_places=2, 
        source='profile.wallet.limit', read_only=True
    )
    loan = serializers.DecimalField(
        max_digits=12, decimal_places=2, 
        source='profile.wallet.loan', read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name', 'last_name',
            'saldo', 'commision', 'limit', 'loan',
        ]


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    agen = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 
            'guid',
            'user', 'agen',
            'user_type',
        ]

    def get_user(self, obj):
        return obj.get_username()

    def get_agen(self, obj):
        return obj.get_username()


class WalletSerializer(serializers.ModelSerializer):
    saldo = serializers.SerializerMethodField(read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = [
            'id',
            'profile',
            'saldo', 'commision', 'loan', 'limit'
        ]

    def get_saldo(self, obj):
        return obj.get_saldo()