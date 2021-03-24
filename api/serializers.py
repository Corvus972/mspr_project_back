from rest_framework import serializers
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

