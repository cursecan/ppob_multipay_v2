from rest_framework import serializers

from billing.models import (
    BillingRecord,
    LoanRecord, ProfitRecord, CommisionRecord
)
from userprofile.api.serializers import UserSimpleSerializer


class BillingRecordSerializer(serializers.ModelSerializer):
    transaction = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = BillingRecord
        fields = [
            'id',
            'debit', 'credit', 'balance',
            'transaction',
            'status',
            'user'
        ]

    def get_transaction(self, obj):
        return obj.get_api_trx()

    def get_status(self, obj):
        return obj.get_api_status()