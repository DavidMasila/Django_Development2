from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('logout/', views.logoutpage, name='logout'),
    path('user/', views.user, name='user'),
    path('settings/', views.user_settings, name='settings'),
    path('products/', views.products, name='products'),
    path('add_products', views.add_products, name='add_products'),
    path('customer/<int:id>/', views.customers, name='customer'),
    path('create_order/<int:id>/', views.createOrder, name="create_order"),
    path('update_order/<int:id>/', views.updateOrder, name="update_order"),
    path('delete_order/<int:id>/', views.deleteOrder, name="delete_order"),
    path('add_customer', views.add_customer, name='add_customer'),
    path('reset_password', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete')
]
