from django.shortcuts import render

# Create your views here.

def store(request):
    return render(request, template_name="store/store.html", context={})

def cart(request):
    return render(request, template_name="store/cart.html", context={})
    
def checkout(request):
    return render(request, template_name="store/checkout.html", context={})
    