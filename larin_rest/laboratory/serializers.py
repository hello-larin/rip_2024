from rest_framework import serializers
from laboratory.models import *

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryOrder
        fields = ["id", "address", "phone", "created_date", "submited_date", "accepted_date", "status", "user"]


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Модель, которую мы сериализуем
        model = LaboratoryItem
        # Поля, которые мы сериализуем
        fields = ["id", "name", "price", "description", "image"]


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryItem
        fields = ["id", "name", "price"]


class ItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_id.name')
    product_price = serializers.CharField(source='product_id.price')
    class Meta:
        # Модель, которую мы сериализуем
        model = LaboratoryOrderItems
        # Поля, которые мы сериализуем
        fields = ["product_name", "product_price", "amount", "id"]
    

class CartSerializer(serializers.ModelSerializer):
    orders = ItemsSerializer(many=True, read_only=True)
    class Meta:
        model = LaboratoryOrder
        fields = ["id", "address", "phone", "created_date", "submited_date", "accepted_date", "status", "orders"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ["username", "password", "email"]


class EditUserSerializer(serializers.ModelSerializer):
    orders = CartSerializer(many=True, read_only=True)
    class Meta:
        model = AuthUser
        fields = ["first_name", "last_name", "email", "password", "orders"]


class EditCartSerializer(serializers.ModelSerializer):
    orders = ItemsSerializer(many=True, read_only=True)
    class Meta:
        model = LaboratoryOrder
        fields = ["address", "phone", "created_date", "orders"]

class EditItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryOrderItems
        fields = ["id", "product_id", "order", "amount"]