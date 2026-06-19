import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery_app', '0005_delivery_promotion_review_alter_order_baking_drink_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('baking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bakery_app.baking', verbose_name='Выпечка')),
                ('drink', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bakery_app.drink', verbose_name='Напиток')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='bakery_app.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Позиция заказа',
                'verbose_name_plural': 'Позиции заказа',
            },
        ),
        migrations.RemoveField(
            model_name='order',
            name='baking',
        ),
        migrations.RemoveField(
            model_name='order',
            name='drink',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
    ]
