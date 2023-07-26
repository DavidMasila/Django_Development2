from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee
# Create your views here.


def employee_list(request):
    context = {
        'employee_list': Employee.objects.all(),
    }
    return render(request, 'employee_register/employee_list.html', context)


def employee_insert(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_register/employee_form.html', {'form': form})


def employee_edit(request, id):
    if request.method == 'GET':
        employee = Employee.objects.get(pk=id)
        #instance = employee fills the form with the employee details for you to edit
        form = EmployeeForm(instance=employee)
        return render(request, 'employee_register/employee_update.html', {'form': form})
    else:
        employee = Employee.objects.get(pk=id)
        #getting the info and having instance updates details to that specific employee
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/list')


def employee_delete(request, id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return redirect("/list")
