# Generated by Django 2.1.5 on 2019-02-02 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'MEMBER'), (2, 'AGEN'), (3, 'PERSONAL')], default=3)),
                ('agen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_agen', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('saldo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('commision', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('loan', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('limit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='userprofile.Profile')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
