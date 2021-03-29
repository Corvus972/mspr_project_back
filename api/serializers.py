from typing import List, Sequence
from rest_framework import serializers
from api.models import OrderItems, Order, models
from api.models.product import Product
from api.models.sales_rule import SalesRule
from api.models.custom_user import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = Product
        fields = ('id', 'product_name', 'product_price', 'description',
                  'quantity', 'created_at', 'sku', 'image')


class SaleRuleSerializer(serializers.ModelSerializer):
    product_associated = ProductSerializer(read_only=True, many=True)

    class Meta:
        ordering = ['-id']
        model = SalesRule
        fields = ('id', 'name', 'description', 'from_data', 'to_data',
                  'coupon_code', 'discount_amount', 'product_associated')

    def to_representation(self, instance):
        data = super(SaleRuleSerializer, self).to_representation(instance)
        for item in data['product_associated']:
            item['product_price'] = str(
                float(item['product_price']) - (float(item['product_price']) / data['discount_amount']))
        return data


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('password', 'is_superuser',
                  'last_name', 'first_name', 'address_line_1',
                  'address_line_2', 'zip_code', 'city', 'email',
                  'phone_number')


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Token Serializer
    """

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['user_id'] = self.user.id
        data['super_user'] = self.user.is_superuser
        return data


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class ItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItems
        fields = ['quantity', 'product']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = {
            "id": instance.product.id,
            "product_name": instance.product.product_name,
            "product_price": str(instance.product.product_price),
            "description": instance.product.description,
            "quantity": instance.product.quantity,
            "created_at": instance.product.created_at,
            "sku": instance.product.sku,
            "image": ""
        }
        return response


class OrderSerializer(serializers.ModelSerializer):
    items = ItemsSerializer(many=True, read_only=False, required=False)
    product = ProductSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Order
        ordering = ['date']
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = {
            "email": instance.user.email,
            "first_name": instance.user.first_name,
            "address_line_1": instance.user.address_line_1,
            "address_line_2": instance.user.address_line_2,
            "zip_code": instance.user.zip_code,
            "city": instance.user.city,
        }
        return response

    def create(self, validated_data):
        list_items: List = validated_data.pop('items')
        order: Order = Order.objects.create(**validated_data)
        for item in list_items:
            # add items
            OrderItems.objects.create(order=order, **item)

            # decrease quantity
            Product.objects.filter(product_name=item.get('product', None)).update(
                quantity=models.F('quantity') - item.get('quantity', None)
            )
        return order
