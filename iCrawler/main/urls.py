from django.urls import path, include
from django.urls import path, include
from . import views
from django.contrib.auth import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Price Tracker API')

router = DefaultRouter()
router.register('scrapy_app', ContractNoticeViewSet)


urlpatterns = [
    #path('', first_view, name='track-home'),
    path('', index, name='index'),
    path('api/', include(router.urls)),
    path('all/', ContractNoticetListView.as_view(), name='track-list-all-scrapy_apps'),
    path('user/<str:username>', UserContractNoticeListView.as_view(), name='user-scrapy_apps'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    #path('api-docs/', schema_view, name="api-docs"),
    # path('logout/', views.LogoutView.as_view(), {"next_page": '/'}),
    path('api-token-auth/', obtain_auth_token),

]