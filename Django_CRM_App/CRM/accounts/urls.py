from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('logout/', views.logoutpage, name='logout'),
    path('products/', views.products, name='products'),
    path('customer/<int:id>/', views.customers, name='customer'),
    path('create_order/<int:id>/', views.createOrder, name="create_order"),
    path('update_order/<int:id>/', views.updateOrder, name="update_order"),
    path('delete_order/<int:id>/', views.deleteOrder, name="delete_order"),
]
