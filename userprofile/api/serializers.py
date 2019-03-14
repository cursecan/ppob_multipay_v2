from django.contrib.auth.models import User
from django.db import transaction
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
    guid = serializers.CharField(
        source='profile.guid', read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'guid',
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
        return obj.get_agen()


class WalletSerializer(serializers.ModelSerializer):
    saldo = serializers.SerializerMethodField(read_only=True)
    profile = ProfileSerializer(read_only=True)

    new_limit = serializers.DecimalField(max_digits=12, decimal_places=0, write_only=True)

    class Meta:
        model = Wallet
        fields = [
            'id',
            'profile',
            'saldo', 'commision', 'loan', 'limit',
            'new_limit',
        ]
        read_only_fields = [
            'id',
            'profile',
            'saldo', 'commision', 'loan', 'limit'
        ]

    def get_saldo(self, obj):
        return obj.get_saldo()

    def update(self, instance, validated_data):
        instance.limit = validated_data.get('new_limit')
        instance.save()
        return instance


class SimpleSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    ponsel = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        ponsel = data.get('ponsel')
        if User.objects.filter(username=email).exists():
            raise serializers.ValidationError({
                'error': 'This email address already taken.' 
            })
        if Profile.objects.filter(ponsel=ponsel).exists():
            raise serializers.ValidationError({
                'error': 'This ponsel already taken.'
            })
        return data


class CustomSignupSerializer(SimpleSignUpSerializer, serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user', 'ponsel',
            'email', 'first_name', 'last_name', 'password'
        ]
        read_only_fields = [
            'id',
            'user'
        ]

    def validate(self, data):
        super(CustomSignupSerializer, self).validate(data)
        agen = self.context.get('user', None)

        # Only agen input
        if agen:
            if agen.profile.user_type != 2:
                raise serializers.ValidationError({
                    'error': 'Permision for agen only.'
                })

        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        ponsel = validated_data.get('ponsel')
        password = validated_data.get('password')

        agen = self.context.get('user', None)

        user_obj = User.objects.create_user(
            email, email, password, first_name=first_name, last_name=last_name, is_active=False
        )
        user_obj.profile.ponsel = ponsel

        # Only agen input
        if agen:
            user_obj.profile.agen = agen
            user_obj.profile.user_type = 1

        user_obj.profile.save()

        return user_obj.profile




