from rest_framework import serializers

from api.models import OrderItems, Order
from api.models.product import Product
from api.models.sales_rule import SalesRule
from api.models.custom_user import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ProductSerializer(serializers.HyperlinkedModelSerializer):

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
            item['product_price'] = str(float(item['product_price']) - (float(item['product_price']) / data['discount_amount']))
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
        fields = ["pk", ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = {
                "id": instance.product.id,
                "name": instance.product.product_name,
                "price": instance.product.product_price,
                "quantity": instance.quantity,
            }

        return response


class OrderSerializer(serializers.ModelSerializer):
    items = ItemsSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Order
        ordering = ['date']
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = {
            "email": instance.user.email,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
        }
        return response

    # def create(self, validated_data):
    #     print('self:', self)
    #     print('validated_data:', validated_data)
    #     instance = Order.objects
    #     items_data = validated_data.pop('items')
    #     items = instance.all()
    #
    #     instance.date = validated_data.get('date', instance.date)
    #     instance.unique_number = validated_data.get('unique_number', instance.unique_number)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
    #     instance.billing_address = validated_data.get('billing_address', instance.billing_address)
    #     instance.save()
    #
    #     for item in items_data:
    #         qs_article = Article.objects.filter(article_code=item.get('article_code'))
    #         if qs_article.exists():
    #             article = items[0]
    #             article.article_code = item.get('article_code', article.article_code)
    #             article.name = item.get('name', article.name)
    #             article.barcode = item.get('barcode', article.barcode)
    #             article.price_without_taxes = item.get('price_without_taxes', article.price_without_taxes)
    #             article.quantity = item.get('quantity', article.quantity)
    #             article.rate_VAT = item.get('rate_VAT', article.rate_VAT)
    #             article.price_by_kg_without_taxes = item.get('price_by_kg_without_taxes', article.price_by_kg_without_taxes)
    #             article.save()
    #     return instance