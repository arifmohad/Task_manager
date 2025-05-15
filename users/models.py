from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('SUPERADMIN', 'SuperAdmin'),
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    add_admin = models.ForeignKey(
    'self',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='assigned_users'
)
    
    def is_superadmin(self):
        return self.role == 'SUPERADMIN'
    
    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_user(self):
        return self.role == 'USER'