from django.db import models
from django.contrib.auth.models import User

from core.models import CommonBase

class Bank(CommonBase):
    bank_code = models.CharField(max_length=2, unique=True)
    bank_name = models.CharField(max_length=30)

    def __str__(self):
        return self.bank_name


class BankAccount(CommonBase):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bank_rekening')
    rekening = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = [
            'bank', 'name'
        ]

class Payment(CommonBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        return '%s %d' %(self.user.email, self.amount)

    def get_balance(self):
        return self.billing_apyment.get().balance       


class LoanPayment(CommonBase):
    """
        - Virtual cash True maka saldo piutang dikembalikan ke Agen (Saldo agen bertambah)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_loanpayment')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='payloan_sender')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    virtual_cash = models.BooleanField(default=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s %d' %(self.user.email, self.amount)


class Transfer(CommonBase):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trans_receiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tran_sender')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
