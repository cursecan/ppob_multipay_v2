from rest_framework import serializers

from witdraw.models import Witdraw

MIN_COMMISION = 10000
class WitdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Witdraw
        fields = [
            'id', 'amount'
        ]
        read_only_fields = [
            'id'
        ]

    def validate(self, data):
        amount = data.get('amount')
        user = self.context.get('user')

        if user.profile.user_type != 2:
            raise serializers.ValidationError({
                'error': 'User not an agen'
            })
        
        if user.profile.ponsel is None or user.profile.ponsel == '':
            raise serializers.ValidationError({
                'error': 'Ponsel cannot be empty.'
            })

        if user.profile.wallet.commision < MIN_COMMISION:
            raise serializers.ValidationError({
                'error': 'Commision wallet not enought.'
            })

        if amount < MIN_COMMISION:
            raise serializers.ValidationError({
                'error': 'Minimal amount 10.000'
            })

        return data

    def create(self, validated_data):
        amount = validated_data.get('amount')
        user = self.context.get('user')

        withdraw_obj = Witdraw.objects.create(
            create_by = user,
            amount = amount
        )

        return withdraw_obj