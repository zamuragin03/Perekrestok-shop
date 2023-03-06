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

admin.site.register(Category, CategoriesAdmin)
admin.site.register(Product,ProductsAdmin)
admin.site.register(Cart, CartAdmin)

