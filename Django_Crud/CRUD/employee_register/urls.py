from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.employee_insert, name="employee_insert"),
    path('list/<int:id>/', views.employee_edit, name="employee_edit"),
    path('delete/<int:id>/', views.employee_delete, name="employee_delete"),
    path('list', views.employee_list, name='employee_list')
]
