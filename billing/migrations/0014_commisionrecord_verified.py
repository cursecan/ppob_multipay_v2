# Generated by Django 2.1.5 on 2019-04-22 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0013_auto_20190331_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='commisionrecord',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
