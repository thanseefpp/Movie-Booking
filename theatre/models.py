from django.db import models
from django.contrib.auth.models import User
from useradmin.models import Dealer
# Create your models here.

class Screen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    screen_name = models.CharField(max_length = 300)
    row = models.IntegerField(null =True, blank=True)
    vip_seats = models.IntegerField()
    vip_price = models.IntegerField(null =True, blank=True)
    premium_seats = models.IntegerField()
    premium_price = models.IntegerField(null =True, blank=True)
    executive_seats = models.IntegerField()
    executive_price = models.IntegerField(null =True, blank=True)
    normal_seats = models.IntegerField()
    normal_price = models.IntegerField(null =True, blank=True)
    select = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.screen_name

class NowShowingMovies(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE, null =True, blank=True)
    movie_title = models.CharField(max_length=300,null=True)
    cast_name = models.CharField(max_length=300,null=True)
    director_name = models.CharField(max_length=300,null=True)
    release_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    show_time = models.TimeField(auto_now_add=True)
    runtime_hour = models.IntegerField(default=0, null=True, blank=True)
    runtime_minute = models.IntegerField(default=0, null=True, blank=True)
    language = models.CharField(max_length=300,null=True)
    movie_type = models.CharField(max_length=200,null=True)
    trailer_link = models.URLField(max_length=500)
    photo_banner = models.ImageField(null=True, blank=True)
    photo_main = models.ImageField(null=True, blank=True)
    
    @property
    def BannerURL(self):
        try:
            url = self.photo_banner.url
        except:
            url = ''
        return url

    @property
    def MainURL(self):
        try:
            url = self.photo_main.url
        except:
            url = ''
        return url


class SeatSelected(models.Model):
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE, null =True, blank=True)
    movie = models.ForeignKey(NowShowingMovies,on_delete=models.CASCADE, null =True, blank=True)
    occupied_seats = models.CharField(max_length=300,null=True)


class UpcomingMovies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE, null =True, blank=True)
    movie_title = models.CharField(max_length=300,null=True)
    cast_name = models.CharField(max_length=300,null=True)
    director_name = models.CharField(max_length=300,null=True)
    language = models.CharField(max_length=300,null=True)
    movie_type = models.CharField(max_length=200,null=True)
    trailer_link = models.URLField(max_length=500)
    photo_banner = models.ImageField(null=True, blank=True)
    photo_main = models.ImageField(null=True, blank=True)
    
    @property
    def BannerURL(self):
        try:
            url = self.photo_banner.url
        except:
            url = ''
        return url

    @property
    def MainURL(self):
        try:
            url = self.photo_main.url
        except:
            url = ''
        return url


class BookingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE, null =True, blank=True)
    movies = models.ForeignKey(NowShowingMovies,on_delete=models.CASCADE, null =True, blank=True)
    seatSelect = models.ForeignKey(SeatSelected,on_delete=models.CASCADE, null =True, blank=True)
    email = models.CharField(max_length=300,null=True)
    phone_number = models.CharField(max_length=300,null=True)
    