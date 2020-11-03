from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Screen(models.Model):
    screen_name = models.CharField(max_length = 300)
    vip_seats = models.IntegerField()
    premium_seats = models.IntegerField()
    executive_seats = models.IntegerField()
    normal_seats = models.IntegerField()

    # def __str__(self):
    #     return self.screen_name