from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import (
    Payment, LoanPayment, 
    Transfer,
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

        if not instance.sender.is_superuser:
            # SENDER IS AGEN OR OTHER CUSTOMER // NOMINAL HARUS SAMA DENGAN UTANGNYA
            if instance.user.profile.agen == instance.sender:
                loan_objs = loan_objs.filter(agen=instance.sender)

        nominal = instance.amount
        rec_loan_list = []

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
            rec_loan_list.append(lo_new)
            nominal -= amount

        pay_obj = Payment.objects.create(
            amount = instance.amount,
            user = instance.user
        )
        for i in rec_loan_list:
            i.payment = pay_obj
            i.save()


@receiver(post_save, sender=Transfer)
def get_transfer_biliing_record(sender, instance, created, **kwargs):
    if created:
        # KURANGI SALDO SENDER
        BillingRecord.objects.create(
            user = instance.sender,
            credit = instance.amount,
            transfer = instance
        )

        # TAMBAH SALDO RECEIVER
        LoanPayment.objects.create(
            user = instance.receiver,
            sender = instance.sender,
            amount= instance.amount,
            virtual_cash = True
        )