from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    InstanSale, Status
)
from billing.models import (
    BillingRecord, CommisionRecord,
    LoanRecord, ProfitRecord
)


@receiver(post_save, sender=InstanSale)
def intansale_billing_record(sender, instance, created, **kwargs):
    if created:
        # Initial status transaction (OPEN)
        Status.objects.create(instansale=instance)

        # Loan recording
        if instance.create_by.profile.wallet.get_saldo() < instance.product.price:
            LoanRecord.objects.create(
                instansale_trx = instance,
                user = instance.create_by,
                agen = instance.create_by.profile.agen,
                debit = instance.product.price - instance.create_by.profile.wallet.get_saldo()
            )

        # Commision record
        if instance.create_by.profile.agen.profile.user_type == 2:
            CommisionRecord.objects.create(
                instansale_trx = instance,
                debit = instance.commision,
                agen = instance.create_by.profile.agen,
            )

        # Billing record
        BillingRecord.objects.create(
            instansale_trx = instance,
            credit = instance.price,
            user = instance.create_by
        )

        # Profit record
        ProfitRecord.objects.create(
            instansale_trx = instance,
        )
        

        