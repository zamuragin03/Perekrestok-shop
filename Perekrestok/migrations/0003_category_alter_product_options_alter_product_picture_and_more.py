# Generated by Django 4.1.7 on 2023-02-28 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "Perekrestok",
            "0002_alter_product_description_alter_product_picture_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Категория")),
            ],
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": ("Продукт",), "verbose_name_plural": "Продукты"},
        ),
        migrations.AlterField(
            model_name="product",
            name="picture",
            field=models.ImageField(
                blank=True, upload_to="products/%Y/%m/%d", verbose_name="Иллюстрация"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Perekrestok.category",
                verbose_name="Категория",
            ),
        ),
    ]
