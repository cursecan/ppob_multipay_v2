# Generated by Django 2.1.5 on 2019-04-21 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankrecon', '0004_catatan'),
    ]

    operations = [
        migrations.AddField(
            model_name='catatan',
            name='category',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='catatan',
            name='nama',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]