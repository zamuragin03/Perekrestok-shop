from django.db import models
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(
        verbose_name="Цена", decimal_places=2, max_digits=10)
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
        return str(self.name)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Cart(models.Model):
    session_key = models.CharField(max_length=128, verbose_name="session_key")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="Выбрано")
    is_paid = models.BooleanField(verbose_name="Оплачено")
    total_price = models.IntegerField(verbose_name="Общая цена", null=True, )
    order_id = models.SmallIntegerField(
        verbose_name='Номер заказа', null=True,)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price*self.count
        super(Cart, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class Costumer_Info(models.Model):
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=20, verbose_name='Имя')
    email = models.EmailField()
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Orders_Info(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    costumer = models.ForeignKey('Costumer_Info', on_delete=models.CASCADE)
    address = models.TextField(verbose_name='Адресс заказа')
    payment = models.ForeignKey('PaymentType', on_delete=models.CASCADE)
    status = models.ForeignKey('Order_Status', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Order(models.Model):
    order_number = models.SmallIntegerField(verbose_name='Номер заказа', null=True)
    def save(self, *args, **kwargs):
        self.order_number = self.id
        super(Order, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.order_number)


class PaymentType(models.Model):
    name = models.CharField(max_length=40, verbose_name='Тип оплаты')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Тип оплаты"
        verbose_name_plural = "Тип оплаты"


class Order_Status(models.Model):
    name = models.CharField(max_length=40, verbose_name='Статус заказа')
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статус заказа"
