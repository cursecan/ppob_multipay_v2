# Generated by Django 2.1.5 on 2019-02-06 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
        ('billing', '0004_loanrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfitRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('instansale_trx', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.InstanSale')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
