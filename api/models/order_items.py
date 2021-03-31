from django.db import models


class OrderItems(models.Model):
    """
    Order Items Model
    """
    order = models.ForeignKey("Order",
                              related_name='items',
                              on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey("Product",
                                null=True,
                                related_name='order_items',
                                on_delete=models.CASCADE)

    class Meta:
        app_label = 'api'
        ordering = ('id',)
        verbose_name = 'Produits Commandés'
        verbose_name_plural = 'Produits Commandés'

    def __unicode__(self):
        return self.id

    def get_product(self):
        return self.product

    def get_cost(self):
        return self.get_product().product_price * self.quantity
