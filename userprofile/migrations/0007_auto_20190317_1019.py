# Generated by Django 2.1.5 on 2019-03-17 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_auto_20190317_1017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user__username']},
        ),
    ]