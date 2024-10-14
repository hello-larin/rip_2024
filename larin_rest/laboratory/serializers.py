from rest_framework import serializers
from laboratory.models import *

class OrdersSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = LaboratoryOrder
        fields = ["id", "address", "phone", "created_date", "submited_date", "accepted_date", "status", "user"]


class EquipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Модель, которую мы сериализуем
        model = LaboratoryItem
        # Поля, которые мы сериализуем
        fields = ["id", "name", "price", "description", "image", "status"]

class ItemsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_id.name')
    price = serializers.CharField(source='product_id.price')
    image = serializers.CharField(source='product_id.image')
    class Meta:
        # Модель, которую мы сериализуем
        model = LaboratoryOrderItems
        # Поля, которые мы сериализуем
        fields = ["name", "price", "amount", "id", "image"]
    

class ProcurementSerializer(serializers.ModelSerializer):
    equipment = ItemsSerializer(many=True, read_only=True)
    class Meta:
        model = LaboratoryOrder
        fields = ["id", "address", "phone", "created_date", "submited_date", "accepted_date", "status", "equipment"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ["username", "password", "email"]


class EditUserSerializer(serializers.ModelSerializer):
    equipment = ProcurementSerializer(many=True, read_only=True)
    class Meta:
        model = AuthUser
        fields = ["first_name", "last_name", "email", "password", "equipment"]


class EditProcurementSerializer(serializers.ModelSerializer):
    equipment = ItemsSerializer(many=True, read_only=True)
    class Meta:
        model = LaboratoryOrder
        fields = ["address", "phone", "created_date", "equipment"]

class EditItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryOrderItems
        fields = ["id", "product_id", "equipment", "amount"]