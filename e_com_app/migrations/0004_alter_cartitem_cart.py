# Generated by Django 5.0.6 on 2024-07-05 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_com_app', '0003_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='e_com_app.cart'),
        ),
    ]