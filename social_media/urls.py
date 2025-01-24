from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static
# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Social Media API",
        default_version="v1",
        description="API documentation for the Social Media backend.",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('social.urls')),  # Include the URLs from the 'social' app
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
