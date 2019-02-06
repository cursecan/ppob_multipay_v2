from django.db import models

# Create your models here.

from core.models import CommonBase

class Group(CommonBase):
    code = models.CharField(max_length=20, unique=True)
    group_name = models.CharField(max_length=100)

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
    code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=200)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    nominal = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = [
            '-timestamp'
        ]

    def __str__(self):
        return self.product_name