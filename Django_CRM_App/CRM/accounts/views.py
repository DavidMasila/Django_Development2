from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    orders_delivered = orders.filter(status = 'Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context={
        'orders':orders,
        'customers':customers,
        'total_orders' : total_orders,
        'total_customers' : total_customers,
        'orders_delivered' : orders_delivered,
        'orders_pending' : orders_pending
    }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    context = {
        #the key is what is called in the template
        'products' : products
    }
    return render(request, 'accounts/products.html', context)

def customers(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    context={
        'customer' : customer,
        'orders' : orders
    }
    return render(request, 'accounts/customer.html', context)

def createOrder(request, id):
    customer = Customer.objects.get(id=id)
    #prefills one of the form inputs. 
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    else:
        form = OrderForm(initial={'customer':customer})
        context = {
            'form':form
        }
        return render(request, 'accounts/order_form.html', context)
    
def updateOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = OrderForm(instance=order)
        context = {
            'form':form
        }
        return render(request, 'accounts/order_form.html', context)
    
def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context ={'order': order}
    return render(request, 'accounts/delete.html', context)