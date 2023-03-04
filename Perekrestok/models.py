from django.db import models
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=10)
    amount = models.IntegerField(verbose_name="Количество")
    picture = models.ImageField(
        upload_to="products",
        verbose_name="Иллюстрация",
        blank=True,
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Категория",
        null=True,
        default=None,
    )

    def __str__(self) -> str:
        return str(self.title)

    def get_absolute_url(self):
        return "item/" + self.slug

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Category(models.Model):
    name = models.CharField(
        verbose_name="Категория",
        max_length=255,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Cart(models.Model):
    session_key = models.CharField(max_length=128, verbose_name="session_key")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Выбрано")
    is_paid = models.BooleanField(verbose_name="Оплачено")
    total_price = models.IntegerField(verbose_name="Общая цена", null=True, )


    def save(self,*args, **kwargs):
        self.total_price = self.product.price*self.amount
        super(Cart, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
    

