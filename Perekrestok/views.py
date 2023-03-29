from django.shortcuts import *
from django.http import *
from rest_framework import generics
from .serializers import ProductSerializer
from django.views.generic import *
from django.urls import reverse
from Perekrestok.models import *
from Perekrestok import Services
from Perekrestok.model_services.order_service import WorkingWithOrder


def main(request: HttpRequest):
    context = {"title": "Главная страница"}
    return render(request, "Perekrestok/main.html", context=context)


def about(request: HttpRequest):
    context = {"title": "О нас"}
    return render(request, "Perekrestok/about.html", context=context)


def contacts(request: HttpRequest):
    context = {"title": "Контакты"}
    return render(request, "Perekrestok/contacts.html", context=context)

class ShowItem(DetailView):
    model = Product
    template_name = 'Perekrestok/show_item.html'

    def get_session_id(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key
    
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     slug = self.kwargs.get(self.slug_url_kwarg, None)
    #     print(slug)
    #     print('-'*100)
    #     # context= Services.get_item_context(session_id=self.get_session_id(request=self.request), slug=self.get_slug_field(), context=context)
    #     return context
    
class ThanksForPurchase(DetailView):
    template_name = "Perekrestok/thanks_for_buying.html"
    # model = Cart
    context_object_name= 'order_items'

    
    def get_session_id(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key
    def get_queryset(self):
        return Services.get_finished_order_query(session_id=self.get_session_id(request=self.request), order_id=self.kwargs['order_id'])
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context = Services.get_finished_order_context(context=context, order_id=self.kwargs['order_id'], session_id=self.get_session_id(request=self.request))
        return context


class CatalogView(ListView):
    model = Product
    template_name = "Perekrestok/catalog.html"
    context_object_name = "products"
    extra_context = {"title": "Каталог", "cat_selected": 0}
    def get_session_id(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key
    
    def post(self, request: HttpRequest, *args, **kwargs):
        cat_id = request.POST.get("category")
        context = Services.get_show_products_by_cat_context(session_id=self.get_session_id(request=self.request), cat_id=cat_id)
        return render(request, "Perekrestok/catalog.html", context=context)

    def get_queryset(self):
        return Services.get_catalog_products(session_id=self.get_session_id(request=self.request))


class delete_from_cart(TemplateView):
    def get_session_id(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key
    
    def get(self, request: HttpRequest, *args, **kwargs):
        id = request.GET["id"]
        Services.delete_product_from_cart(session_id=self.get_session_id(request=self.request), product_id=id)
        return HttpResponse("ok", content_type="text/html")


class change_cart_amount(TemplateView):
    def get_session_id(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key
     
    def get(self, request: HttpRequest, *args, **kwargs):
        id = request.GET["id"]
        flag = request.GET["flag"]
        Services.change_cart_product(session_id=self.get_session_id(request=self.request), product_id=id, flag=flag)
        return HttpResponse("ok", content_type="text/html")


class add_to_cart(ListView):
    def get_session_id(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key
    
    def get(self, request: HttpRequest, *args, **kwargs):
        id = request.GET["id"]
        Services.add_product_to_cart(session_id=self.get_session_id(request=self.request), product_id=id)
        return HttpResponse("ok", content_type="text/html")


class CartView(ListView):
    
    model = Cart
    template_name = "Perekrestok/cart.html"
    context_object_name = "cart"

    def get_session_id(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key
    
    def get_queryset(self):
        return Services.get_cart_products(session_id=self.get_session_id(request=self.request))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_context = Services.get_cart_context(session_id=self.get_session_id(request=self.request), context=context)
        return cart_context


class create_order(TemplateView):
    template_name = "Perekrestok/create_order.html"

    def get_session_id(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_context = Services.get_creating_order_context(session_id=self.get_session_id(request=self.request),context=context)
        return order_context

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        pymntType = request.POST.get("PaymentType")
        email = request.POST.get("email")
        is_validated = WorkingWithOrder.validate_data(name=name,phone=phone,address=address,pymntType=pymntType,email=email,context=self.get_context_data())
        if is_validated:
            return render(
                request, 'Perekrestok/create_order.html', context=is_validated
            )
        order_id = Services.create_order(name=name,phone=phone,address=address,pymntType=pymntType,email=email,session_id=self.get_session_id(request=self.request),)
        return HttpResponseRedirect(reverse("thanks_for_buying",args=[order_id,],))


class ProdcuctAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
