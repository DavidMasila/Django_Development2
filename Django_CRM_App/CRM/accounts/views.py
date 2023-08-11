from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    context={
        'orders':orders,
        'customers':customers
    }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    context = {
        #the key is what is called in the template
        'products' : products
    }
    return render(request, 'accounts/products.html', context)

def customers(request):
    return render(request, 'accounts/customer.html')