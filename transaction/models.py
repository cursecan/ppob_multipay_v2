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
    inquery = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='ppob_inquery')
    customer = models.CharField(max_length=30)
    sale_type = models.CharField(max_length=2, choices=SALETYPE_LIST, default=INQUERY)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ppob_product')
    product_code = models.CharField(max_length=30, blank=True)
    nominal = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='ppob_create_user')
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            if self.inquery:
                self.product = self.inquery.product
                self.customer = self.inquery.customer
                self.sale_type = self.PAY
                self.nominal = self.inquery.responseppobsale.nominal
                self.price = self.inquery.responseppobsale.get_price()

            self.code = str(int(timezone.now().timestamp() * 100))
            self.product_code = self.product.code
            self.commision = self.product.commision

            if self.product.price != 0:
                self.price = self.product.price
                self.nominal = self.product.nominal

        super(PpobSale, self).save(*args, **kwargs)

    def __str__(self):
        if self.sale_type == self.INQUERY:
            return 'IN ' + self.code
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

    def get_sn(self):
        return self.responseppobsale.ref3
    

    def get_profit(self):
        return self.price - self.responseppobsale.saldo_terpotong

    def get_customer_name(self):
        return self.responseppobsale.nama_pelanggan

    def get_customer_detail(self):
        return {
            'number': self.customer,
            'name': self.responseppobsale.nama_pelanggan,
            'tagihan': self.responseppobsale.nominal,
            'admin': self.responseppobsale.admin
        }


class InstanSale(CommonBase):
    code = models.CharField(max_length=30, unique=True, editable=False)
    customer = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='instan_product')
    product_code = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='instan_create_user')
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = str(int(timezone.now().timestamp() * 100))
            self.product_code = self.product.code
            self.price = self.product.price
            self.commision = self.product.commision
            if self.create_by.profile.user_type == 2:
                self.price = self.product.agen_price()
                self.commision = 0

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

    def get_sn(self):
        try :
            return self.responseinsale.sn
        except :
            return None

    def get_profit(self):
        try :
            return self.price - self.responseinsale.saldo_terpotong
        except :
            return 0

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
    instansale = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True, related_name='instansale_status')
    ppobsale = models.ForeignKey(PpobSale, on_delete=models.CASCADE, blank=True, null=True, related_name='ppobsale_status')
    status = models.CharField(max_length=2, choices=STATUS_LIST, default=OPEN)

    def __str__(self):
        return self.get_status_display()


class ResponseInSale(CommonBase):
    sale = models.OneToOneField(InstanSale, on_delete=models.CASCADE)
    kode_produk = models.CharField(max_length=100, blank=True)
    waktu = models.CharField(max_length=100, blank=True)
    no_hp = models.CharField(max_length=100, blank=True)
    sn = models.CharField(max_length=100, blank=True)
    nominal = models.PositiveIntegerField(default=0)
    ref1 = models.CharField(max_length=100, blank=True)
    ref2 = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    ket = models.CharField(max_length=200, blank=True)
    saldo_terpotong = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Transaksi Topup'
        ordering = [
            '-timestamp'
        ]


class ResponsePpobSale(CommonBase):
    sale = models.OneToOneField(PpobSale, on_delete=models.CASCADE)
    kode_produk = models.CharField(max_length=100, blank=True)
    waktu = models.CharField(max_length=100, blank=True)
    idpel1 = models.CharField(max_length=100, blank=True)
    idpel2 = models.CharField(max_length=100, blank=True)
    idpel3 = models.CharField(max_length=100, blank=True)
    nama_pelanggan = models.CharField(max_length=100, blank=True)
    periode = models.CharField(max_length=100, blank=True)
    nominal = models.PositiveIntegerField(default=0)
    admin = models.PositiveIntegerField(default=0)
    ref1 = models.CharField(max_length=100, blank=True)
    ref2 = models.CharField(max_length=100, blank=True)
    ref3 = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    ket = models.CharField(max_length=200, blank=True)
    saldo_terpotong = models.PositiveIntegerField(default=0)
    url_struk = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Transaksi Ppob'
        ordering = [
            '-timestamp'
        ]

    def get_price(self):
        return self.nominal + self.admin


class RefundRequest(CommonBase):
    intstan_trx = models.ForeignKey(InstanSale, on_delete=models.CASCADE, blank=True, null=True, related_name='instan_refund')
    ppob_trx = models.ForeignKey(PpobSale, on_delete=models.CASCADE, blank=True, null=True, related_name='ppob_refund')
    comment = models.CharField(max_length=200)
    closed = models.BooleanField(default=False)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        if self.intstan_trx:
            return self.intstan_trx.code
        if self.ppob_trx:
            return self.ppob_trx.code

    def get_trx(self):
        if self.intstan_trx:
            return self.intstan_trx
        if self.ppob_trx:
            return self.ppob_trx
        return None

class RefundApproval(CommonBase):
    refund = models.OneToOneField(RefundRequest, on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = [
            '-timestamp'
        ]