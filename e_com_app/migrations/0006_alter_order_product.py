# Generated by Django 5.0.6 on 2024-07-07 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_com_app', '0005_order_customer_email_order_customer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_com_app.product'),
        ),
    ]
