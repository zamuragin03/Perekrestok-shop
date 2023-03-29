from Perekrestok.models import Costumer_Info
class WorkingWithCostumers():
    def create_costumer(phone, name, email):
        if len(Costumer_Info.objects.filter(phone=phone)) == 0:
            user = Costumer_Info(phone=phone, name=name, email=email)
            user.save()