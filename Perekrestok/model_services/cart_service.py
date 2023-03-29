from Perekrestok.models import *


class WorkingWithCart:
    def add_to_cart(session_key, prod_id):
        c = Cart.objects.filter(
            session_key=session_key,
            product=Product.objects.get(id=prod_id),
            order_id__isnull=True,
        ).all()
        print(c)
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
                session_key=session_key,
                product=Product.objects.get(
                    id=prod_id,
                ),
                is_paid=False,
            )
            c.count += 1
            c.save()

    def get_cart_products(session_key):
        res = (
            Cart.objects.select_related()
            .filter(session_key=session_key, is_paid=0)
            .all()
        )
        print(res)
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

    def get_overall_count(session_key):
        total_count = 0
        prods = Cart.objects.filter(session_key=session_key, is_paid=False)
        for prod in prods:
            total_count += prod.count
        return total_count

    def has_cart_products(session_key):
        return len(Cart.objects.filter(session_key=session_key, is_paid=False)) > 0

    def get_products_and_cart_amount(session_key):
        query = """
        SELECT 
            pp.id, 
            pp.title, 
            pp.price, 
            pp.amount,
            pp.picture,
            pp.description,
            pp.slug,
            pp.category_id,
            pc.id,
            pc.session_key, 
            IFNULL(pc.count, 0) as count ,
            pc.is_paid,
            pc.total_price,
            pc.order_id, 
            pc.product_id 
            from Perekrestok_product  pp left join Perekrestok_cart pc on pp.id=pc.product_id and pc.is_paid=0
            where ( pc.session_key="{session_key}" or pc.session_key is NULL) order by pp.id"""
        res = Product.objects.raw(query)
        for el in res:
            if el.count is None:
                # print("None found")
                el.count = 0
        if len(res) == 0:
            return Product.objects.all()
        else:
            return res

    def finish_cart(
        session_key,
    ):
        prods = Cart.objects.filter(session_key=session_key, is_paid=False)
        for prod in prods:
            prod.is_paid = True
            prod.save()

    def get_finished_order_products(session_key, order_id):
        return Cart.objects.filter(session_key=session_key, order_id=order_id)

    def get_finished_order_summ(order_id):
        return sum(int(el.total_price) for el in Cart.objects.filter(order_id=order_id))
