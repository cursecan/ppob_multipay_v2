from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User

from core.models import CommonBase

from datetime import datetime
import re


class Bank(CommonBase):
    bank_code = models.CharField(max_length=3, unique=True)
    bank_name = models.CharField(max_length=50)

    class Meta:
        ordering = [
            'bank_code'
        ]

    def __str__(self):
        return self.bank_code


class BankAccount(CommonBase):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bank')
    account = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, blank=True)
    how_to = models.TextField(max_length=2000, blank=True)

    class Meta:
        ordering = [
            'bank__bank_code'
        ]

    def __str__(self):
        return self.account


class Reconciliation(CommonBase):
    reconid = models.CharField(max_length=30, unique=True, editable=False)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='bank_account')
    nominal = models.DecimalField(max_digits=15, decimal_places=0)
    trans_date = models.DateTimeField(default=timezone.now)
    keterangan = models.TextField(max_length=500, blank=True)
    marker = models.TextField(max_length=30, blank=True)
    identified = models.BooleanField(default=False)

    class Meta:
        ordering = [
            '-trans_date', 'bank_account' 
        ]

    def save(self, *args, **kwargs):
        if self.reconid is None or self.reconid == '':
            tm = timezone.now()
            dt = datetime.strftime(tm, '%Y%m%d')
            bank_code = self.bank_account.bank.bank_code
            c = Reconciliation.objects.filter(trans_date__date=tm.date()).count() + 1

            self.reconid = bank_code + dt + str(c).rjust(4,'0')

            mark = re.findall(r'08\d+', self.keterangan)
            if mark:
                self.marker = mark[0]

        super(Reconciliation, self).save(*args, **kwargs)


class Catatan(CommonBase):
    nomor = models.CharField(max_length=20)
    keterangan = models.CharField(max_length=30)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        return self.nomor
