from django.urls import path, include
from django.urls import path, include
from django.contrib.auth.views import LoginView, UserModel
from rest_framework import views as r_views
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import *
from .forms import AuthenticationForm

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Price Tracker API')

router = DefaultRouter()
router.register('list_all', ContractNoticeViewSet)
for r in router.get_urls():
    print(r)

urlpatterns = [
    #path('', first_view, name='track-home'),
    path('', index, name='index'),
    path('api/', include(router.urls)),
    path('api/list/',ContractNoticetListView),
    path('accounts/register/', views.register, name='registration_form'),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('api-docs/', schema_view, name="api-docs"),
    #path('logout/', views.LogoutView.as_view(), {"next_page": '/'}),
    path('api-token-auth/', obtain_auth_token),

]