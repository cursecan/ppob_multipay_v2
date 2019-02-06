from django.db import models
from django.contrib.auth.models import User

from core.models import CommonBase
from transaction.models import InstanSale

class BillingRecord(CommonBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prev_billing = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    sequence = models.PositiveSmallIntegerField(default=1)
    instansale_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        self.balance = self.user.profile.wallet.saldo + self.debit - self.credit
        super(BillingRecord, self).save(*args, **kwargs)
    

class CommisionRecord(CommonBase):
    agen = models.ForeignKey(User, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prev_com = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    sequence = models.PositiveSmallIntegerField(default=1)
    instansale_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE)

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
    instansale_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        self.balance = self.user.profile.wallet.loan + self.debit - self.credit
        super(LoanRecord, self).save(*args, **kwargs)


class ProfitRecord(CommonBase):
    instansale_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
