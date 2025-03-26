from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)    


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=50, default='General')
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_users = models.ManyToManyField(User, related_name='tasks')

    #Make Task unique with name and description
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'description'], name='unique_name_description')
        ]
