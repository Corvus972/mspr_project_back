from django.db import models

STATUS_CHOICES = (
    ('Ordered', 'Ordered'),
    ('Preparation', 'Preparation'),
    ('Done', 'Done'),
    ('Canceled', 'Canceled'),
)


class Order(models.Model):
    """
    Order Model
    """
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Ordered")
    user = models.ForeignKey("CustomUser",
                             related_name='order_user',
                             on_delete=models.CASCADE,
                             null=True)

    class Meta:
        app_label = 'api'
        ordering = ('-date',)
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return f'{self.id}'

    @property
    def yearpublished(self):
        return self.date.strftime('%Y')

    @property
    def monthpublished(self):
        return self.date.strftime('%m')

    def get_number_products(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    get_total_cost.short_description = 'TTC'

    def get_articles(self):
        return [item.get_article() for item in self.items.all()]