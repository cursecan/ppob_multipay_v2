from rest_framework import serializers

from payment.models import (
    Payment, LoanPayment
)
from userprofile.api.serializers import UserSimpleSerializer


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'user',
            'balance',
            'timestamp'
        ]
    
    def get_balance(self, obj):
        return obj.get_balance()