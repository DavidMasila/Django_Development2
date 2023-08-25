from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(null=True, unique=True, max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    # def __str__(self):
    # full_name = ""
    # if self.first_name:
    #     full_name += self.first_name
    # if self.last_name:
    #     if full_name:
    #         full_name += " "
    #     full_name += self.last_name
    # if not full_name:
    #     full_name = f"Customer {self.id}"
    # return full_name


class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door')
    )
    product_name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    description = models.TextField(max_length=250, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.product_name
    

class Order(models.Model):
    #lets build a drop down menu for status so that its a selection of options
    #we create tuples for their immutability
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered', 'Delivered')
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS)
    note = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return self.customer.first_name + " - " + self.product.product_name + " - " + self.status