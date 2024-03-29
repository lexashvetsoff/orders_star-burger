# Generated by Django 3.2.15 on 2023-02-13 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('необработанный', 'необработанный'), ('сборка', 'сборка'), ('доставка', 'доставка'), ('исполнен', 'исполнен')], db_index=True, default='необработанный', max_length=15, verbose_name='статус заказа'),
        ),
    ]
