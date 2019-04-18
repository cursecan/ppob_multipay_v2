# Generated by Django 2.1.5 on 2019-04-16 16:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('delete_on', models.DateTimeField(blank=True, null=True)),
                ('bank_code', models.CharField(max_length=3, unique=True)),
                ('bank_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('delete_on', models.DateTimeField(blank=True, null=True)),
                ('account', models.CharField(max_length=30, unique=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank', to='bankrecon.Bank')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reconciliation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('delete_on', models.DateTimeField(blank=True, null=True)),
                ('reconid', models.CharField(editable=False, max_length=30, unique=True)),
                ('nominal', models.DecimalField(decimal_places=0, max_digits=15)),
                ('trans_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('keterangan', models.TextField(blank=True, max_length=500)),
                ('identified', models.BooleanField(default=False)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_account', to='bankrecon.BankAccount')),
            ],
            options={
                'ordering': ['-trans_date', 'bank_account'],
            },
        ),
    ]
