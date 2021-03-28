from django.db import models
from django.utils.html import format_html
from api.helpers import RandomFileName
# Product model


class Product(models.Model):
    product_name = models.CharField(
        max_length=30, verbose_name="Nom du produit")
    product_price = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=100, verbose_name="Prix du produit")
    description = models.CharField(max_length=500, default="Pas de description pour l'instant")
    quantity = models.IntegerField(default=0, verbose_name="Quantité")
    created_at = models.DateField(auto_now=True, verbose_name="Créée le")
    sku = models.CharField(max_length=30)
    image = models.ImageField(
        upload_to=RandomFileName('img/'), null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_img(self):
        if self.image:
            return format_html('<img src="{url}" width="50" height="50" />'.format(
                url=self.image.url
            ))
        else:
            return format_html('<img src="{url}" width="50" height="50" />'.format(
                url='/media/img/defaultphoto.png'
            ))

    get_img.short_description = 'Image'
    get_img.allow_tags = True
