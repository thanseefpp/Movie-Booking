from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Screen
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import base64
from PIL import Image
from base64 import decodestring
import binascii
from django.core.files import File
from django.http import JsonResponse
import json
from datetime import *
import requests
from .models import *
from django.views.generic import View
from django.core.files.base import ContentFile



def theatreLogin(request):
    if request.user.is_staff:
        owner = User.objects.filter(is_staff=True)
        return redirect('theatreDashboard')
    
    elif request.method == 'POST':
        otp=request.POST['otp']

        id = request.session['id']

        print('id one:',id)

        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': id,
        'otp_code': otp}
        files = [

        ]
        headers = {
        'Authorization': 'Token ca23c2854b8ab3dc239f449be501299d5fefe86f'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))
        data=response.text.encode('utf8')
        datadict=json.loads(data)
        status=datadict['status']
        
        if status == 'success':
            username = request.session['username']
            if User.objects.filter(username=username,is_staff=True).exists():
                user = User.objects.get(username=username)
                auth.login(request,user)
                return redirect(theatreDashboard)
            else:
                messages.error(request,'User not Exist')
                return render(request,'Theatre/Theatrelogin.html')

        else:
            messages.error(request,'Incorrect OTP')
            return render(request,'Theatre/Theatrelogin.html')

    else:
        return render(request,'Theatre/Theatrelogin.html')


def mobile(request):
    number = request.GET.get('mobile', None)
    user=User.objects.get(last_name=number,is_staff=True)
    print(user)
   
    if user:
        username = user.username
        request.session['username'] =  username

        url = "https://d7networks.com/api/verifier/send"
        number=str(91) + number
        
        payload = {'mobile': number,
        'sender_id': 'SMSINFO',
        'message': 'Your otp code is {code}',
        'expiry': '900'}
        files = [

        ]
        headers = {
        'Authorization': 'Token ca23c2854b8ab3dc239f449be501299d5fefe86f'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))
        data=response.text.encode('utf8')
        datadict=json.loads(data)
        print('datadict:',datadict)

        id=datadict['otp_id']
        print('id:',id)
        request.session['id'] = id
        
        data='success'
        return JsonResponse (data,safe=False)


def theatreDashboard(request):
    if request.user.is_staff:
        owner = User.objects.filter(is_staff=True)
        print("Owner:",owner)
        context = {'Owner':owner}
        return render(request,'Theatre/theatredashboard.html',context)
    else:
        return redirect('theatreLogin')


def theatreout(request):
    if request.user.is_staff:
        auth.logout(request)
        return redirect('theatreLogin')
    else:
        return redirect('theatreLogin')

def screens(request):
    if request.user.is_staff:
        user = request.user
        screen = Screen.objects.filter(user=user)
        dict = {}
        for i in screen:
            dict[i] = i.vip_seats+i.normal_seats+i.executive_seats+i.premium_seats

        context = {'screen':dict}
        return render(request,'Theatre/screen_manage.html',context)
    else:
        return redirect('theatreLogin')


def addScreens(request):
    if request.user.is_staff:
        if request.method == 'POST':
            user = request.user
            screen_name = request.POST['screen_name']
            vip_seat = request.POST['vip_seat']
            premium_seat = request.POST['premium_seat']
            executive_seat = request.POST['executive_seat']
            normal_seat = request.POST['normal_seat']
            screen_table = Screen(user=user,screen_name=screen_name,vip_seats=vip_seat,premium_seats=premium_seat,executive_seats=executive_seat,normal_seats=normal_seat)
            print(screen_table)
            screen_table.save()
            return redirect('screens')
        else:
            return render(request,'Theatre/addscreen.html')
    else:
        return redirect('theatreLogin')
    

def theatreUserActivity(request):
    if request.user.is_staff:
        return render(request,'Theatre/theatre_user_activity.html')
    else:
        return redirect('theatreLogin')

def upcomingShow(request):
    if request.user.is_staff:
        return render(request,'Theatre/upcoming.html')
    else:
        return redirect('theatreLogin')
    

def nowShow(request):
    if request.user.is_staff:
        user = request.user
        nowshow = NowShowingMovies.objects.filter(user=user)
        context = {'nowshow':nowshow}
        return render(request,'Theatre/show.html',context)
    else:
        return redirect('theatreLogin')


def addMovie(request):
    if request.user.is_staff:
        if request.method == 'POST':
            user = request.user
            movie_name = request.POST['movie_name']
            cast_name = request.POST['cast_name']
            director_name = request.POST['director_name']
            release_date = request.POST['release_date']
            show_time = request.POST['show_time']
            run_time_hour = request.POST['run_time_hour']
            run_time_minutes = request.POST['run_time_minutes']
            language = request.POST['language']
            type_movie = request.POST['type_movie']
            trailer_link = request.POST['trailer_link']
            photo_banner = request.FILES.get('photo_banner')
            photo_main = request.POST['image64data']
            print('data:', photo_main)
            value = photo_main.strip('data:image/png;base64,')
            format, imgstr = photo_main.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
            prod = NowShowingMovies(user=user,movie_title=movie_name,cast_name=cast_name,director_name=director_name,release_date=release_date,show_time=show_time,runtime_hour=run_time_hour,runtime_minute=run_time_minutes,language=language,movie_type=type_movie,trailer_link=trailer_link,photo_banner=photo_banner,photo_main = data)
            prod.save();
            return redirect('now_show')
        else:
            return render(request,'Theatre/addmovie.html')
    else:
        return redirect('theatreLogin')
    

def upcomingMovie(request):
    if request.user.is_staff:
        
        return render(request,'Theatre/upcoming_movie.html')
    else:
        return redirect('theatreLogin')
