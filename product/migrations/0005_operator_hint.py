# Generated by Django 2.1.5 on 2019-03-15 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20190307_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='hint',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
