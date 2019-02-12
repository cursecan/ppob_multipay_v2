from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import (
    Payment, LoanPayment
)
from billing.models import (
    BillingRecord, LoanRecord
)


@receiver(post_save, sender=Payment)
def payment_billing_record(sender, instance, created, **kwargs):
    if created:
        BillingRecord.objects.create(
            payment = instance,
            debit = instance.amount,
            user = instance.user
        )


@receiver(post_save, sender=LoanPayment)
def payloan_biling_record(sender, instance, created, **kwargs):
    if created:
        loan_objs = LoanRecord.objects.filter(
            user = instance.user,
            record_type = 'LO',
            is_paid = False,
            is_delete = False
        )
        nominal = instance.amount

        for lo in loan_objs:
            unpaid = lo.get_loan_residu()
            if nominal <= 0:
                break

            amount = nominal
            if nominal >= unpaid:
                amount = unpaid
                lo.is_paid = True
                lo.save()

            lo_new = LoanRecord()
            lo_new.user = lo.user
            lo_new.agen = lo.agen
            lo_new.payform = lo
            lo_new.loan_payment = instance
            lo_new.record_type = 'PA'
            lo_new.credit = amount
            if not instance.virtual_cash:
                lo_new.debit = amount
                
            lo_new.save()
            nominal -= amount

        Payment.objects.create(
            amount = instance.amount,
            user = instance.user
        )
