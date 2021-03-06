# Generated by Django 2.1.5 on 2019-02-03 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0001_initial'),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingrecord',
            name='instansale_trx',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.InstanSale'),
        ),
        migrations.AddField(
            model_name='billingrecord',
            name='prev_billing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.BillingRecord'),
        ),
        migrations.AddField(
            model_name='billingrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
