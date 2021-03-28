from django.urls import include, path
from rest_framework import routers
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='product')
router.register(r'salesrule', SalesRuleViewSet, basename='salesrules')
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('ruleproduct/<product_associated>',
         SaleProduct.as_view(), name='saleproduct'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_create'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
