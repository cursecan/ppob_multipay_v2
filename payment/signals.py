from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, F, Value as V
from django.db.models.functions import Coalesce


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
        # List semua loan yang belum closed / complete
        loan_objs = LoanRecord.objects.filter(
            user = instance.user,
            record_type = 'LO',
            closed = False,
        ).order_by('timestamp')

        if not instance.sender.is_superuser:
            # Filter hanya untuk user sesuai agen terdaftar
            loan_objs = loan_objs.filter(agen=instance.sender)

        nominal = instance.amount

        for lo in loan_objs:
            unpaid = lo.get_loan_residu()
            if nominal <= 0:
                break
    
            lo_new = LoanRecord()
            lo_new.user = lo.user
            lo_new.agen = lo.agen
            lo_new.payform = lo
            lo_new.loan_payment = instance
            lo_new.record_type = 'PA'
            lo_new.credit = nominal if nominal < unpaid else unpaid
            lo_new.bill_record = lo.bill_record
            if not instance.virtual_cash:
                lo_new.debit = lo_new.credit
            lo_new.save()
            lo_new.debit = 0
            lo_new.save()
            

            loan_res = lo_new.bill_record.loan_bill.aggregate(
                residu = Sum(F('debit') - F('credit'))
            )
            if loan_res['residu'] == 0:
                LoanRecord.objects.filter(
                    bill_record = lo_new.bill_record
                ).update(closed=True)

            nominal -= lo_new.credit

        pay_obj = Payment.objects.create(
            amount = instance.amount,
            user = instance.user
        )
        
        instance.payment = pay_obj
        instance.save()


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