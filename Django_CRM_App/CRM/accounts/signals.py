from django.contrib.auth.models import User, Group
from .models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def Create_Customer(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="customer")
        instance.groups.add(group)
        first_name = instance.first_name
        last_name = instance.last_name
        email = instance.email
        Customer.objects.create(user=instance, first_name=first_name, last_name = last_name, email=email)
        
#post_save.connect(Create_Customer, sender=User)