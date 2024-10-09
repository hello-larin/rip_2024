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

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'products/', views.laboratory_catalog, name='laboratory-catalog'),
    path(r'carts/', views.laboratory_carts, name='laboratory-carts'),
    path(r'products/<int:id>/', views.laboratory_product, name='laboratory-product'),
    #path(r'products/<int:id>/put/', views.put, name='product-put'),
    path(r'products/<int:id>/add', views.add_item, name='add-item'),
    path(r'carts/<int:id>/', views.laboratory_cart, name='laboratory-cart'),
    path(r'carts/<int:id>/submit/', views.submit_cart, name='submit-cart'),
    path(r'carts/<int:id>/accept/', views.accept_cart, name='accept-cart'),
    path(r'item/<int:id>/', views.one_item, name='laboratory_item'),
    path(r'user/', views.user_registration, name='registration'),
    path(r'auth/', views.user_auth, name='auth'),
    path(r'logout/', views.user_deauth, name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]