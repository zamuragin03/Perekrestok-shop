# Generated by Django 4.1.7 on 2023-03-19 15:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Perekrestok", "0002_costumer_info_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_number",
            field=models.SmallIntegerField(
                default=0, null=True, verbose_name="Номер заказа"
            ),
        ),
    ]
