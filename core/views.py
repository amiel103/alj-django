from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Category, Products, Sales, salesItems
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Sum



class TestView(APIView):
    def get(self, request, sales_id):
        sales = Sales.objects.get(pk=sales_id)
        sales_items = sales.salesitems_set.all()
        total = sum(item.total for item in sales_items)
        return Response({'total_items': total})
    

class TotalSalesAPIView(APIView):
    def get(self, request, format=None):
        total_sales = Sales.objects.aggregate(total_sales=Sum('grand_total'))
        return Response({'total_sales': total_sales['total_sales']})
    

class GetCategoryView(APIView):
    def get(self, request, format=None):
      # Retrieve all categories from the database
      all_categories = Category.objects.all()

      # Create a list to store dictionaries containing values of each category
      categories_data = []

      # Iterate through each category and extract its values
      for category in all_categories:
          category_data = {
              'id': category.id,
              'name': category.name,
              'description': category.description,
              'status': category.status,
              'date_added': category.date_added,
              'date_updated': category.date_updated
          }
          categories_data.append(category_data)

      return Response(categories_data)

# Create your views here.
class GetProducts(APIView):
    def get(self, request, format=None):
        all_products = Products.objects.all()
        products_data = []

        # Iterate through each product and extract its values
        for product in all_products:
            product_data = {
                'id': product.id,
                'code': product.code,
                'category_id': product.category_id.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'status': product.status,
                'date_added': product.date_added,
                'date_updated': product.date_updated
            }
            products_data.append(product_data)

        # Return JSON response containing all products
        return Response(products_data)
    
    
    


    def post(self,request):
        # Get the product instance
        
        
        product = get_object_or_404(Products, pk=request.data['id'])

        # Update the product data
        if request.method == 'POST':
            serializer = ProductSerializer(product, data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'error': 'Method not allowed'}, status=405)