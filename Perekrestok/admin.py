from django.contrib import admin
from .models import *
# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    fields = ['title','category', 'price','amount','slug','description','picture',]
    list_display=fields
    list_filter=['category']
    prepopulated_fields ={'slug':('title',)}
    search_fields = ['title','price','description','amount','slug','picture',]
    list_editable=['category',]
    
class CategoriesAdmin(admin.ModelAdmin):
    list_display =['id','name']

class CartAdmin(admin.ModelAdmin):
    list_display =[field.name for field in Cart._meta.get_fields()]

class PaymentTypeAdmin(admin.ModelAdmin):
    list_display =('id','name')

class OrderStatusAdmin(admin.ModelAdmin):
    list_display= ('id','name')

class CostumerInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone','email')

class OrderInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Orders_Info._meta.get_fields()]
    list_display_links = [field.name for field in Orders_Info._meta.get_fields()]


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_number',
    )

admin.site.register(Order, OrderAdmin)
admin.site.register(Orders_Info, OrderInfoAdmin)
admin.site.register(Costumer_Info, CostumerInfoAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Product,ProductsAdmin)
admin.site.register(Cart, CartAdmin)
# admin.site.register(PaymentType, PaymentTypeAdmin)
# admin.site.register(Order_Status, OrderStatusAdmin)
