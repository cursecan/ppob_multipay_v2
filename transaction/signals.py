from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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
        

@receiver(post_save, sender=Status)
def status_failed_process(sender, instance, created, **kwargs):
    duedate = timezone.now()
    if created:
        if instance.status == 'FL':
            saletrx_obj = instance.instansale

            # Refund billing
            last_bill_obj = saletrx_obj.get_billing_record()
            BillingRecord.objects.create(
                instansale_trx = saletrx_obj,
                debit = saletrx_obj.price,
                user = saletrx_obj.create_by,
                prev_billing = last_bill_obj,
                sequence = last_bill_obj.sequence + 1
            )
            saletrx_obj.bill_instan_trx.update(
                is_delete=True, delete_on=duedate
            )

            # Refund Commision
            last_sale_obj = saletrx_obj.get_commision_record()
            if last_sale_obj:
                CommisionRecord.objects.create(
                    instansale_trx = saletrx_obj,
                    credit = last_sale_obj.debit,
                    agen = last_sale_obj.agen,
                    prev_com = last_sale_obj,
                    sequence = last_sale_obj.sequence + 1
                )
                saletrx_obj.commision_instan_trx.update(
                    is_delete=True, delete_on=duedate
                )
            
            # Refund loan
            last_loan_obj = saletrx_obj.get_loan_record()
            if last_loan_obj:
                LoanRecord.objects.create(
                    instansale_trx = saletrx_obj,
                    user = last_loan_obj.user,
                    agen = last_loan_obj.agen,
                    credit = last_loan_obj.debit
                )
                saletrx_obj.loan_instan_trx.update(
                    is_delete=True, delete_on=duedate
                )

            


