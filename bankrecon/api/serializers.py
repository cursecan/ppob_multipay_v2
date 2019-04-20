from bankrecon.models import (
    Bank, BankAccount, Catatan
)

from rest_framework.serializers import ModelSerializer


class BankSerializer(ModelSerializer):
    class Meta:
        model = Bank
        fields = [
            'id',
            'bank_name', 'bank_code'
        ]



class BankAccountSerializer(ModelSerializer):
    bank = BankSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = [
            'id', 
            'account', 'name',
            'bank',
            'how_to',
        ]


class CatatanSerializer(ModelSerializer):
    class Meta:
        model = Catatan
        fields = [
            'id', 
            'nomor', 'keterangan'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        nomor = validated_data.get('nomor')
        ket = validated_data.get('keterangan')
        create_by = self.context.get('user')

        catatan_obj = Catatan.objects.create(
            nomor = nomor, keterangan=ket,
            create_by = create_by
        )
        return catatan_obj