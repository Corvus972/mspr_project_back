from django.db import models

from api.models import Order, Product


class OrderItems(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product,
                                null=True,
                                related_name='orders_items',
                                on_delete=models.CASCADE)

    class Meta:
        app_label = 'order'
        ordering = ('name',)
        verbose_name = 'Produits Commandés'
        verbose_name_plural = 'Produits Commandés'

    def __str__(self):
        return self.product.product_name

    def get_product(self):
        return self.product

    def get_cost(self):
        return self.get_product().product_price * self.quantity
