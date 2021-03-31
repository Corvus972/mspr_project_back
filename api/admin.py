from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from api.resource import *


class OrderInLine(admin.TabularInline):
    """
    Order Items
    """
    model = OrderItems
    readonly_fields = ('product', 'quantity',)
    fields = ('product', 'quantity',)

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Order)
class OrderViews(admin.ModelAdmin):
    """
    Order
    """
    list_display = ('date', 'status', 'user',)
    list_filter = ['date']
    date_hierarchy = 'date'
    inlines = [OrderInLine]
    search_fields = ('user__username',)
    ordering = ('status',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all()
        # return qs.all().exclude(Q(status="PendingPayment"))

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Product
    """
    resource_class = ProductResource
    # GET
    list_display = ('product_name', 'product_price',
                    'description', 'quantity', 'sku', 'image')

    # POST
    fieldsets = (
        ('Informations requises', {
            'fields': ('product_name', 'product_price', 'description', 'quantity', 'sku', 'image')
        }),
    )

    # filter queryset
    def get_queryset(self, request):
        # for super admin
        if request.user.is_authenticated and request.user.is_superuser:
            qs = super(ProductAdmin, self).get_queryset(request)
            return qs
        else:
            # for admin
            qs = super(ProductAdmin, self).get_queryset(request)
            return qs.filter(product__name=request.user)


@admin.register(SalesRule)
class SalesRuleAdmin(admin.ModelAdmin):
    """
    SalesRule
    """
    # GET
    list_display = ('name', 'description',
                    'from_data', 'to_data', 'coupon_code', 'discount_amount', 'products_list')

    # POST
    fieldsets = (
        ('Informations requises', {
            'fields': (
                'name', 'description', 'from_data', 'to_data', 'coupon_code', 'discount_amount', 'product_associated')
        }),
    )

    # get product name to associate it to the coupon
    def product_associated(self, obj):
        return obj.product_associated

    # product_associated.empty_value_display = 'api.Product.None'
    def get_queryset(self, request):
        # for super admin
        if request.user.is_authenticated and request.user.is_superuser:
            qs = super(SalesRuleAdmin, self).get_queryset(request)
            return qs
        else:
            # for admin
            qs = super(SalesRuleAdmin, self).get_queryset(request)
            return qs.filter(SalesRuleAdmin=request.user)
