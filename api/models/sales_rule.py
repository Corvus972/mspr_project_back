from django.db import models


class SalesRule(models.Model):
    name = models.CharField(
        max_length=30, verbose_name="Nom du coupon")
    description = models.CharField(max_length=500)
    from_data = models.DateField(verbose_name="Date de début")
    to_data = models.DateField(verbose_name="Date de fin")
    coupon_code = models.CharField(
        max_length=30, verbose_name="Code du coupon")
    discount_amount = models.IntegerField(default=0, verbose_name="Remise")
    product_associated = models.ManyToManyField(
        'Product', verbose_name="produits", related_name='salesrule', blank=True)

    def __str__(self):
        return self.name

    def products_list(self):
        return ', '.join([a.product_name for a in self.product_associated.all()])
