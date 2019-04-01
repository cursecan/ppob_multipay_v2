# Generated by Django 2.1.5 on 2019-03-29 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0009_auto_20190322_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefundApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('delete_on', models.DateTimeField(blank=True, null=True)),
                ('approve', models.BooleanField(default=False)),
                ('create_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RefundRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('delete_on', models.DateTimeField(blank=True, null=True)),
                ('comment', models.CharField(max_length=200)),
                ('closed', models.BooleanField(default=False)),
                ('create_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('intstan_trx', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instan_refund', to='transaction.InstanSale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='refundapproval',
            name='refund',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transaction.RefundRequest'),
        ),
    ]