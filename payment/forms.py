from django import forms

from .models import (
    LoanPayment, Bank
)


class LoanPaymentForm(forms.ModelForm):
    class Meta:
        model = LoanPayment
        fields = '__all__'


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = [
            'bank_code', 'bank_name'
        ]

    def clean_bank_code(self):
        return self.cleaned_data['bank_code'].upper()

    def clean_bank_name(self):
        return self.cleaned_data['bank_name'].upper()