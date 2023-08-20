from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
# Create your views here.


def loginpage(request):
    return render(request, 'accounts/login.html')


def registerpage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    else:
        form = CreateUserForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        # the key is what is called in the template
        'products': products
    }
    return render(request, 'accounts/products.html', context)


def customers(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    # we create a filter and give it the query set of the customer orders so it only provides those //
    # after we recreate the orders variable with filter.qs (qs = queryset)
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'filter': my_filter
    }
    return render(request, 'accounts/customer.html', context)


def createOrder(request, id):
    # inline formsets allow to enter multiple fields without first submitting
    # Takes in the Parent model, child model and the fields to take from child model
    # extra determines how many form sets to generate
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status', 'note'), extra=3)
    customer = Customer.objects.get(id=id)

    # prefills one of the form inputs.
    if request.method == "POST":
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    else:
        # form = OrderForm(initial={'customer':customer})
        # the queryset=Order.Objects.none() eliminates the previous order from from list
        formset = OrderFormSet(
            queryset=Order.objects.none(), instance=customer)
        context = {
            'formset': formset
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
            'form': form
        }
        return render(request, 'accounts/update_order_form.html', context)


def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'accounts/delete.html', context)


def logoutpage(request):
    return render(request, 'accounts/login.html')
