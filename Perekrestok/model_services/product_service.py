from Perekrestok.models import *
class WorkingWithProducts():
    def get_all_products(session_key, id):
        if id == "0":
            query = f"""
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
            from Perekrestok_product  pp left join Perekrestok_cart pc on pp.id=pc.product_id and pc.is_paid=0 and pc.session_key="{session_key}"
                        """
            res = Product.objects.raw(query)
            return res
        query = f'''
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
            from Perekrestok_product  pp left join Perekrestok_cart pc on pp.id=pc.product_id and pc.is_paid=0 and pc.session_key="{session_key}"
            where pp.category_id= {id}
			order by pp.id 
        '''
        res = Product.objects.raw(query)
        for el in res:
            if el.count is None:
                el.count = 0
            if el.is_paid == 1:
                el.count = 0
        if len(res) == 0:
            return Product.objects.all()
        else:
            return res

