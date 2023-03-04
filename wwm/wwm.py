from Perekrestok.models import *
from django.db.models import Count, Sum


class WorkingWithCart:
    def add_to_cart(session_key, prod_id):
        c = Cart.objects.filter(
            session_key=session_key,
            product=Product.objects.get(id=prod_id),
        ).all()
        if not c.exists():
            c = Cart(
                session_key=session_key,
                product=Product.objects.get(id=prod_id),
                is_paid=False,
                amount=1,
            )
            c.save()
        else:
            c = Cart.objects.get(
                session_key=session_key, product=Product.objects.get(id=prod_id)
            )
            c.amount += 1
            c.save()

    def get_cart_products(session_key):
        res = Cart.objects.select_related().filter(session_key=session_key, is_paid=0).all()
        return res
    
    def get_total_sum(session_key):
        res = Cart.objects.select_related().filter(session_key=session_key, is_paid=0).all()
        s = 0
        for price in res:
            s+=int(price.total_price)
        return s

class WorkingWithProducts():

    def get_all_products(id):
        if id =='*':
            return Product.objects.all()
        
        cat = Category.objects.get(id=id)
        return Product.objects.select_related().filter(category=cat).all()
    
    