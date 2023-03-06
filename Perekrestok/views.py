from django.shortcuts import *
from django.http import *
from .models import *
from rest_framework import generics
from .serializers import ProductSerializer
from django.views.generic import *
from wwm.wwm import *


def main(request: HttpRequest):
    context = {"title": "Главная страница"}
    return render(request, "Perekrestok/main.html", context=context)


def about(request: HttpRequest):
    context = {"title": "О нас"}
    return render(request, "Perekrestok/about.html", context=context)


def contacts(request: HttpRequest):
    context = {"title": "Контакты"}
    return render(request, "Perekrestok/contacts.html", context=context)


def show_item(request: HttpRequest, item_slug):
    product = get_object_or_404(Product, slug=item_slug)
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    item_count = WorkingWithCart.get_selecte_product_count(
        session_key=session_id, slug=item_slug
    )
    words = ['Превосходный','Замечательный','Отличный','Хороший','Блестящий','Чудесный']
    from random import choice
    a = choice(words)
    context = {
        "title": product.title,
        "product": product,
        # 'item-count':item_slug
        'choice':a,
        "item_count": item_count,
    }

    return render(request, "Perekrestok/show_item.html", context=context)


class CatalogView(ListView):
    model = Product
    template_name = "Perekrestok/catalog.html"
    context_object_name = "products"
    extra_context = {"title": "Каталог", "cat_selected": 0}

    def post(self, request, *args, **kwargs):
        cat_id = request.POST.get("category")
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key

        prod_list = WorkingWithProducts.get_all_products(session_key=session_id, id=cat_id)
        context = {
            "title": "Каталог",
            "products": prod_list,
            "cat_selected": int(cat_id),
        }
        return render(request, "Perekrestok/catalog.html", context=context)
    
    def get_queryset(self):
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key
        res = WorkingWithCart.get_products_and_cart_amount(session_key=session_id)
        return res

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)


class delete_from_cart(TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs):
        id = request.GET["id"]
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key
        WorkingWithCart.delete_product_from_cart(session_key=session_id, id=id)
        return HttpResponse("ok", content_type="text/html")


class change_cart_amount(TemplateView):
    def get(self, request: HttpRequest, *args, **kwargs):
        id = request.GET["id"]
        flag = request.GET["flag"]
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key
        WorkingWithCart.change_cart_product(session_key=session_id, id=id, flag=flag)
        return HttpResponse("ok", content_type="text/html")


class add_to_cart(ListView):
    def get(self, request: HttpRequest, *args, **kwargs):
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        id = request.GET["id"]
        WorkingWithCart.add_to_cart(session_key=session_id, prod_id=id)
        return HttpResponse("ok", content_type="text/html")


class CartView(ListView):
    model = Cart
    template_name = "Perekrestok/cart.html"
    context_object_name = "cart"

    def get_queryset(self):
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key
        return WorkingWithCart.get_cart_products(session_key=session_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Корзина"
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key
        total_price = WorkingWithCart.get_total_sum(session_key=session_id)
        context["total_price"] = total_price
        return context

    # def post(self, request, *args, **kwargs):
    #     cat_id = request.POST.get("category")
    #     prod_list = WorkingWithProducts.get_all_products(id=cat_id)
    #     context = {
    #         "title": "Каталог",
    #         "products": prod_list,
    #         "cat_selected": int(cat_id)
    #                }
    #     return render(request, "Perekrestok/catalog.html", context=context)


class ProdcuctAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
