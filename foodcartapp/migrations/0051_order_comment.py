# Generated by Django 3.2.15 on 2023-02-13 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(default='', verbose_name='Комментарий'),
        ),
    ]
