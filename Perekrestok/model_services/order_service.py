from Perekrestok.models import *


class WorkingWithOrder:
    def create_order(name, address, phone, payment_id, session_id):
        order = Order()
        order.save()
        prods = Cart.objects.filter(session_key=session_id, is_paid=False)
        for prod in prods:
            prod.order_id = order.id
            prod.save()
        statuses = Order_Status.objects.all()
        user = Costumer_Info.objects.get(phone=phone)
        user.save()
        payment = PaymentType.objects.get(id=payment_id)
        o = Orders_Info(
            order=order,
            address=address,
            costumer=user,
            payment=payment,
            status=statuses[0],
        )
        o.save()

    def get_order_id(session_id):
        order = Cart.objects.filter(session_key=session_id).order_by("-order_id")
        return order[0].order_id
    def validate_data(name,phone,address,pymntType,email,context):
        props = {
            "Имя": str(name).strip(),
            "Телефон": str(phone).strip(),
            "Адрес": str(address).strip(),
            "Тип оплаты": str(pymntType).strip(),
            "Почта": str(email).strip(),
        }
        for key, value in props.items():
            if value == "" or value == "None":
                context["error_message"] = f"Заполите поле {key}"
                context["title"] = "Проверьте поля"
                context["name"] = name
                context["phone"] = phone
                context["address"] = address
                context["email"] = email
                if pymntType is not None:
                    context["payment"] = int(pymntType)
                return context
        
