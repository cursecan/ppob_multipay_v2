# Generated by Django 2.1.5 on 2019-02-24 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0006_auto_20190220_0912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responseinsale',
            name='sisa_saldo',
        ),
        migrations.RemoveField(
            model_name='responseppobsale',
            name='sisa_saldo',
        ),
    ]
