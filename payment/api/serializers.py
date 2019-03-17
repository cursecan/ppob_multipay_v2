from rest_framework import serializers
from userprofile.models import Profile
from userprofile.api.serializers import UserSimpleSerializer

from payment.models import (
    Payment, LoanPayment, Transfer
)
from billing.models import LoanRecord

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


class FlagSerializer(serializers.Serializer):
    guid = serializers.CharField(write_only=True)
    nominal = serializers.DecimalField(max_digits=12, decimal_places=0, write_only=True)

    def validate(self, data):
        guid = data.get('guid')
        nominal = data.get('nominal')
        sender = self.context.get('user') # Sender / Agen

        profile_obj = Profile.objects.filter(guid=guid)
        if not profile_obj.exists():
            raise serializers.ValidationError({
                'error': 'User not found.' 
            })

        if not sender.is_superuser:
            loan_objs = LoanRecord.objects.filter(
                user = profile_obj.get().user,
                agen = sender,
                record_type = 'LO',
                is_paid = False,
                is_delete = False
            )
            v = 0
            for i in loan_objs:
                v += i.get_loan_residu()

            if v == 0 :
                raise serializers.ValidationError({
                    'error': 'User does not have loan to flag.'
                })
            
            if v < nominal:
                raise serializers.ValidationError({
                    'error': 'Nominal must less or equal {}'.format(v) 
                })

        return data

class LoanPaymentSerializer(FlagSerializer ,serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = LoanPayment
        fields = [
            'id',
            'user',
            'amount',
            'guid',
            'nominal',
        ]

        read_only_fields = [
            'id',
            'user',
            'amount',
        ]

    
    def create(self, validated_data):
        guid = validated_data.get('guid')
        amount = validated_data.get('nominal')
        sender = self.context.get('user') # Sender / Agen
       

        profile_obj = Profile.objects.get(guid=guid)

        loan_obj = LoanPayment()
        loan_obj.user = profile_obj.user
        loan_obj.sender = sender
        loan_obj.amount = amount
        if sender.is_superuser:
            loan_obj.virtual_cash = True

        loan_obj.save()
        return loan_obj


class TransferSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(write_only=True)

    class Meta:
        model = Transfer
        fields = [
            'id',
            'sender', 'receiver',
            'amount', 'guid',
            'timestamp'
        ]
        read_only_fields = [
            'id',
            'sender', 'receiver',
            'timestamp'
        ]

    def validate(self, data):
        sender = self.context.get('sender')
        amount = data.get('amount')
        guid = data.get('guid')

        receive_profile = Profile.objects.filter(
            guid = guid
        )
        if not receive_profile.exists():
            raise serializers.ValidationError({
                'error': 'Receiver canot be found.'
            })

        if receive_profile.get().agen != sender:
            raise serializers.ValidationError({
                'error': 'Valid for its agen or admin only.'
            })
            
        if receive_profile.get().user == sender:
            raise serializers.ValidationError({
                'error': 'Cannot transfer to self account.'
            })

        if receive_profile.get().wallet.loan != 0:
            raise serializers.ValidationError({
                'error': 'User loan must be clean.'
            })

        if amount < 1:
            raise serializers.ValidationError({
                'error': 'Amount has to larger than 0.'
            })

        if amount > sender.profile.wallet.saldo:
            raise serializers.ValidationError({
                'error': 'Your saldo not enought to trasfer.'
            })

        return data

    def create(self, validated_data):
        sender = self.context.get('sender')
        guid = validated_data.get('guid')
        amount = validated_data.get('amount')

        receiver = Profile.objects.get(guid=guid)

        transfer_obj = Transfer.objects.create(
            sender = sender,
            receiver = receiver.user,
            amount = amount
        )
        return transfer_obj

