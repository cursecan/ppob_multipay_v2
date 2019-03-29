from django import forms

from .models import (
    InstanSale, PpobSale, RefundRequest
)
from product.models import Product

class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = [
            'intstan_trx',
            'comment',
        ]

    def __init__(self, *args, **kwargs):
        super(RefundRequestForm, self).__init__(*args, **kwargs)
        self.fields['intstan_trx'].queryset = InstanSale.objects.filter(closed=False)


class InstanSaleForm(forms.ModelForm):
    class Meta:
        model = InstanSale
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InstanSaleForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(
            type_product='IN'
        )

    def clean_product(self):
        product = self.cleaned_data['product']
        if product.is_delete:
            raise forms.ValidationError('This product has been delete.')
        if not product.is_active:
            raise forms.ValidationError('This product is not active.')
        return product


class PpobSaleForm(forms.ModelForm):
    class Meta:
        model = PpobSale
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PpobSaleForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(
            type_product='QU'
        )

    def clean_product(self):
        product = self.cleaned_data['product']
        if product.is_delete:
            raise forms.ValidationError('This product has been delete.')
        if not product.is_active:
            raise forms.ValidationError('This product is not active.')
        return product