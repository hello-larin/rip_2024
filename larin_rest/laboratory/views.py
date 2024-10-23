from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from laboratory.serializers import *
from laboratory.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser
from laboratory.stocks.minio import add_pic, del_pic
import datetime

# Create your views here.

def user():
    try:
        user1 = AuthUser.objects.get(id=2)
    except:
        user1 = AuthUser(id=2, first_name="Иван", last_name="Иванов", password=1234, username="user1")
        user1.save()
    return user1

@api_view(["GET", "POST"])
def laboratory_catalog(request):
    if request.method == 'GET':
        try:
            parsed_data = JSONParser().parse(request)
            if parsed_data['price'] != None:
                equipment = LaboratoryItem.objects.filter(price__lte = parsed_data['price'])
            else:
                equipment = LaboratoryItem.objects.all()
        except:
            equipment = LaboratoryItem.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        printed_count = None
        selected_procurement_id = None
        selected_user = user()
        selected_procurement = LaboratoryOrder.objects.filter(status=1, user=selected_user.id)
        if selected_procurement.count() != 0:
            selected_procurement_id = selected_procurement[0].id
            printed_count = LaboratoryOrderItems.objects.filter(order=selected_procurement_id).count()
        response = {
            "equipment": serializer.data,
            "procurement_id": selected_procurement_id,
            "procurement_count": printed_count,
        }
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        parsed_data = JSONParser().parse(request)
        serializer = EquipmentSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE", "POST"])
def laboratory_equipment(request, id):
    try: 
        equipment = LaboratoryItem.objects.get(id=id) 
    except LaboratoryItem.DoesNotExist: 
        return Response({"message": "equipment not found"}, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = EquipmentSerializer(equipment)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
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
    elif request.method == 'DELETE':
        pic_result = del_pic(equipment)
        if 'error' in pic_result:
            return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
        equipment.delete() 
        return Response({"message": "equipment was deleted successfully!"}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
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
    

@api_view(["GET", "POST"])
def laboratory_procurements(request):
    if request.method == 'GET':
        try:
            parsed_data = JSONParser().parse(request)
            if 'status' in parsed_data.keys() and 'start_date' in parsed_data.keys() and 'end_date' in parsed_data.keys():
                procurement = LaboratoryOrder.objects.filter(status=parsed_data['status'],
                                                 created_date__range=(parsed_data['start_date'], parsed_data['end_date']))
            elif 'status' in parsed_data.keys():
                procurement = LaboratoryOrder.objects.filter(status=parsed_data['status'])
            elif 'start_date' in parsed_data.keys() and 'end_date' in parsed_data.keys():
                procurement = LaboratoryOrder.objects.filter(created_date__range=(parsed_data['start_date'], parsed_data['end_date']),
                                                  status__gte = 3)
            else:
                procurement =  LaboratoryOrder.objects.filter(status__gte = 3).order_by('created_date', 'status')
        except:
            procurement =  LaboratoryOrder.objects.filter(status__gte = 3).order_by('created_date', 'status')
        if orders.count() == 0:
            orders = None
        serializer = OrdersSerializer(orders, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        parsed_data = JSONParser().parse(request)
        serializer = OrdersSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def laboratory_procurement(request, id):
    try: 
        procurement = LaboratoryOrder.objects.get(id=id) 
    except LaboratoryOrder.DoesNotExist: 
        return Response(None, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = ProcurementSerializer(procurement)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        parsed_data = JSONParser().parse(request)
        serializer = EditProcurementSerializer(procurement, data=parsed_data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE':
        procurement.status = 2
        procurement.save() 
        return Response({"message": "procurement was deleted successfully!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_item(request, id):
    parsed_data = JSONParser().parse(request)
    if parsed_data['amount'] == None:
        return Response({"message": "No amount"}, status=status.HTTP_400_BAD_REQUEST)
    selected_user = user()
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
    item.save()
    procurement_items = LaboratoryOrderItems.objects.filter(order=procurement)
    serializer = ItemsSerializer(procurement_items, many=True)
    response = serializer.data
    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST", "PUT"])
def user_registration(request):
    parsed_data = JSONParser().parse(request)
    if request.method == 'POST':
        serializer = UserSerializer(data=parsed_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response({"message": "Used username"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        try:
            user = AuthUser.objects.get(username = parsed_data['username'], password = parsed_data['password'])
        except AuthUser.DoesNotExist:
            return Response({"message": "Cant login"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EditUserSerializer(user, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"message": "Bad data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def user_auth(request):
    parsed_data = JSONParser().parse(request)
    try:
        user = AuthUser.objects.get(username = parsed_data['username'], password = parsed_data['password'])
    except AuthUser.DoesNotExist:
        return Response({"message": "Cant login"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "login succesfuly"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def user_deauth(request):
    parsed_data = JSONParser().parse(request)
    try:
        user = AuthUser.objects.get(username = parsed_data['username'], password = parsed_data['password'])
    except AuthUser.DoesNotExist:
        return Response({"message": "Cant logout"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "logout succesfuly"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def submit_procurement(request, id):
    try: 
        procurement = LaboratoryOrder.objects.get(id=id, status=1) 
    except LaboratoryOrder.DoesNotExist: 
        return Response(None, status=status.HTTP_200_OK)
    if procurement.phone != None and procurement.address != None:
        procurement.status = 3
        procurement.submited_date = datetime.datetime.now()
        procurement.save()
        serializers = ProcurementSerializer(procurement)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def accept_procurement(request, id):
    try: 
        procurement = LaboratoryOrder.objects.get(id=id, status=3) 
    except LaboratoryOrder.DoesNotExist: 
        return Response({"message": "procurement not found"}, status=status.HTTP_200_OK)
    if procurement.phone != None and procurement.address != None and procurement.submited_date != None:
        procurement.status = 4
        procurement.accepted_date = datetime.datetime.now()
        procurement.save()
        serializers = ProcurementSerializer(procurement)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def one_item(request, id):
    try: 
        item = LaboratoryOrderItems.objects.get(id=id) 
    except LaboratoryOrderItems.DoesNotExist: 
        return Response({"message": "cant get item"}, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        parsed_data = JSONParser().parse(request)
        serializer = ItemsSerializer(item, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        item.delete()
        return Response({"message": "Deleted succesfuly"}, status=status.HTTP_200_OK)
