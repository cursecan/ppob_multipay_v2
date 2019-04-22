from django import forms

from .models import (
    Group, Operator, Product
)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'code', 'group_name', 'active'
        ]

    def clean_group_name(self):
        return self.cleaned_data['group_name'].upper()

    def clean_code(self):
        return self.cleaned_data['code'].upper()


class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = [
            'code', 'operator_name'
        ]

    def clean_operator_name(self):
        return self.cleaned_data['operator_name'].upper()

    def clean_code(self):
        return self.cleaned_data['code'].upper()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'code', 'product_name',
            'type_product',
            'operator', 'group',
            'nominal', 'price', 'commision',
            'is_active'
        ]
