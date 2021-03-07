from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'salesrule', views.SalesRuleViewSet, basename='salesrules')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # test http://127.0.0.1:8000/ruleproduct/id_in_your_product_associated
    path('ruleproduct/<product_associated>',
         views.SaleProduct.as_view(), name='saleproduct')
]
