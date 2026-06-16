from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bakery_app', '0007_order_delivery_promotion_category_review_baking_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery',
        ),
    ]
