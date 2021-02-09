from django.contrib import admin
from api.models.product import Product
from django.contrib import admin

# Register your models here.


@admin.register(Product)
class MyModelProduct(admin.ModelAdmin):
    # GET
    list_display = ('product_name', 'product_price',
                    'description', 'quantity', 'created_at', 'sku', 'image')
    # POST
    fieldsets = (
        ('Informations requises', {
            'fields': ('product_name', 'product_price', 'description', 'quantity', 'created_at', 'sku', 'image')
        }),
    )

    def get_queryset(self, request):
        # for super admin
        if request.user.is_authenticated and request.user.is_superuser:
            qs = super(MyModelProduct, self).get_queryset(request)
            return qs
        else:
            # for admin
            qs = super(MyModelProduct, self).get_queryset(request)
            return qs.filter(product__name=request.user)
