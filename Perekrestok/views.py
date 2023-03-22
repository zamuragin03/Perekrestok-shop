from django.shortcuts import *
from django.http import *
from .models import *
from rest_framework import generics
from .serializers import ProductSerializer
from django.views.generic import *
from wwm.wwm import *
import json


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
    words = [
        "Превосходный",
        "Замечательный",
        "Отличный",
        "Хороший",
        "Блестящий",
        "Чудесный",
    ]
    from random import choice

    a = choice(words)
    context = {
        "title": product.title,
        "product": product,
        "choice": a,
        "item_count": item_count,
    }

    return render(request, "Perekrestok/show_item.html", context=context)


def thanks_for_buying(request: HttpRequest, order_id):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    context_success = {}
    ordered_products = WorkingWithCart.get_finished_order_products(
        session_key=session_id, order_id=order_id
    )
    total_price = WorkingWithCart.get_finished_order_summ(order_id=order_id)
    context_success["order_id"] = order_id
    context_success["order_items"] = ordered_products
    context_success["total_price"] = total_price
    return render(
        request, "Perekrestok/thanks_for_buying.html", context=context_success
    )


class CatalogView(ListView):
    model = Product
    template_name = "Perekrestok/catalog.html"
    context_object_name = "products"
    extra_context = {"title": "Каталог", "cat_selected": 0}

    def post(self, request: HttpRequest, *args, **kwargs):
        cat_id = request.POST.get("category")
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key
        prod_list = WorkingWithProducts.get_all_products(
            session_key=session_id, id=cat_id
        )
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
        prod_list = WorkingWithProducts.get_all_products(session_key=session_id, id="0")
        return prod_list

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


class create_order(TemplateView):
    template_name = "Perekrestok/create_order.html"
    succes_template = "Perekrestok/thanks_for_buying.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление заказа"
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key
        total_price = WorkingWithCart.get_total_sum(session_key=session_id)
        total_count = WorkingWithCart.get_overall_count(session_key=session_id)
        has_items = WorkingWithCart.has_cart_products(session_key=session_id)
        context["total_price"] = total_price
        context["total_count"] = total_count
        context["has_items"] = has_items
        return context

    def post(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.save()
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        pymntType = request.POST.get("PaymentType")
        email = request.POST.get("email")
        session_id = request.session.session_key
        props = {
            "Имя": str(name).strip(),
            "Телефон": str(phone).strip(),
            "Адрес": str(address).strip(),
            "Тип оплаты": str(pymntType).strip(),
            "Почта": str(email).strip(),
        }
        context = {}
        for key, value in props.items():
            if value == "" or value == "None":
                context = self.get_context_data()
                context["error_message"] = f"Заполите поле {key}"
                context["title"] = "Проверьте поля"
                context["name"] = name
                context["phone"] = phone
                context["address"] = address
                context["email"] = email
                if pymntType is not None:
                    context["payment"] = int(pymntType)

                return render(request, "Perekrestok/create_order.html", context=context)
        WorkingWithCostumers.create_costumer(phone=phone, name=name, email=email)
        WorkingWithOrder.create_order(
            address=address,
            name=name,
            phone=phone,
            payment_id=pymntType,
            session_id=session_id,
        )
        WorkingWithCart.finish_cart(session_key=session_id)
        order_id = WorkingWithOrder.get_order_id(session_id=session_id)

        return HttpResponseRedirect(
            reverse(
                "thanks_for_buying",
                args=[
                    order_id,
                ],
            )
        )


class ProdcuctAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
