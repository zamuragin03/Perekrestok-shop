from django.contrib import admin
from .models import *
# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    fields = ['title','price','amount', 'description','slug','picture']
    list_display=fields
    list_filter=fields
    prepopulated_fields ={'slug':('title',)}
    search_fields = fields
    

admin.site.register(Product,ProductsAdmin)
