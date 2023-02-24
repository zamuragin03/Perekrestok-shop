from django.urls import path
from .views import *

urlpatterns = [
    path('main', main, name='main'),
    path('cart', cart, name='cart'),
    path('catalog', catalog, name='catalog'),
    path('contacts', contacts, name='contacts'),
    path('about', about, name='about'),
    # path('item/<int:item_id>', show_item, name='show_item'),
    path('item/<slug:item_slug>', show_item, name='show_item'),

]