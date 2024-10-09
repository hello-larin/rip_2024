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
        products = LaboratoryItem.objects.all()
        serializer = ProductSerializer(products, many=True)
        printed_count = None
        selected_cart_id = None
        selected_user = user()
        selected_cart = LaboratoryOrder.objects.filter(status=1, user=selected_user.id)
        if selected_cart.count() != 0:
            selected_cart_id = selected_cart[0].id
            printed_count = LaboratoryOrderItems.objects.filter(order=selected_cart_id).count()
        response = {
            "products": serializer.data,
            "cart_id": selected_cart_id,
            "cart_count": printed_count,
            "user_id": selected_user.id
        }
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        parsed_data = JSONParser().parse(request)
        serializer = ProductSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE", "POST"])
def laboratory_product(request, id):
    try: 
        product = LaboratoryItem.objects.get(id=id) 
    except LaboratoryItem.DoesNotExist: 
        return Response({"message": "Product not found"}, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        parsed_data = JSONParser().parse(request)
        if 'pic' in parsed_data:
            pic_result = add_pic(product, parsed_data.initial_data['pic'])
            if 'error' in pic_result.data:
                return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(product, data=parsed_data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE':
        pic_result = del_pic(product)
        if 'error' in pic_result:
            return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
        product.delete() 
        return Response({"message": "Product was deleted successfully!"}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # Используем MultiPartParser для обработки файлов
        pic_file = request.FILES['pic']
        # Проверяем наличие файла в parsed_data
        if pic_file != None:
            pic_result = add_pic(product, pic_file)
            if 'error' in pic_result:
                return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
            product.image = pic_result["message"]
            product.save()
            serializer = ProductSerializer(LaboratoryItem.objects.get(id=id) ) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "not a image"}, status=status.HTTP_400_BAD_REQUEST) 
    

@api_view(["GET", "POST"])
def laboratory_carts(request):
    if request.method == 'GET':
        orders =  LaboratoryOrder.objects.filter(status__gte = 3).order_by('created_date', 'status')
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
def laboratory_cart(request, id):
    try: 
        cart = LaboratoryOrder.objects.get(id=id) 
    except LaboratoryOrder.DoesNotExist: 
        return Response(None, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = CartSerializer(cart)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        parsed_data = JSONParser().parse(request)
        serializer = EditCartSerializer(cart, data=parsed_data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE':
        cart.status = 2
        cart.save() 
        return Response({"message": "Cart was deleted successfully!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_item(request, id):
    parsed_data = JSONParser().parse(request)
    if parsed_data['amount'] == None:
        return Response({"message": "No amount"}, status=status.HTTP_400_BAD_REQUEST)
    selected_user = user()
    try: 
        cart = LaboratoryOrder.objects.get(user=selected_user, status=1) 
    except LaboratoryOrder.DoesNotExist: 
        cart = LaboratoryOrder(user=selected_user, status=1)
        cart.save()
    try:
        product = LaboratoryItem.objects.get(id=id)
    except LaboratoryItem.DoesNotExist:
        return Response({"message": "Product with id={id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        item = LaboratoryOrderItems.objects.get(order=cart, product_id=product) 
    except LaboratoryOrderItems.DoesNotExist: 
        item = LaboratoryOrderItems(order=cart, product_id=product, amount=0)
    item.amount += parsed_data['amount']
    item.save()
    cart_items = LaboratoryOrderItems.objects.filter(order=cart)
    serializer = ItemsSerializer(cart_items, many=True)
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
def submit_cart(request, id):
    try: 
        cart = LaboratoryOrder.objects.get(id=id, status=1) 
    except LaboratoryOrder.DoesNotExist: 
        return Response(None, status=status.HTTP_200_OK)
    if cart.phone != None and cart.address != None:
        cart.status = 3
        cart.submited_date = datetime.date.today()
        cart.save()
        serializers = CartSerializer(cart)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def accept_cart(request, id):
    try: 
        cart = LaboratoryOrder.objects.get(id=id, status=3) 
    except LaboratoryOrder.DoesNotExist: 
        return Response({"message": "cart not found"}, status=status.HTTP_200_OK)
    if cart.phone != None and cart.address != None and cart.submited_date != None:
        cart.status = 4
        cart.accepted_date = datetime.date.today()
        cart.save()
        serializers = CartSerializer(cart)
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