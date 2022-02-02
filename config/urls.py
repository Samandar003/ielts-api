from rest_framework.permissions import AllowAny
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from 

schema_view = get_schema_view(
    openapi.Info(
        title='IELTS Api',
        default_version='v1',
        description='Swagger docs for REST API',
        contact=openapi.Contact('Samandar Shiyimov <Samandar200527@gmail.com>')
    ),
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('auth/', obtain_auth_token),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
]
