from django.db import models
from django.contrib.auth.models import User
# from theatre.models import *
# Create your models here.



class Dealer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    dealer_name = models.CharField(null = True, max_length = 300)
    dealer_phone = models.CharField(null = True, max_length = 300)
    theatre_name = models.CharField(null = True, max_length = 300)
    theatre_image = models.ImageField(null=True, blank=True)
    theatre_location = models.CharField(null = True, max_length = 300)
    theatre_close = models.TimeField(auto_now_add=True)
    
    @property
    def MainURL(self):
        try:
            url = self.theatre_image.url
        except:
            url = ''
        return url

    