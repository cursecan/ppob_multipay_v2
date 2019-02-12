from django.db import models
from django.contrib.auth.models import User

from core.models import CommonBase

class Payment(CommonBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return '%s %d' %(self.user.email, self.amount)


class LoanPayment(CommonBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_loanpayment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    virtual_cash = models.BooleanField(default=False) # Jika True makan saldo piutang agen dikembalikan

    def __str__(self):
        return '%s %d' %(self.user.email, self.amount)
