from rest_framework import serializers

from api.models.product import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_price', 'description',
                  'quantity', 'created_at', 'sku', 'image')
