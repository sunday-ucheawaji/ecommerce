from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)
from django.conf import settings
from django.conf.urls.static import static
from user_auth.views.auth_view import LogoutView
from user_auth.views.auth_view import LogoutAllView


schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("user_auth.urls")),
    path("products/", include("product.urls")),
    path("orders/", include("order.urls")),
    path("api/stripe/", include("payment.urls")),

    # Auth
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('logout-all', LogoutAllView().as_view(), name='logout-all'),

    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    # documentation
    path('swagger.json', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
