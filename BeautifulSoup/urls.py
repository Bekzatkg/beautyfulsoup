from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from main.views import PostViewSet, ReviewViewSet


schema_view = get_schema_view(
    openapi.Info(
      title="BeautifulSoup API",
      default_version='v1',
      description="...",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
    public=True,
    permission_classes=(AllowAny, ),
)

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('review', ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('account/', include('account.urls')),
    path('profile/', include('myprofile.urls')),
    path('api/v1/', include('main.urls')),
    path('api/v1/', include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
