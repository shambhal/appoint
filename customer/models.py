from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default='shambhal')
    phone = models.CharField(null=True, blank=True ,max_length=20)
    access=models.CharField(null=True,max_length=150)
    refresh=models.CharField(null=True,max_length=150)