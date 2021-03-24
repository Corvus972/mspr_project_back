from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer, CustomUserSerializer, MyTokenObtainPairSerializer, SaleRuleSerializer
from api.models.custom_user import CustomUser
from api.models.product import Product
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from api.models.sales_rule import SalesRule
from rest_framework import generics


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all().order_by('product_name')
    serializer_class = ProductSerializer


class SalesRuleViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = SalesRule.objects.all()
    serializer_class = SaleRuleSerializer


class SaleProduct(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SaleRuleSerializer

    def get_queryset(self):
        product_associated = self.kwargs['product_associated']
        return SalesRule.objects.filter(product_associated=product_associated)


class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all().order_by('id').exclude(is_staff=True)
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        # Hash password but passwords are not required
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
