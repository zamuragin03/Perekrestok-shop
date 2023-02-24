from django.shortcuts import *
from django.http import *
from .models import *


def main(request: HttpRequest):
    context = {
        'title':'Главная страница'
    }
    return render(request, "Perekrestok/main.html",context=context)


def about(request: HttpRequest):
    context = {
        'title':'О нас'
    }
    return render(request, "Perekrestok/about.html", context=context)


def catalog(request: HttpRequest):
    context = {
        'title':'Каталог'
    }
    return render(request, "Perekrestok/catalog.html", context=context)


def contacts(request: HttpRequest):
    context = {
        'title':'Контакты'
    }
    return render(request, "Perekrestok/contacts.html", context=context)


def cart(request: HttpRequest):
    context = {
        'title':'Корзина'
    }
    return render(request, "Perekrestok/cart.html", context=context)

def show_item(request:HttpRequest, item_slug):
    product =get_object_or_404(Product, slug=item_slug)

    context = {
        'title':product.title,
        'product': product,
        
    }
    return render(request, 'Perekrestok/show_item.html', context=context)

