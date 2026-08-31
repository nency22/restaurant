from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
     is_active= models.BooleanField(default=True)# # The default is typically set to True, or False if they must confirm an email first 
     created_at = models.DateTimeField(auto_now_add=True)# The field automatically sets to the current timestamp on creation
     class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        CUSTOMER = 'CUSTOMER', 'Customer'

     role = models.CharField(
             max_length=10,
             choices=Role.choices,
             default=Role.CUSTOMER
    )
    

    
# Create your models here.
