# Generated by Django 2.1.7 on 2020-07-25 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20200725_0734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipments',
            name='is_active',
        ),
    ]