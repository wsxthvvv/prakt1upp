import django.db.models.deletion
from django.db import migrations, models


def copy_order_legacy_fields(apps, schema_editor):
    Order = apps.get_model('bakery_app', 'Order')
    for order in Order.objects.all():
        if order.customer_name and not order.buyer_name:
            order.buyer_name = order.customer_name
        if order.address and not order.delivery_address:
            order.delivery_address = order.address
        order.save(update_fields=['buyer_name', 'delivery_address'])


class Migration(migrations.Migration):

    dependencies = [
        ('bakery_app', '0009_order_user_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='buyer_firstname',
            field=models.CharField(default='', max_length=255, verbose_name='Фамилия покупателя'),
        ),
        migrations.AddField(
            model_name='order',
            name='buyer_name',
            field=models.CharField(default='', max_length=255, verbose_name='Имя покупателя'),
        ),
        migrations.AddField(
            model_name='order',
            name='buyer_surname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество покупателя'),
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий к заказу'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(default='', verbose_name='Адрес доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(
                choices=[('SH', 'Вывоз из магазина'), ('CR', 'Курьер'), ('PP', 'Пункт выдачи заказов')],
                default='SH',
                max_length=7,
                verbose_name='Способ доставки',
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, default='', verbose_name='Адрес доставки (устар.)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Имя клиента'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Телефон'),
        ),
        migrations.RunPython(copy_order_legacy_fields, migrations.RunPython.noop),
    ]
