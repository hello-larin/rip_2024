from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from laboratory.serializers import *
from laboratory.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser
from laboratory.stocks.minio import add_pic, del_pic
import datetime
from drf_yasg.utils import swagger_auto_schema
from laboratory.permissions import *
from laboratory.redis import session_storage
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import *
from django.views.decorators.csrf import csrf_exempt
import uuid

from drf_yasg import openapi
import hashlib

# Create your views here.

def hash_delivery(username, address, phone):
    input_string = f"{id}{address}{phone}{username}"

    # Создаем хэш SHA-256
    hash_object = hashlib.sha256(input_string.encode())
    hash_hex = hash_object.hexdigest()

    # Преобразуем хэш в base64 и берем первые 3 символа
    hash_base64 = base64.b64encode(hash_object.digest()).decode()
    prefix = hash_base64[:3].upper()

    # Преобразуем хэш в число и берем первые 8 цифр
    hash_int = int(hash_hex, 16)
    suffix = str(hash_int)[:8]

    # Формируем окончательный хэш
    unique_hash = f"{prefix}{suffix}"

    return unique_hash


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes        
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator

def get_user(request):
    session_id = request.COOKIES.get("session_id")
    if session_id is None:
        return None
    else:
        username = session_storage.get(session_id).decode("utf-8")
        try:
            user = User.objects.get(username=username)
            print(user.username)
            return user
        except:
            print("cant get user")
            user = None
            return user
    

class laboratory_catalog(APIView):
    @swagger_auto_schema(responses={200: EquipmentResponseSerializer()})
    @method_permission_classes([AllowAny])
    def get(self, request, format=None):
        try:
            price = request.GET.get("price")
            print(price)
            if price != None:
                equipment = LaboratoryItem.objects.filter(price__lte = price)
            else:
                equipment = LaboratoryItem.objects.all()
        except:
            equipment = LaboratoryItem.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        printed_count = None
        selected_procurement_id = None
        user = get_user(request)
        if user is not None:
            try:
                selected_procurement = LaboratoryOrder.objects.get(status=1, user=user)
                selected_procurement_id = selected_procurement.id
                printed_count = LaboratoryOrderItems.objects.filter(order=selected_procurement_id).count()
            except LaboratoryOrder.DoesNotExist:
                print('*' * 12)
                print('Not auth')
        response = {
            "equipment": serializer.data,
            "procurement_id": selected_procurement_id,
            "procurement_count": printed_count,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=EquipmentSerializer)
    @method_permission_classes([IsAdminAuth])
    def post(self, request):
        parsed_data = JSONParser().parse(request)
        serializer = EquipmentSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class laboratory_equipment(APIView):
    @swagger_auto_schema(responses={200: EquipmentSerializer()})
    @permission_classes([AllowAny])
    def get(self, request, id, format=None):
        try: 
            equipment = LaboratoryItem.objects.get(id=id) 
        except LaboratoryItem.DoesNotExist: 
            return Response({"message": "equipment not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EquipmentSerializer(equipment)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    
    @method_permission_classes([IsAdminAuth])
    @swagger_auto_schema(request_body=EquipmentSerializer)
    def put(self, request, id, format=None):
        try: 
            equipment = LaboratoryItem.objects.get(id=id) 
        except LaboratoryItem.DoesNotExist: 
            return Response({"message": "equipment not found"}, status=status.HTTP_400_BAD_REQUEST)
        parsed_data = JSONParser().parse(request)
        if 'pic' in parsed_data:
            pic_result = add_pic(equipment, parsed_data.initial_data['pic'])
            if 'error' in pic_result.data:
                return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EquipmentSerializer(equipment, data=parsed_data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_permission_classes([IsAdminAuth])
    def delete(self, request, id, format=None):
        try: 
            equipment = LaboratoryItem.objects.get(id=id) 
        except LaboratoryItem.DoesNotExist: 
            return Response({"message": "equipment not found"}, status=status.HTTP_400_BAD_REQUEST)
        pic_result = del_pic(equipment)
        if 'error' in pic_result:
            return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
        equipment.delete() 
        return Response({"message": "equipment was deleted successfully!"}, status=status.HTTP_200_OK)
    
    @method_permission_classes([IsAdminAuth])
    @swagger_auto_schema(request_body=EquipmentSerializer)
    def post(self, request, id, format=None):
        try: 
            equipment = LaboratoryItem.objects.get(id=id) 
        except LaboratoryItem.DoesNotExist: 
            return Response({"message": "equipment not found"}, status=status.HTTP_400_BAD_REQUEST)
        # Используем MultiPartParser для обработки файлов
        pic_file = request.FILES['pic']
        # Проверяем наличие файла в parsed_data
        if pic_file != None:
            pic_result = add_pic(equipment, pic_file)
            if 'error' in pic_result:
                return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
            equipment.image = pic_result["message"]
            equipment.save()
            serializer = EquipmentSerializer(LaboratoryItem.objects.get(id=id) ) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "not a image"}, status=status.HTTP_400_BAD_REQUEST)


class laboratory_procurements(APIView):
    @swagger_auto_schema(responses={200: OrdersSerializer(many=True)},
                         )
    def get(self, request):
        user = get_user(request)
        if user is None:
            return Response({"message": "no active session"}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_superuser or user.is_staff:
            orders =  LaboratoryOrder.objects.filter(status__gte = 3).order_by('created_date', 'status')   
        else:
            print("order start user") 
            orders = LaboratoryOrder.objects.filter(user=user)
        if orders.count() == 0:
            print("order start") 
            return Response([],status=status.HTTP_200_OK)
        serializer = OrdersSerializer(orders, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

class laboratory_procurement(APIView):
    @swagger_auto_schema(responses={200: OrdersSerializer()})
    def get(self, request, id):
        user = get_user(request)
        try: 
            procurement = LaboratoryOrder.objects.get(id=id, user=user) 
        except LaboratoryOrder.DoesNotExist: 
            return Response({"message": "procurement not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProcurementSerializer(procurement)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=EditProcurementSerializer,
                         responses={200: EditProcurementSerializer()})
    def put(self, request, id):
        user = get_user(request)
        try: 
            procurement = LaboratoryOrder.objects.get(id=id, user=user) 
        except LaboratoryOrder.DoesNotExist: 
            return Response({"message": "procurement not found"}, status=status.HTTP_400_BAD_REQUEST)
        parsed_data = JSONParser().parse(request)
        serializer = EditProcurementSerializer(procurement, data=parsed_data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user = get_user(request)
        try: 
            procurement = LaboratoryOrder.objects.get(id=id, user=user)
        except LaboratoryOrder.DoesNotExist: 
            return Response({"message": "procurement not found"}, status=status.HTTP_400_BAD_REQUEST)
        procurement.status = 2
        procurement.save() 
        return Response({"message": "procurement was deleted successfully!"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=AmountRequestSerializer(),
                     responses={200: ItemsSerializer(many=True)})
@api_view(["POST"])
@permission_classes([IsAuth])
def add_item(request, id):
    parsed_data = {}
    parsed_data['amount'] = request.data.get("amount")
    if parsed_data['amount'] == None:
        return Response({"message": "No amount"}, status=status.HTTP_400_BAD_REQUEST)
    selected_user = request.user
    if selected_user is None:
        return Response({"message": "No session!"}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        procurement = LaboratoryOrder.objects.get(user=selected_user, status=1) 
    except LaboratoryOrder.DoesNotExist: 
        procurement = LaboratoryOrder(user=selected_user, status=1)
        procurement.save()
    try:
        equipment = LaboratoryItem.objects.get(id=id)
    except LaboratoryItem.DoesNotExist:
        return Response({"message": "equipment with id={id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        item = LaboratoryOrderItems.objects.get(order=procurement, product_id=equipment) 
    except LaboratoryOrderItems.DoesNotExist: 
        item = LaboratoryOrderItems(order=procurement, product_id=equipment, amount=0)
    item.amount += parsed_data['amount']
    if item.amount <= 0:
        item.delete()
    else:
        item.save()
    procurement_items = LaboratoryOrderItems.objects.filter(order=procurement)
    serializer = ItemsSerializer(procurement_items, many=True)
    response = serializer.data
    return Response(response, status=status.HTTP_200_OK)


class user_registration(APIView):
    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request):
        user = get_user(request)
        if user == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=EditUserSerializer,
                         responses={200: UserSerializer()})
    def put(self, request):
        parsed_data = JSONParser().parse(request)
        user = get_user(request)
        if user == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = EditUserSerializer(user, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user = get_user(request)
            serializer = UserSerializer(user)
        else:
            return Response({"message": "Bad data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=RegisterSerializer,
                     responses={201: RegisterSerializer()})
@csrf_exempt
@api_view(['Post'])
@permission_classes([AllowAny])
def register(request, format=None):
    #parsed_data = JSONParser().parse(request)
    if User.objects.filter(username=request.data['username']).exists():
        return Response({"message": "username exist!"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=AuthSerializer,
                     responses={200: UserSerializer()})
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def user_auth(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username,
                            password=password)
    if user is not None:
        login(request, user)
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        serializer = UserSerializer(user)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie("session_id", random_key, samesite="lax")
        return response
    else:
        return Response({"message": "Cant login",
                             "username":username,
                             "password":password},
                            status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post')
@api_view(["POST"])
def user_deauth(request):
    session_id = request.COOKIES.get("session_id")
    if session_id is not None:
        session_storage.delete(session_id)
    logout(request._request)
    return Response({'message': 'Success'})


@swagger_auto_schema(method='post', responses={200: ProcurementSerializer()})
@api_view(["POST"])
def submit_procurement(request, id):
    user = get_user(request)
    try: 
        procurement = LaboratoryOrder.objects.get(id=id, status=1, user=user) 
    except LaboratoryOrder.DoesNotExist: 
        return Response({"message": "cant find procurement"}, status=status.HTTP_400_BAD_REQUEST)
    if procurement.phone != None and procurement.address != None:
        procurement.status = 3
        procurement.submited_date = datetime.datetime.now()
        procurement.delivery_number = hash_delivery(procurement.user.username, procurement.address, procurement.phone)
        procurement.save()
        serializers = ProcurementSerializer(procurement)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', responses={200: ProcurementSerializer()})
@api_view(["POST"])
@permission_classes([IsManagerAuth])
def accept_procurement(request, id):
    user = get_user(request)
    try: 
        procurement = LaboratoryOrder.objects.get(id=id, status=3) 
    except LaboratoryOrder.DoesNotExist: 
        return Response({"message": "procurement not found"}, status=status.HTTP_200_OK)
    if procurement.phone != None and procurement.address != None and procurement.submited_date != None:
        procurement.status = 4
        procurement.accepted_date = datetime.datetime.now()
        procurement.moderator = user
        procurement.save()
        serializers = ProcurementSerializer(procurement)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)


class one_item(APIView):
    @swagger_auto_schema(request_body=ItemsSerializer, 
                         responses={200: ItemsSerializer(many=True)})
    def put(self, request, id):
        user = user(request)
        try: 
            item = LaboratoryOrderItems.objects.get(id=id, order__user=user) 
        except LaboratoryOrderItems.DoesNotExist: 
            return Response({"message": "cant get item"}, status=status.HTTP_400_BAD_REQUEST)
        parsed_data = JSONParser().parse(request)
        serializer = ItemsSerializer(item, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        user = user(request)
        try: 
            item = LaboratoryOrderItems.objects.get(id=id, order__user=user) 
        except LaboratoryOrderItems.DoesNotExist: 
            return Response({"message": "cant get item"}, status=status.HTTP_400_BAD_REQUEST)
        item.delete()
        return Response({"message": "Deleted succesfuly"}, status=status.HTTP_200_OK)
        
        

