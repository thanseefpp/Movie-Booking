from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Contact(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    name = models.CharField(null = True,max_length = 200)
    email = models.CharField(null = True,max_length = 200)
    number = models.CharField(null = True,max_length = 200)
    subject = models.CharField(null = True,max_length = 200)
    contents = models.CharField(null = True,max_length = 2000)