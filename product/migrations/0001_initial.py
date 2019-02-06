# Generated by Django 2.1.5 on 2019-02-02 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('group_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('operator_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Prefix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=4, unique=True)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Operator')),
            ],
            options={
                'ordering': ['prefix'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('product_name', models.CharField(max_length=200)),
                ('nominal', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('commision', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('is_active', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Group')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Operator')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddField(
            model_name='operator',
            name='group',
            field=models.ManyToManyField(through='product.Product', to='product.Group'),
        ),
    ]
