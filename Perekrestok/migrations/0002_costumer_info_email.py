# Generated by Django 4.1.7 on 2023-03-09 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Perekrestok", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="costumer_info",
            name="email",
            field=models.EmailField(default=0, max_length=254),
            preserve_default=False,
        ),
    ]