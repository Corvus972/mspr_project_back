from decimal import Decimal

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

    def create(self, validated_data):
        """ Creates and returns a new user """
        # Validating Data
        user = CustomUser(
            is_superuser=validated_data['is_superuser'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            address_line_1=validated_data['address_line_1'],
            address_line_2=validated_data['address_line_2'],
            zip_code=validated_data['zip_code'],
            city=validated_data['city'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
        )

        user.set_password(validated_data['password'])
        user.save()
        print(user.password)
        return user


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
        # token['email'] = user.email
        # token['id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['user_id'] = self.user.id
        data['super_user'] = self.user.is_superuser
        # data['groups'] = self.user.groups.values_list('name', flat=True)
