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
                count=1,
            )
            c.save()
        else:
            c = Cart.objects.get(
                session_key=session_key, product=Product.objects.get(id=prod_id)
            )
            c.count += 1
            c.save()

    def get_cart_products(session_key):
        res = (
            Cart.objects.select_related()
            .filter(session_key=session_key, is_paid=0)
            .all()
        )
        return res

    def get_total_sum(session_key):
        res = (
            Cart.objects.select_related()
            .filter(session_key=session_key, is_paid=0)
            .all()
        )
        s = 0
        for price in res:
            s += int(price.total_price)
        return s

    def delete_product_from_cart(session_key, id):
        a = Cart.objects.get(session_key=session_key, id=id)
        a.delete()

    def change_cart_product(session_key, id, flag):
        a = Cart.objects.get(session_key=session_key, id=id)
        if flag == "-":
            a.count -= 1
        elif flag == "+":
            a.count += 1
        if a.count == 0:
            a.delete()
        else:
            a.save()

    def get_selecte_product_count(session_key, slug):
        print(slug)
        id = Product.objects.get(slug=slug)
        try:
            a = Cart.objects.get(session_key=session_key, product=id)
            return a.count
        except:
            return 0
        # return a.amount

    def get_products_and_cart_amount(session_key):
        query = f'SELECT * from Perekrestok_product pp left join Perekrestok_cart pc on pp.id=pc.product_id where pc.session_key="{session_key}" or pc.session_key is NULL'
        res = Product.objects.raw(query)
        for el in res:
            if el.count is None:
                print("None found")
                el.count = 0
        if len(res) == 0:
            return Product.objects.all()
        else:
            return res


class WorkingWithProducts:
    def get_all_products(session_key,id):
        if id == "0":
            return Product.objects.all()
        
        query = f'SELECT * from Perekrestok_product pp left join Perekrestok_cart pc on pp.id=pc.product_id where pp.category_id={id} and ( pc.session_key="{session_key}" or pc.session_key is NULL)'
        res = Product.objects.raw(query)
        for el in res:
            if el.count is None:
                print("None found")
                el.count = 0
        if len(res) == 0:
            return Product.objects.all()
        else:
            return res
