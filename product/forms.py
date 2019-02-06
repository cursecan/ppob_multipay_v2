from django import forms

from .models import (
    Group, Operator, Product
)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def clean_group_name(self):
        return self.cleaned_data['group_name'].upper()

    def clean_code(self):
        return self.cleaned_data['code'].upper()


class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = '__all__'

    def clean_operator_name(self):
        return self.cleaned_data['operator_name'].upper()

    def clean_code(self):
        return self.cleaned_data['code'].upper()