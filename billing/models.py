from django.db import models
from django.contrib.auth.models import User

from core.models import CommonBase
from transaction.models import (
    InstanSale, PpobSale
)

class BillingRecord(CommonBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prev_billing = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    sequence = models.PositiveSmallIntegerField(default=1)
    instansale_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True, related_name='bill_instan_trx')
    ppobsale_trx = models.ForeignKey(PpobSale, on_delete=models.CASCADE, blank=True, null=True, related_name='bill_ppob_trx')

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        self.balance = self.user.profile.wallet.saldo + self.debit - self.credit
        super(BillingRecord, self).save(*args, **kwargs)

    def get_trx(self):
        if self.instansale_trx:
            return self.instansale_trx
        if self.ppobsale_trx:
            return self.ppobsale_trx
        return None

    def get_api_trx(self):
        trx = dict()
        if self.get_trx():
            trx['trx_code'] = self.get_trx().code
            trx['product'] = self.get_trx().product.product_name
            trx['commision'] = self.get_trx().commision
        return trx

    def get_api_status(self):
        if self.get_trx():
            return self.get_trx().get_status().get_status_display()
        return None

class CommisionRecord(CommonBase):
    agen = models.ForeignKey(User, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prev_com = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    sequence = models.PositiveSmallIntegerField(default=1)
    instansale_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True, related_name='commision_instan_trx')
    ppobsale_trx = models.ForeignKey(PpobSale, on_delete=models.CASCADE, blank=True, null=True, related_name='commision_ppob_trx')

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        self.balance = self.agen.profile.wallet.commision + self.debit - self.credit
        super(CommisionRecord, self).save(*args, **kwargs)


class LoanRecord(CommonBase):
    LOAN = 'LO'
    PAYMENT = 'PA'
    LIST_TYPE = (
        (LOAN, 'LOAN'),
        (PAYMENT, 'PAYMENT')
    )
    agen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_record_agen')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_record_user')
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0) # tambah utang
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0) # pengurangan utang
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0) # loan user balance
    is_paid = models.BooleanField(default=False)
    record_type = models.CharField(max_length=2, choices=LIST_TYPE, default=LOAN)
    payment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    instansale_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True, related_name='loan_instan_trx')
    ppobsale_trx = models.ForeignKey(PpobSale, on_delete=models.CASCADE, blank=True, null=True, related_name='loan_ppob_trx')

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        self.balance = self.user.profile.wallet.loan + self.debit - self.credit
        super(LoanRecord, self).save(*args, **kwargs)


class ProfitRecord(CommonBase):
    instansale_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True, related_name='profit_instan_trx')
    ppobsale_trx = models.ForeignKey(PpobSale, on_delete=models.CASCADE, blank=True, null=True, related_name='profit_ppob_trx')
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
