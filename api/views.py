from django.shortcuts import render
from rest_framework import viewsets

from .serializers import ProductSerializer
from api.models.product import Product
from api.models.sales_rule import SalesRule

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('product_name')
    serializer_class = ProductSerializer
