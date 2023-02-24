from django.db import models
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=10)
    amount = models.IntegerField(verbose_name="Количество")
    picture = models.ImageField(
        upload_to="products/%Y/%m/%d",
        verbose_name="Иллюстрация",
        blank=True,
    )
    description = models.CharField(verbose_name="Описание", max_length=255, blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )

    def __str__(self) -> str:
        return str(self.title)

    def get_absolute_url(self):
        return 'item/' +self.slug

    class Meta:
        verbose_name = 'Продукт',
        verbose_name_plural= 'Продукты'