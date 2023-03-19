from django import template
from Perekrestok.models import *

register = template.Library()


# @register.simple_tag()
# def get_orders():
#     return Order.objects.all()


@register.simple_tag()
def get_menu():
    site_menu = [
        {'title': 'Главная', 'url_name': 'main'},
        {'title': 'О нас', 'url_name': 'about'},
        {'title': 'Каталог', 'url_name': 'catalog'},
        {'title': 'Контакты', 'url_name': 'contacts'},
        {'title': 'Корзина', 'url_name': 'cart'}
    ]
    return site_menu

@register.simple_tag()
def get_content():
    links = [
        {'name':'Шлюкоза'},
        {'name':'калий, магний, натрий, кальций, железо, фосфор, цинк, медь'},
        {'name':'Фруктоза'},
        {'name':'Сахароза'},
        {'name':'Глюкоза'},
    ]
    return links

@register.simple_tag()
def get_items():
    return Product.objects.all()

@register.simple_tag()
def get_all_categories():
    return Category.objects.all()

@register.simple_tag()
def get_all_payment_methods():
    return PaymentType.objects.all()