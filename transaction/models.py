from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

from core.models import CommonBase
from product.models import Product


class PpobSale(CommonBase):
    INQUERY = 'IN'
    PAY = 'PY'
    SALETYPE_LIST = (
        (INQUERY, 'INQUERY REQUEST'),
        (PAY, 'PAYMENT REQUEST')
    )

    code = models.CharField(max_length=30, unique=True, editable=False)
    customer = models.CharField(max_length=30)
    sale_type = models.CharField(max_length=2, choices=SALETYPE_LIST, default=INQUERY)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ppob_product')
    product_code = models.CharField(max_length=30, blank=True)
    nominal = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='ppob_create_user')
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = int(timezone.now().timestamp() * 100)
            self.product_code = self.product.code
            self.commision = self.product.commision

        super(PpobSale, self).save(*args, **kwargs)

    def __str__(self):
        return self.code

    def get_status(self):
        return self.ppobsale_status.latest('timestamp')

    def get_billing_record(self):
        return self.bill_ppob_trx.filter(is_delete=False).latest('timestamp')

    def get_commision_record(self):
        if self.commision_ppob_trx.filter(is_delete=False).exists():
            return self.commision_ppob_trx.filter(is_delete=False).latest('timestamp')
        return None

    def get_loan_record(self):
        if self.loan_ppob_trx.filter(is_delete=False).exists():
            return self.loan_ppob_trx.filter(is_delete=False).latest('timestamp')
        return  None



class InstanSale(CommonBase):
    code = models.CharField(max_length=30, unique=True, editable=False)
    customer = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='instan_product')
    product_code = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='instan_create_user')
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = int(timezone.now().timestamp() * 100)
            self.product_code = self.product.code
            self.price = self.product.price
            self.commision = self.product.commision

        super(InstanSale, self).save(*args, **kwargs)

    def __str__(self):
        return self.code

    def get_status(self):
        return self.instansale_status.latest('timestamp')

    def get_billing_record(self):
        return self.bill_instan_trx.filter(is_delete=False).latest('timestamp')

    def get_commision_record(self):
        if self.commision_instan_trx.filter(is_delete=False).exists():
            return self.commision_instan_trx.filter(is_delete=False).latest('timestamp')
        return None

    def get_loan_record(self):
        if self.loan_instan_trx.filter(is_delete=False).exists():
            return self.loan_instan_trx.filter(is_delete=False).latest('timestamp')
        return  None



class Status(CommonBase):
    OPEN = 'OP'
    INPROCESS = 'IN'
    COMPLETE = 'CO'
    FAILED = 'FL'
    STATUS_LIST = (
        (OPEN, 'OPEN'),
        (INPROCESS, 'IN PROCESS'),
        (COMPLETE, 'COMPLETE'),
        (FAILED, 'FAILED')
    )
    instansale = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True, related_name='isntansale_status')
    ppobsale = models.ForeignKey(PpobSale, on_delete=models.CASCADE, blank=True, null=True, related_name='ppobsale_status')
    status = models.CharField(max_length=2, choices=STATUS_LIST, default=OPEN)

    def __str__(self):
        return self.get_status_display()