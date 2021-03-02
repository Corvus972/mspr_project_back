from django.contrib import admin
from api.models.product import Product
from api.models.sales_rule import SalesRule
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from api.resource import *
# Register your models here.


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
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
            qs = super(ProductAdmin, self).get_queryset(request)
            return qs
        else:
            # for admin
            qs = super(ProductAdmin, self).get_queryset(request)
            return qs.filter(product__name=request.user)


admin.site.register(Product, ProductAdmin)


@admin.register(SalesRule)
class SalesRuleAdmin(admin.ModelAdmin):
    # GET
    list_display = ('name', 'description',
                    'from_data', 'to_data', 'coupon_code', 'discount_amount', 'product_associated')

    # POST
    fieldsets = (
        ('Informations requises', {
            'fields': ('name', 'description', 'from_data', 'to_data', 'coupon_code', 'discount_amount', 'product_associated')
        }),
    )
    # get product name to associate it to the coupon

    def product_associated(self, obj):
        return obj.product_associated

    #product_associated.empty_value_display = 'api.Product.None'

    def get_queryset(self, request):
        # for super admin
        if request.user.is_authenticated and request.user.is_superuser:
            qs = super(SalesRuleAdmin, self).get_queryset(request)
            return qs
        else:
            # for admin
            qs = super(ProductAdmin, self).get_queryset(request)
            return qs.filter(SalesRuleAdmin=request.user)
