# Generated by Django 2.1.5 on 2019-03-17 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_operator_hint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='commision',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
    ]
