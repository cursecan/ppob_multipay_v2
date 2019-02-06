from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from .models import (
    BillingRecord, CommisionRecord, LoanRecord
)
from userprofile.models import Wallet


@receiver(post_save, sender=BillingRecord)
def wallet_saldo_update(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.filter(
            profile__user=instance.user
        ).update(saldo=instance.balance)


@receiver(post_save, sender=CommisionRecord)
def wallet_commision_update(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.filter(
            profile__user=instance.agen
        ).update(commision=instance.balance)


@receiver(post_save, sender=LoanRecord)
def wallet_loan_update(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.filter(
            profile__user=instance.user
        ).update(loan=instance.balance)

        Wallet.objects.filter(
            profile__user=instance.agen
        ).update(saldo=F('saldo') - instance.debit + instance.credit)