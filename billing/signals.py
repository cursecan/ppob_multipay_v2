from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from .models import (
    BillingRecord, CommisionRecord, LoanRecord
)
from userprofile.models import Wallet

# TRIGER BILLING
@receiver(post_save, sender=BillingRecord)
def wallet_saldo_update(sender, instance, created, **kwargs):
    """
        Billing mempengaruhi nilai dari wallet-saldo sesuai balance billing.
    """
    if created:
        # Calculate balance
        cur_walet = instance.user.profile.wallet
        cur_walet.refresh_from_db()
        
        instance.balance = cur_walet.saldo + instance.debit - instance.credit
        instance.save()

        # Updata saldo with new balance
        Wallet.objects.filter(
            profile__user=instance.user
        ).update(saldo=instance.balance)


@receiver(post_save, sender=CommisionRecord)
def wallet_commision_update(sender, instance, created, update_fields, **kwargs):
    """
        Commisison mempengaruhi nilai wallet-commision sesuai balance comisi
    """
    # if created:
    #     if instance.verified:
    #         instance.balance = instance.agen.profile.wallet.commision + instance.debit - instance.credit
    #         instance.save()

    #         Wallet.objects.filter(
    #             profile__user=instance.agen
    #         ).update(commision=instance.balance)

    # Update commision saldo if already verified commision
    if update_fields:
        if 'verified' in update_fields:
            if instance.verified:
                instance.balance = instance.agen.profile.wallet.commision + instance.debit - instance.credit
                instance.save()

                Wallet.objects.filter(
                    profile__user=instance.agen
                ).update(commision=instance.balance)


@receiver(post_save, sender=LoanRecord)
def wallet_loan_update(sender, instance, created, **kwargs):
    if created:

        Wallet.objects.filter(
            profile__user=instance.agen
        ).update(saldo=F('saldo') - instance.debit + instance.credit)