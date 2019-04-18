from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Reconciliation,
)
from payment.models import (
    LoanPayment, Payment
)
from userprofile.models import (
    Profile,
)


@receiver(post_save, sender= Reconciliation)
def bankrecon_trigger(sender, instance, created, **kwargs):
    if created:
        if instance.marker is not None and instance.marker != '':
            # Marker is filled
            profiles = Profile.objects.filter(ponsel=instance.marker)
            if profiles.exists():
                # Profile exists with ponsel marker
                profile = profiles.get()

                # Complete loan payment, with trigger to paymnet
                lpayment = LoanPayment.objects.create(
                    user = profile.user,
                    amount = instance.nominal,
                    virtual_cash = True
                )

                lpayment.refresh_from_db()
                payment = lpayment.payment
                payment.reconsil = instance
                payment.save()

                instance.identified = True
                instance.save()


