from django import forms
from django.contrib.auth.models import User

from .models import Witdraw

MIN_COMMISION = 10000
class WitdrawForm(forms.ModelForm):
    class Meta:
        model = Witdraw
        fields = [
            'create_by', 'amount'
        ]

    def __init__(self, *args, **kwargs):
        self.fields['create_by'].queryset = User.objects.filter(
            profile__user_type=2
        )
        super(WitdrawForm,self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < MIN_COMMISION:
            raise forms.ValidationError('Monimal withdraw 10.000')
        return amount

    def clean_create_by(self):
        usr = self.cleaned_data.get('create_by')

        if usr.profile.user_type != 2:
            raise forms.ValidationError('User is not an agen')

        if usr.profile.ponsel is None or usr.profile.ponsel == '':
            raise forms.ValidationError('Ponsel canot be empty')

        if usr.profile.wallet.commision < MIN_COMMISION:
            raise forms.ValidationError('Commision not enought to withdraw')
        return usr