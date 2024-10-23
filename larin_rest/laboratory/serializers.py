from rest_framework import serializers
from laboratory.models import *

class UsernameSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class OrdersSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source="user.username", allow_null=True)
    moderator = serializers.CharField(source="moderator.username", allow_null=True)
    class Meta:
        model = LaboratoryOrder
        fields = ["id", "address", "phone", "created_date", "submited_date", "accepted_date", "status", "creator", "moderator"]


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
        model = User
        fields = ["username", "password", "is_staff", "is_superuser"]

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = User
        fields = ['username','password','is_staff','is_superuser']
    
    def create(self, validated_data):
        user = super().create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user

class EditUserSerializer(serializers.ModelSerializer):
    equipment = ProcurementSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "password", "equipment"]


class EditProcurementSerializer(serializers.ModelSerializer):
    equipment = ItemsSerializer(many=True, read_only=True)
    class Meta:
        model = LaboratoryOrder
        fields = ["address", "phone", "created_date", "equipment"]

class EditItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryOrderItems
        fields = ["id", "product_id", "equipment", "amount"]


