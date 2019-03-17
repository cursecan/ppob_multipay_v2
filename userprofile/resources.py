from import_export import resources
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget


from .models import (
    Profile, Wallet, UploadUser
)


class UploadUserResource(resources.ModelResource):
    class Meta:
        model = UploadUser
        fields = [
            'username', 'password', 'first_name', 'last_name'
        ]

        export_order = [
            'username', 'password', 'first_name', 'last_name'
        ]
        import_id_fields = ['username']
        skip_unchanged = True
        report_skipped = False


class WalletResource(resources.ModelResource):
    ponsel = resources.Field(
        attribute='profile', column_name='ponsel',
        widget=ForeignKeyWidget(Profile, 'ponsel')
    )

    class Meta:
        model = Wallet
        fields = [
            'ponsel', 'saldo', 'limit', 'loan', 'commision', 'init_loan'
        ]

        export_order = [
            'ponsel', 'saldo', 'limit', 'loan', 'commision', 'init_loan'
        ]
        import_id_fields = ['ponsel']
        skip_unchanged = True
        report_skipped = False
