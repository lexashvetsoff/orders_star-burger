# Generated by Django 3.2.15 on 2023-02-12 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_rename_count_ordermenuitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sum',
        ),
        migrations.RemoveField(
            model_name='ordermenuitem',
            name='sum',
        ),
    ]
