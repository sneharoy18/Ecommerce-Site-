from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group

def customer_profile(sender, instance, created, **kwargs):
    if created :
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
        user=instance,
        name=instance.username,
        email=instance.email,
#        id=instance.id,              #i have to add this because i have created customer without any user 
        )# apply relationship with customer user this create a customer model and attached to user

        print("profile created!")
post_save.connect(customer_profile, sender=User)   # just when user save in views.py page this function is called