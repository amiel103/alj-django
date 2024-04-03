"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from core.views import TestView 
from core.views import TotalSalesAPIView, GetCategoryView , GetProducts


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/', TestView.as_view()),
    path('api/total-sales/', TotalSalesAPIView.as_view(), name='total_sales'),
    path('api/category/', GetCategoryView.as_view(), name='category'),
    path('api/get-products/', GetProducts.as_view(), name='products'),
    path('api/update-product/', GetProducts.as_view(), name='update_product'),
    
    
]
