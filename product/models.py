from django.db import models

# Create your models here.

from core.models import CommonBase

class Group(CommonBase):
    code = models.CharField(max_length=20, unique=True)
    group_name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = [
            'timestamp'
        ]
    
    def __str__(self):
        return self.group_name


class Operator(CommonBase):
    code = models.CharField(max_length=20, unique=True)
    operator_name = models.CharField(max_length=100)
    group = models.ManyToManyField(Group, through='Product')
    hint = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = [
            'timestamp'
        ]
    
    def __str__(self):
        return self.operator_name


class Prefix(models.Model):
    prefix = models.CharField(max_length=4, unique=True)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)

    class Meta:
        ordering = [
            'prefix'
        ]

    def __str__(self):
        return self.prefix


class Product(CommonBase):
    INSTAN = 'IN'
    INQUERY = 'QU'
    LIST_PRODUCTTYPE = (
        (INSTAN, 'INSTAN PRODUCT'),
        (INQUERY, 'INQUERY PRODUCT')
    )

    type_product = models.CharField(max_length=2, choices=LIST_PRODUCTTYPE, default=INSTAN)
    code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=200)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    nominal = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = [
            'operator', 'group', 'nominal', 'product_name'
        ]

    def __str__(self):
        return self.product_name

    def agen_price(self):
        return  self.price - self.commision

    def agen_commision(self):
        return 0