"""
URL configuration for larin_rest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from laboratory import views
from django.urls import include, path
from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Лабороторное оборудование API",
      default_version='v1',
      description="Апи для оформления закупок лабораторного оборудования",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@labeq.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   #permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'equipment/', views.laboratory_catalog.as_view(), name='laboratory-catalog'),
    path(r'procurements/', views.laboratory_procurements.as_view(), name='laboratory-procurements'),
    path(r'equipment/<int:id>/', views.laboratory_equipment.as_view(), name='laboratory-equipment'),
    path(r'equipment/<int:id>/add', views.add_item, name='add-item'),
    path(r'procurements/<int:id>/', views.laboratory_procurement.as_view(), name='laboratory-procurement'),
    path(r'procurements/<int:id>/submit/', views.submit_procurement, name='submit-procurement'),
    path(r'procurements/<int:id>/accept/', views.accept_procurement, name='accept-procurement'),
    path(r'item/<int:id>/', views.one_item.as_view(), name='laboratory_item'),
    path(r'user/', views.user_registration.as_view(), name='registration'),
    path(r'registration/', views.register, name='reg'),
    path('login', views.user_auth, name='login'),
    path('logout', views.user_deauth, name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]