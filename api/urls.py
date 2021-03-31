from django.urls import include, path
from rest_framework import routers
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.conf.urls import url

# Default router
router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='product')  # product
router.register(r'salesrule', SalesRuleViewSet, basename='salesrules')  # salesrule
router.register(r'users', CustomUserViewSet, basename='users')  # users
router.register(r'orders', OrderViewSet, basename='orders')  # orders

me_routing = MeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('ruleproduct/<product_associated>',
         SaleProduct.as_view(), name='saleproduct'),  # salesproduct
    path('login/', MyTokenObtainPairView.as_view(), name='token_create'),  # get token
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # verify token
    url(r'me/', me_routing, name='me')  # user authenticated
]
