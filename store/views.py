from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
import json
# Create your views here.

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # We are able to query child objects: [parent].[child]_set.all()... reveres query set allows us to access child elements
        cartItems = order.get_total_quantity
    else:
        items = []
        order = {'get_total_cart': 0, 'get_total_quantity': 0, 'shipping': False}
        cartItems = order['get_total_quantity']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, template_name="store/store.html", context=context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # We are able to query child objects: [parent].[child]_set.all()... reveres query set allows us to access child elements
        cartItems = order.get_total_quantity
    else:
        items = []
        order = {'get_total_cart': 0, 'get_total_quantity': 0, 'shipping': False}
        cartItems = order['get_total_quantity']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, template_name="store/cart.html", context=context)
    
def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # We are able to query child objects: [parent].[child]_set.all()... reveres query set allows us to access child elements
        cartItems = order.get_total_quantity

    else:
        items = []
        order = {'get_total_cart': 0, 'get_total_quantity': 0, 'shipping': False}
        cartItems = order['get_total_quantity']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, template_name="store/checkout.html", context=context)
    

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productId: ", productId)
    print("action: ", action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    print("Data: ", request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if(request.user.is_authenticated):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_total_cart:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print("User is not logged in")
    return JsonResponse("Payment completed", safe=False)