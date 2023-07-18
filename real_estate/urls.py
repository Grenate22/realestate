from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair' ),
    path('api/token/refresh/',TokenRefreshView.as_view(), name='token_refresh' ),
    path('admin/', admin.site.urls),
    path('api/',include('accounts.urls')),
    path('api/',include('realtors.urls')),
    path('api/',include('listings.urls')),
    path('api/',include('contacts.urls')),
    path('docs/',include_docs_urls(title='RealestateApi')),
    path('schema', get_schema_view(title="RealestateApi",description="Api for realestate",version="1.0.0"),name='openapi-schema'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
