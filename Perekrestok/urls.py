from django.urls import path
from .views import *

urlpatterns = [
    path("", main, name="main"),
    path("cart", CartView.as_view(), name="cart"),
    path("catalog", CatalogView.as_view(), name="catalog"),
    path("contacts", contacts, name="contacts"),
    path("about", about, name="about"),
    # path('item/<int:item_id>', show_item, name='show_item'),
    path("item/<slug:item_slug>", ShowItem.as_view(), name="show_item"),
    path("api", ProdcuctAPI.as_view()),
    path("add_to_cart/", add_to_cart.as_view(), name="add_to_cart"),
    path("delete_from_cart", delete_from_cart.as_view(), name="delete_from_cart"),
    path("change_cart_amount", change_cart_amount.as_view(), name="change_cart_amount"),
    path("create_order", create_order.as_view(), name="create_order"),
    path("thanks_for_buying/<int:order_id>", ThanksForPurchase.as_view(), name="thanks_for_buying"),


]
