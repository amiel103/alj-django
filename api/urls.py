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
from core.views import TotalSalesAPIView, GetCategoryView , GetProducts , ProductAdd,  SalesAdd
from core.views import GetMonth, SalesItem , MaterialsGet , GetTopCategories, GetSalesData ,UserLogin , VerifyToken , UpdatePassword

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/', TestView.as_view()),
    path('api/user-login/', UserLogin.as_view(), name='user_login'),
    path('api/user-update/', UpdatePassword.as_view(), name='user_login'),
    path('api/total-sales/', TotalSalesAPIView.as_view(), name='total_sales'),
    path('api/category/', GetCategoryView.as_view(), name='category'),
    path('api/category-update/', GetCategoryView.as_view(), name='category_update'),
    path('api/product-get-all/', GetProducts.as_view(), name='products'),
    path('api/product-update/', GetProducts.as_view(), name='update_product'),
    path('api/product-add/', ProductAdd.as_view() , name='add_product'),
    path('api/product-delete/', ProductAdd.as_view() , name='delete_product'), 
    path('api/sales-add/', SalesAdd.as_view() , name='sales_add'), 
    path('api/sales-get-all/', SalesAdd.as_view() , name='sales_get_all'), 
    path('api/sales-item-get/', SalesItem.as_view() , name='salesItem_get'), 
    path('api/materials-get-all/', MaterialsGet.as_view() , name='materials_get'), 
    path('api/materials-update/', MaterialsGet.as_view() , name='materials_get'),  
    path('api/get-top-categories/', GetTopCategories.as_view() , name='materials_get'),  
    path('api/get-sales-data/', GetSalesData.as_view() , name='materials_get'),  
    path('api/get-month-data/', GetMonth.as_view() , name='materials_get'),  
    path('api/api/auth/me', VerifyToken.as_view() , name='materials_get'),  
]
