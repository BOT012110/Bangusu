# Generated by Django 3.0.8 on 2020-09-01 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bangusu', '0006_auto_20200901_2259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_date',
            new_name='ordered_date',
        ),
    ]