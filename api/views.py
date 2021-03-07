from django.shortcuts import render
from rest_framework import viewsets

from .serializers import ProductSerializer, SaleRuleSerializer
from api.models.product import Product
from api.models.sales_rule import SalesRule
from rest_framework import generics

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('product_name')
    serializer_class = ProductSerializer


class SalesRuleViewSet(viewsets.ModelViewSet):
    queryset = SalesRule.objects.all()
    serializer_class = SaleRuleSerializer


class SaleProduct(generics.ListAPIView):
    serializer_class = SaleRuleSerializer

    def get_queryset(self):
        product_associated = self.kwargs['product_associated']
        return SalesRule.objects.filter(product_associated=product_associated)
