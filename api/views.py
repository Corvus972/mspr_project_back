from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order
from .serializers import ProductSerializer, CustomUserSerializer, MyTokenObtainPairSerializer, SaleRuleSerializer, \
    OrderSerializer
from api.models.custom_user import CustomUser
from api.models.product import Product
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from api.models.sales_rule import SalesRule
from rest_framework import generics
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product
    """
    permission_classes = (AllowAny,)
    queryset = Product.objects.all().order_by('product_name')
    serializer_class = ProductSerializer
    lookup_field = "sku"


class SalesRuleViewSet(viewsets.ModelViewSet):
    """
    SalesRule
    """
    permission_classes = (AllowAny,)
    queryset = SalesRule.objects.all()
    serializer_class = SaleRuleSerializer


class SaleProduct(generics.ListAPIView):
    """
    SalesProduct
    """
    permission_classes = (AllowAny,)
    serializer_class = SaleRuleSerializer

    # filter queryset
    def get_queryset(self):
        product_associated = self.kwargs['product_associated']
        return SalesRule.objects.filter(product_associated=product_associated)


class CustomUserViewSet(CreateModelMixin, GenericViewSet):
    """
    Create User
    """
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    # filter queryset
    def get_queryset(self):
        return self.queryset.exclude(is_staff=True)

    # hash password
    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)


class MeViewSet(RetrieveModelMixin, GenericViewSet, UpdateModelMixin, DestroyModelMixin):
    """
    Update and Get user authenticated
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    # retrieve user
    def get_object(self):
        return self.request.user

    # overwrite update method
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    # hash password but passwords are not required
    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Handle Token
    """
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    lookup_field = 'pk'


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order
    """
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # filter queryset
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    # save user directly in order
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
