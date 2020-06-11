from django.shortcuts import render
from .models import *
# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name="store/store.html", context=context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # We are able to query child objects: [parent].[child]_set.all()... reveres query set allows us to access child elements
    else:
        items = []
        order = {'get_total_cart': 0, 'get_total_quantity': 0}

    context = {'items': items, 'order': order}
    return render(request, template_name="store/cart.html", context=context)
    
def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # We are able to query child objects: [parent].[child]_set.all()... reveres query set allows us to access child elements
    else:
        items = []
        order = {'get_total_cart': 0, 'get_total_quantity': 0}

    context = {'items': items, 'order': order}
    return render(request, template_name="store/checkout.html", context=context)
    