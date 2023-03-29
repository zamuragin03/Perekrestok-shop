from Perekrestok.model_services.order_service import *
from Perekrestok.model_services.cart_service import *
from Perekrestok.model_services.product_service import *
from Perekrestok.model_services.costumer_service import *
from django.shortcuts import *


def get_creating_order_context(session_id, context):
    context["title"] = "Оформление заказа"
    total_price = WorkingWithCart.get_total_sum(session_key=session_id)
    total_count = WorkingWithCart.get_overall_count(session_key=session_id)
    has_items = WorkingWithCart.has_cart_products(session_key=session_id)
    context["total_price"] = total_price
    context["total_count"] = total_count
    context["has_items"] = has_items
    return context


"""create order and return it number"""


def create_order(name, phone, email, address, pymntType, session_id):
    WorkingWithCostumers.create_costumer(phone=phone, name=name, email=email)
    WorkingWithOrder.create_order(
        address=address,
        name=name,
        phone=phone,
        payment_id=pymntType,
        session_id=session_id,
    )
    WorkingWithCart.finish_cart(session_key=session_id)
    return WorkingWithOrder.get_order_id(session_id=session_id)


def get_cart_products(session_id):
    return WorkingWithCart.get_cart_products(session_key=session_id)


def get_cart_context(session_id, context):
    context["title"] = "Корзина"
    total_price = WorkingWithCart.get_total_sum(session_key=session_id)
    context["total_price"] = total_price
    return context


def add_product_to_cart(session_id, product_id):
    WorkingWithCart.add_to_cart(session_key=session_id, prod_id=product_id)


def change_cart_product(session_id, product_id, flag):
    WorkingWithCart.change_cart_product(
        session_key=session_id, id=product_id, flag=flag
    )


def delete_product_from_cart(session_id, product_id):
    WorkingWithCart.delete_product_from_cart(session_key=session_id, id=id)


def get_show_products_by_cat_context(session_id, cat_id):
    prod_list = WorkingWithProducts.get_all_products(session_key=session_id, id=cat_id)
    context = {
        "title": "Каталог",
        "products": prod_list,
        "cat_selected": int(cat_id),
    }
    return context

def get_catalog_products(session_id):
    prod_list = WorkingWithProducts.get_all_products(session_key=session_id, id="0")
    return prod_list
    
def get_finished_order_context(context, order_id, session_id):
        ordered_products = WorkingWithCart.get_finished_order_products(
        session_key=session_id, order_id=order_id
        )
        total_price = WorkingWithCart.get_finished_order_summ(order_id=order_id)
        context["order_id"] = order_id
        context["order_items"] = ordered_products
        context["total_price"] = total_price
        return context

def get_finished_order_query(session_id, order_id):
    ordered_products = WorkingWithCart.get_finished_order_products(
        session_key=session_id, order_id=order_id
        )
    return ordered_products
def get_item_context(session_id, slug, context):
        item_count = WorkingWithCart.get_selecte_product_count(
            session_key=session_id, slug=slug
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

        word = choice(words)
        # context = {
        #     # "title": product.title,
        #     # "product": product,
        #     "choice": a,
        #     "item_count": item_count,
        # }
        context['choice']=word
        context['item_count']=item_count
        return context