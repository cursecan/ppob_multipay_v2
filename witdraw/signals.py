from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Witdraw
from billing.models import CommisionRecord
from bankrecon.models import Reconciliation


@receiver(post_save, sender=Witdraw)
def withdraw_triggering(sender, instance, created, **kwargs):
    if created:
        Reconciliation.objects.create(
            nominal = instance.amount,
            keterangan = 'Transfer komisi ' + instance.create_by.profile.ponsel,
            resource = 0,
            commision_witdraw = instance
        )

        CommisionRecord.objects.create(
            agen = instance.create_by,
            credit = instance.amount,
            verified = True,
            withdraw = instance,
            is_withdraw = True
        )