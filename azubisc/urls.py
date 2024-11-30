
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Azubi Shopping Cart API',
        default_version='v1',
        description='API endpoints for Azubi shopping cart',
        contact=openapi.Contact(email='ecobblah2@gmail.com'),
        license=openapi.License(name='MIT License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0))
]

admin.site.site_header = 'Azubi Shopping Cart API'
admin.site.site_title = 'Azubi Shopping Cart API Admin Portal'
admin.site.index_title = 'Welcome to Azubi Shoping Cart Admin Portal'
