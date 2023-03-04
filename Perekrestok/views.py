from django.shortcuts import *
from django.http import *
from .models import *
from rest_framework import generics
from .serializers import ProductSerializer
from wwm.wwm import *


def main(request: HttpRequest):
    context = {"title": "Главная страница"}
    return render(request, "Perekrestok/main.html", context=context)


def about(request: HttpRequest):
    context = {"title": "О нас"}
    return render(request, "Perekrestok/about.html", context=context)


def catalog(request: HttpRequest):
    context = {}
    if request.method == "POST":
        cat_id = request.POST.get("category")
        prod_list = WorkingWithProducts.get_all_products(id=cat_id)
        context = {
            "title": "Каталог", 
            "products": prod_list, 
            "cat_selected": int(cat_id)
                   }
    else:
        prod_list = WorkingWithProducts.get_all_products(id="*")
        context = {"title": "Каталог", "products": prod_list}

    return render(request, "Perekrestok/catalog.html", context=context)


def contacts(request: HttpRequest):
    context = {"title": "Контакты"}
    return render(request, "Perekrestok/contacts.html", context=context)


def cart(request: HttpRequest):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    cart = WorkingWithCart.get_cart_products(session_key=session_id)
    total_price = WorkingWithCart.get_total_sum(session_key=session_id)
    context = {"title": "Корзина", 
               "cart": cart,
               'total_price':total_price}

    return render(request, "Perekrestok/cart.html", context=context)


def show_item(request: HttpRequest, item_slug):
    product = get_object_or_404(Product, slug=item_slug)

    context = {
        "title": product.title,
        "product": product,
    }
    return render(request, "Perekrestok/show_item.html", context=context)


def add_to_cart(request: HttpRequest):
    if request.GET:
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        id = request.GET["id"]
        WorkingWithCart.add_to_cart(session_key=session_id, prod_id=id)

        return HttpResponse("ok", content_type="text/html")
    else:
        return HttpResponse("neok", content_type="text/html")


## API


class ProdcuctAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
