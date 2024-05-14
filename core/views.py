from django.shortcuts import render
from datetime import timedelta
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import Category, Products, Sales, salesItems , Materials, CustomUser
from .serializers import ProductSerializer , CategorySerializer, SalesItemsSerializer ,SalesSerializer ,MaterialsSerializer, MaterialsSerializer2
from .serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings

# from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_simplejwt.backends import TokenBackend

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# Obtain the JWT encoder
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class UserLogin(APIView):
    def post(self, request):
        user = get_object_or_404(CustomUser, email=request.data['email'])

        if user.password == request.data['password'] :
            print("correct")
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            data = {
                'accessToken': token,
                'user':{
                    "displayName": user.first_name +" "+ user.last_name,
                    "email": user.email,
                    "id": user.id,
                    "role": user.role
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UpdatePassword(APIView):
    def post(self, request):
        user = get_object_or_404(CustomUser, id=request.data['id'])

        if request.method == 'POST':
            serializer = CustomUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'error': 'Method not allowed'}, status=405)
        
class VerifyToken(APIView):
    def get(self, request):
        # print("fuck off bitch")        

        # text = request.headers.get('Authorization')
        # print(text)

        return Response( jwt_decode_handler( request.GET['id'] ) )
        # return Response('yawa')

        # data = {'token': request.GET['id']}
        # valid_data = VerifyJSONWebTokenSerializer().validate(data)
        # user = valid_data['user']
        
        # return Response({'token': user})
        
        # print(request.META)
        # token = request.META.get('HTTP_AUTHORIZATION')
        # token = request.headers.get('Authorization')

        return Response( token )
        # print( jwt_decode_handler(token) )
        # data = {'token': token}
        # try:
        #     valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
        #     user = valid_data['user']
        #     request.user = user
        # except ValidationError as v:
        #     print("validation error", v)

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
    
    def post(self,request):
        # Get the product instance
        category = get_object_or_404(Category, pk=request.data['id'])

        # Update the product data
        if request.method == 'POST':
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'error': 'Method not allowed'}, status=405)

class GetProducts(APIView):
    def get(self, name, format=None):
        all_products = Products.objects.all()
        products_data = []

        # Iterate through each product and extract its values
        for product in all_products:
            product_data = {
                'id': product.id,
                'code': product.code,
                'category_id': product.category_id.name,
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
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'error': 'Method not allowed'}, status=405)

class ProductAdd(APIView):
    def post(self,request):
        if request.method == 'POST':
            serializer = ProductSerializer(data=request.data)

            print(request.data)

            if serializer.is_valid():
                # 
                serializer.save()

            if(request.data['category_id'] == 11):


                lastProduct = Products.objects.last()
                print('--------------------------')
                print(lastProduct)
                data = {
                    "product_id":lastProduct.id,
                    "stock":20
                }
                print(data)
                ms = MaterialsSerializer2(data = data)
                print(ms)

                if ms.is_valid():
                    ms.save()
                    print(ms.data)

                print(ms.errors)
            return Response("inserted")

class ProductDelete(APIView):
    def post(self,request):
        if request.method == 'POST':

            # serializer = ProductSerializer(data=request.data)

            # print(request.data)
            try:
                print("yeah ========================")
                print(request.data['id'])
                product = Products.objects.get(id=request.data['id'])
                product.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except: 
                return Response(status=status.HTTP_404_NOT_FOUND)

class SalesAdd(APIView):
    def post(self,request):
        if request.method == 'POST':
            prod = Sales()
            # print(request.data)
            serializer = SalesSerializer(data=request.data['sales'])
            if serializer.is_valid():
                serializer.save()
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
            last_sale = Sales.objects.last()

            for x in request.data['cart']:

                item = get_object_or_404(Products, pk=x['productId'])

                if(item.category_id.name == 'ETC'):
                    material  = get_object_or_404(Materials, product_id=item.id)
                    material.stock = material.stock - int(x['quantity'])
                    material.save()

                    ms = MaterialsSerializer(data = material)
                    if ms.is_valid():
                        ms.save()
                        print('yeeahg')
                    print(ms.data)
                data = {
                    "sale_id": last_sale.id,
                    "product_id": x['productId'],
                    "price": x['price'],
                    "qty": x['quantity'],
                    "total": x['total']
                }
                
                serializerItems = SalesItemsSerializer(data=data)

                if serializerItems.is_valid():
                    serializerItems.save()

            data = {
                "id": last_sale.id,
                "date": last_sale.date_added
            }
            return Response( data ) 
        
    def get(self, name, format=None):
        sales = Sales.objects.all()
        sales_data = []

        # Iterate through each product and extract its values
        for x in sales:
            product_data = {
                'id': x.id,
                'grand_total': x.grand_total,
                'tendered_amount': x.tendered_amount,
                'amount_change': x.amount_change,
                'date':x.date_added
            }
            sales_data.append(product_data)

    # Return JSON response containing all products
        return Response(sales_data)
        
class SalesItem(APIView):
    def get(self, request, format=None):
        print(request.GET['id'])
        sales_items = salesItems.objects.filter(sale_id=request.GET['id'])
        items = []
        for item in sales_items:
            data = {
                "id":item.id,
                "sale_id": item.sale_id.id,
                "product_id": item.product_id.name,
                "price": item.price,
                "qty": item.qty,
                "total": item.total,
                "date_added": item.date_added
            }

            items.append(data)
        
        print(items)
        return Response(items)
    
class MaterialsGet(APIView):
    def get(self, name, format=None):
        all_products = Materials.objects.all()
        products_data = []

        print('yeah')

        # Iterate through each product and extract its values
        for item in all_products:
            product_data = {
                'id': item.id,
                'name': item.product_id.name,
                'description': item.product_id.description,
                'stock': item.stock,
            }
            products_data.append(product_data)

        # Return JSON response containing all products
        return Response(products_data)
        
    def post(self,request):
    # Get the product instance
        product = get_object_or_404(Materials, pk=request.data['id'])

        print(request.data)

        # Update the product data
        if request.method == 'POST':
            serializer = MaterialsSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(serializer.data)
            
            print(serializer.errors)
            return Response(serializer.errors)
        else:
            return Response({'error': 'Method not allowed'}, status=405)  
        
class GetTopCategories(APIView):
    def get(self, name, format=None):

        category_sales = salesItems.objects.values('product_id__category_id__name')

        data = {}
        # data = {}
        for x in category_sales:
            try:
                data[x["product_id__category_id__name"]] += 1
            except:
                data[x["product_id__category_id__name"]] = 0


        converted_data = [{"label": key, "value": value} for key, value in data.items() if value != 0]

        # print(converted_data)
        # Return JSON response containing all products
        return Response(converted_data)

class GetSalesData(APIView):
    def get(self, name, format=None):
        all_data = Sales.objects.all()

        today = timezone.now().date()
        previous_day = today - timedelta(days=1)
        last_month = today - timedelta(days=30)


        total_current_day = Sales.objects.filter(date_added__date=today).aggregate(total_current_day=Sum('grand_total'))['total_current_day'] or 0
        total_previous_day = Sales.objects.filter(date_added__date=previous_day).aggregate(total_previous_day=Sum('grand_total'))['total_previous_day'] or 0
        total_last_month = Sales.objects.filter(date_added__date__gte=last_month, date_added__date__lt=today).aggregate(total_last_month=Sum('grand_total'))['total_last_month'] or 0


        data = {
            "today": total_current_day,
            "previous": total_previous_day,
            "month": total_last_month
        }

        return Response(data)
    
class GetMonth(APIView):
    def get(self, name, format=None):
        today = timezone.now().date()
        dates = [today - timedelta(days=i) for i in range(30)]

        # Query Sales data for each date
        sales_data = Sales.objects.filter(date_added__date__in=dates).values('date_added__date').annotate(total_sales=Sum('grand_total'))


        # Initialize labels and series
        labels = []
        sales_series = []

        # Populate labels and series
        for date in dates:
            label = date.strftime('%m/%d/%Y')
            labels.append(label)
            
            # print("sales "  ,next(item['total_sales'] for item in sales_data if item['date_added__date'] == date))
            sales_total = next((item['total_sales'] for item in sales_data if item['date_added__date'] == date), 0)

            sales_series.append(sales_total)

        # Format the output
        output = {
            'labels': labels,
            'series': [
                {
                    'name': 'Sales',
                    'type': 'column',
                    'fill': 'solid',
                    'data': sales_series,
                },

            ]
        }

        return Response(output)
    
