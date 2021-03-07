from rest_framework import serializers

from api.models.product import Product
from api.models.sales_rule import SalesRule


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Product
        fields = ('id', 'product_name', 'product_price', 'description',
                  'quantity', 'created_at', 'sku', 'image')


class SaleRuleSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = SalesRule
        fields = ('id', 'name', 'description', 'from_data', 'to_data',
                  'coupon_code', 'discount_amount', 'product_associated')
