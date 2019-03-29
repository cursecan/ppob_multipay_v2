from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import (
    InstanSale, Status, PpobSale,
    ResponseInSale, ResponsePpobSale,
    RefundApproval, RefundRequest,
)

from billing.models import (
    BillingRecord, CommisionRecord,
    LoanRecord, ProfitRecord,
)

from .tasks import (
    instansale_tasks, ppobsale_tasks
)


@receiver(post_save, sender=InstanSale)
def intansale_billing_record(sender, instance, created, **kwargs):
    if created:
        # Initial status transaction (OPEN)
        Status.objects.create(instansale=instance)

        # Response Sale Init
        ResponseInSale.objects.create(
            sale = instance
        )

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

        # Task process
        instansale_tasks(instance.id)




@receiver(post_save, sender=PpobSale)
def ppobsale_billing_record(sender, instance, created, **kwargs):
    if created:
        # Initial status transaction (OPEN)
        Status.objects.create(ppobsale=instance)

        # Response Ppob Sale
        ResponsePpobSale.objects.create(
            sale = instance
        )

        if instance.sale_type == 'PY':
            # Loan recording
            if instance.create_by.profile.wallet.get_saldo() < instance.price:
                LoanRecord.objects.create(
                    ppobsale_trx = instance,
                    user = instance.create_by,
                    agen = instance.create_by.profile.agen,
                    debit = instance.price - instance.create_by.profile.wallet.get_saldo()
                )

            # Commision record
            if instance.create_by.profile.agen.profile.user_type == 2:
                CommisionRecord.objects.create(
                    ppobsale_trx = instance,
                    debit = instance.commision,
                    agen = instance.create_by.profile.agen,
                )

            # Billing record
            BillingRecord.objects.create(
                ppobsale_trx = instance,
                credit = instance.price,
                user = instance.create_by
            )

            # Profit record
            ProfitRecord.objects.create(
                ppobsale_trx = instance,
            )

            # Task process
            ppobsale_tasks.now(instance.id)

        else :
            # Task process
            ppobsale_tasks.now(instance.id)
        

@receiver(post_save, sender=Status)
def status_failed_process(sender, instance, created, **kwargs):
    duedate = timezone.now()
    if created:
        # PPOB SALE
        if instance.ppobsale:
            saleppob_obj = instance.ppobsale

            if instance.status == 'CO':
                saleppob_obj.closed = True
                saleppob_obj.save()


        # INSTAN SALE
        if instance.instansale:
            saletrx_obj = instance.instansale
 
            if instance.status == 'CO':
                # Transaction Complete
                saletrx_obj.closed = True
                saletrx_obj.save()

            elif instance.status == 'FL':                
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

                # Refund billing
                last_bill_obj = saletrx_obj.get_billing_record()
                refund = saletrx_obj.price
                if last_loan_obj:
                    refund = last_loan_obj.debit
                BillingRecord.objects.create(
                    instansale_trx = saletrx_obj,
                    debit = refund,
                    user = saletrx_obj.create_by,
                    prev_billing = last_bill_obj,
                    sequence = last_bill_obj.sequence + 1
                )
                saletrx_obj.bill_instan_trx.update(
                    is_delete=True, delete_on=duedate
                )

                saletrx_obj.closed = True
                saletrx_obj.save()



@receiver(post_save, sender=RefundApproval)
def get_refund_response(sender, instance, created, **kwars):
    if created:
        trx = instance.refund.get_trx()
        if instance.approve:
            Status.objects.create(
                instansale = trx, status='FL'
            )

        instance.refund.closed = True
        instance.refund.save()