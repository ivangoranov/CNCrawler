from django.conf.urls import url
from django.urls import path, include
from django.urls import path, include
from django.contrib.auth.views import LoginView, UserModel, LogoutView
from rest_framework import views as r_views, permissions
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import *
from .forms import AuthenticationForm

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Contract Tender Notice Scraper API",
      default_version='v1',
      description="Crawling website to collect contract notice data",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ivan1goranov@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

#router = DefaultRouter()
##router.register('list_all', ContractNoticeViewSet)
#router.register('contract_notices', views.HomeView)
#for r in router.get_urls():
#    print(r)

urlpatterns = [
    #path('', first_view, name='track-home'),
    path('', index, name='index'),
    path('contract_notice_api/', apiOverview, name='contract_notice_api'),
    path('contract_notice_api/list/', noticeList, name='notice_list'),
    path('contract_notice_api/search/<str:date>/', noticeSearch, name='search-by-date'),
    path('contract_notice_api/detail/<str:pk>/', getNoticeListByID, name='detail-by-id'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='registration_form'),
    path('accounts/profile/', index, name='index'),
    path('logout/', LogoutView.as_view(), {"next_page": '/'}),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #path('api-token-auth/', obtain_auth_token),

]