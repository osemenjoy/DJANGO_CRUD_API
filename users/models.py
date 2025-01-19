from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"), # first is the value stored in the database, second is the human-readable name
        ("user", "User")
    )
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length= 255, choices=ROLE_CHOICES, default='user')
    
