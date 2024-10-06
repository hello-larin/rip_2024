from django.shortcuts import render
from lab.models import *
import datetime

def GetLaboratoryCatalog(request):
    product_price = request.GET.get("laboratory-price")
    printed_count = 0
    selected_cart_id = 0
    selected_cart = LaboratoryOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = LaboratoryOrderItems.objects.filter(order=selected_cart_id).count()
    if product_price != None:
        return render(request, 'laboratory_catalog.html', {
            'data': LaboratoryItem.objects.filter(price__lte = int(product_price)),
            'searched_price': product_price,
            'cart_count': printed_count,
            'cart_id' : selected_cart_id
        })
    return render(request, 'laboratory_catalog.html', {
        'data': LaboratoryItem.objects.all(),
        'cart_count': printed_count,
        'cart_id' : selected_cart_id
    })


def GetLaboratoryItemInformation(request, selected_id):
    printed_count = 0
    selected_cart_id = 0
    selected_cart = LaboratoryOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = LaboratoryOrderItems.objects.filter(order=selected_cart_id).count()
    return render(request, 'laboratory_item_information.html', {
        'data': LaboratoryItem.objects.filter(id=selected_id),
        'cart': printed_count})
# Create your views here.

def GetLaboratoryCart(request, id):
    a = LaboratoryOrderItems.objects.filter(order=LaboratoryOrder.objects.filter(status=1)[0]).select_related('product_id')
    final_price = 0
    for i in a:
        final_price += i.product_id.price * i.amount
    return render(request, 'laboratory_cart.html', {
        'data': LaboratoryOrderItems.objects.select_related('product_id').filter(order=LaboratoryOrder.objects.filter(status=1)[0]),
        'final_price': final_price,
        'cart_id': id
    })

def AddLaboratoryItem(request):
    writing_count = request.POST['this_product_count']
    writing_product =request.POST['selected_product']
    print(writing_product)
    started_order = LaboratoryOrder.objects.filter(status=1).count()
    if started_order == 0:
        new_order = LaboratoryOrder(created_date = datetime.date.today(), status = 1)
        new_order.save()
    if LaboratoryOrderItems.objects.filter(order=LaboratoryOrder.objects.filter(status=1)[0]).count() != 0:
        selected_item = LaboratoryOrderItems.objects.filter(order=LaboratoryOrder.objects.filter(status=1)[0])[0]
        selected_item.amount += int(writing_count)
        selected_item.save()
    else:
        for_key = LaboratoryOrder.objects.filter(status=1)[0]
        pr_id = LaboratoryItem.objects.filter(id=writing_product)[0]
        item = LaboratoryOrderItems(order=for_key, product_id=pr_id, amount=int(writing_count))
        item.save()
    printed_count = 0
    selected_cart_id = 0
    selected_cart = LaboratoryOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = LaboratoryOrderItems.objects.filter(order=selected_cart_id).count()
    return render(request, 'laboratory_catalog.html', {
        'data': LaboratoryItem.objects.all(),
        'cart_count': printed_count,
        'cart_id' : selected_cart_id
    })

def DelLaboratoryItem(request, selected_id):
    selected_order = LaboratoryOrder.objects.filter(status=1)[0]
    selected_order.status = 2
    selected_order.save()
    printed_count = 0
    selected_cart_id = 0
    selected_cart = LaboratoryOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = LaboratoryOrderItems.objects.filter(order=selected_cart_id).count()
    return render(request, 'laboratory_catalog.html', {
        'data': LaboratoryItem.objects.all(),
        'cart_count': printed_count,
        'cart_id' : selected_cart_id
    })