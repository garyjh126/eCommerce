from django.shortcuts import render
from .models import *
# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name="store/store.html", context=context)

def cart(request):
    return render(request, template_name="store/cart.html", context={})
    
def checkout(request):
    return render(request, template_name="store/checkout.html", context={})
    