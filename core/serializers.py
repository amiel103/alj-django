from rest_framework import serializers
from .models import Products , Category , Sales , salesItems, Materials, CustomUser

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class SalesItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = salesItems
        fields = '__all__'

class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = ['stock'] 


class MaterialsSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ['password']

