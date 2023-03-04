from rest_framework import serializers
from .models import *
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title','price','amount','description')