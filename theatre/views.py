from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from useradmin.models import *
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
        return render(request,'Theatre/dashboard.html',context)
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

        for i in screen:
            i.total_seats = i.vip_seats+i.normal_seats+i.executive_seats+i.premium_seats
            i.total_price = i.vip_price+i.premium_price+i.executive_price+i.normal_price

        print('screen:',screen)
        context = {'screen':screen}
        return render(request,'Theatre/screenManage.html',context)
    else:
        return redirect('theatreLogin')


def addScreens(request):
    if request.user.is_staff:
        if request.method == 'POST':
            user = request.user
            screen_name = request.POST['screen_name']
            row = request.POST['row']
            vip_seat = request.POST['vip_seat']
            vip_price = request.POST['vip_price']
            premium_seat = request.POST['premium_seat']
            premium_price = request.POST['premium_price']
            executive_seat = request.POST['executive_seat']
            executive_price = request.POST['executive_price']
            normal_seat = request.POST['normal_seat']
            normal_price = request.POST['normal_price']
            dict = {"row":row,"screen_name":screen_name,"vip_seat":vip_seat,"vip_price":vip_price,
            "premium_seat":premium_seat,"premium_price":premium_price,"executive_seat":executive_seat,
            "executive_price":executive_price,"normal_seat":normal_seat,"normal_price":normal_price}
            
            if Screen.objects.filter(screen_name=screen_name,user=user).exists():
                messages.error(request,'Screen already taken')
                return render(request,'Theatre/addscreen.html',dict)
            elif int(row) <= 4 or int(row) > 15 :
                messages.error(request,'Row value must between 5 & 15')
                return render(request,'Theatre/addscreen.html',dict)
            elif int(vip_seat) % int(row) != 0:
                messages.error(request,'VIP seats not count divisible by row_count')
                return render(request,'Theatre/addscreen.html',dict)
            elif int(premium_seat) % int(row) !=  0:
                messages.error(request,'Premium seats count not divisible by row_count')
                return render(request,'Theatre/addscreen.html',dict)
            elif int(executive_seat) % int(row) !=  0:
                messages.error(request,'Executive seats count not divisible by row_count')
                return render(request,'Theatre/addscreen.html',dict)
            elif int(normal_seat) % int(row) != 0:
                messages.error(request,'Normal seats count not divisible by row_count')
                return render(request,'Theatre/addscreen.html',dict)
            else:
                screen_table = Screen(row=row,vip_price=vip_price,normal_price=normal_price,premium_price=premium_price,executive_price=executive_price,user=user,screen_name=screen_name,vip_seats=vip_seat,premium_seats=premium_seat,executive_seats=executive_seat,normal_seats=normal_seat)
                print(screen_table)
                screen_table.save()
                return redirect('screens')
        else:
            return render(request,'Theatre/addscreen.html')
    else:
        return redirect('theatreLogin')
    

def theatreUserActivity(request):
    if request.user.is_staff:
        user = request.user
        return render(request,'Theatre/theatre_useractivity.html')
    else:
        return redirect('theatreLogin')


def upcomingShow(request):
    if request.user.is_staff:
        user = request.user
        upComingShow = UpcomingMovies.objects.filter(user=user)
        context = {'upComingShow':upComingShow}
        return render(request,'Theatre/upcoming_movies.html',context)
    else:
        return redirect('theatreLogin')
    

def nowShow(request):
    if request.user.is_staff:
        user = request.user
        nowshow = NowShowingMovies.objects.filter(user=user)
        context = {'nowshow':nowshow}
        return render(request,'Theatre/now_show.html',context)
    else:
        return redirect('theatreLogin')


def addMovie(request):
    if request.user.is_staff:
        if request.method == 'POST':
            user = request.user
            dealer = Dealer.objects.get(user_id=user)
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
            screen_name = request.POST['Screen']
            screen = Screen.objects.get(screen_name=screen_name,user=user)
            screen.select = True
            screen.save();
            photo_banner = request.FILES.get('photo_banner')
            photo_main = request.POST['image64data']
            value = photo_main.strip('data:image/png;base64,')
            format, imgstr = photo_main.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
            print('dealer:',dealer)
            prod = NowShowingMovies(dealer=dealer,screen=screen,user=user,movie_title=movie_name,cast_name=cast_name,director_name=director_name,release_date=release_date,show_time=show_time,runtime_hour=run_time_hour,runtime_minute=run_time_minutes,language=language,movie_type=type_movie,trailer_link=trailer_link,photo_banner=photo_banner,photo_main = data)
            prod.save();
            return redirect('now_show')
        else:
            choose_screen = Screen.objects.filter(select=False)
            context = {'screen':choose_screen}
            return render(request,'Theatre/addmovie.html',context)
    else:
        return redirect('theatreLogin')
    

def upcomingMovie(request):
    if request.user.is_staff:
        if request.method == 'POST':
            user = request.user
            dealer = Dealer.objects.get(user_id=user)
            movie_name = request.POST['movie_name']
            cast_name = request.POST['cast_name']
            director_name = request.POST['director_name']
            language = request.POST['language']
            type_movie = request.POST['type_movie']
            trailer_link = request.POST['trailer_link']
            photo_banner = request.FILES.get('photo_banner')
            photo_main = request.POST['image64data']
            value = photo_main.strip('data:image/png;base64,')
            format, imgstr = photo_main.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
            print('dealer:',dealer)
            prod = UpcomingMovies(dealer=dealer,user=user,movie_title=movie_name,cast_name=cast_name,director_name=director_name,language=language,movie_type=type_movie,trailer_link=trailer_link,photo_banner=photo_banner,photo_main = data)
            prod.save();
            return redirect('upcoming_show')
        return render(request,'Theatre/upcoming_movie.html')
    else:
        return redirect('theatreLogin')


def Nowdelete(request,id):
    movie_delete = NowShowingMovies.objects.get(id=id)
    movie_delete.delete()
    return redirect(nowShow)

def screen_delete(request,id):
    screen_delete = Screen.objects.get(id=id)
    screen_delete.delete()
    return redirect(screens)

def upcome_delete(request,id):
    upcome_delete = UpcomingMovies.objects.get(id=id)
    upcome_delete.delete()
    return redirect(upcomingShow)



def now_update(request,id):
    movie_update = NowShowingMovies.objects.get(id=id)
    if request.method == 'POST':
        movie_update.movie_name=request.POST['movie_name']
        movie_update.cast_name=request.POST['cast_name']
        movie_update.director_name=request.POST['director_name']
        movie_update.release_date=request.POST['release_date']
        movie_update.show_time=request.POST['show_time']
        movie_update.run_time_hour=request.POST['run_time_hour']
        movie_update.run_time_minutes=request.POST['run_time_minutes']
        movie_update.language=request.POST['language']
        movie_update.type_movie=request.POST['type_movie']
        movie_update.Screen=request.POST['Screen']
        movie_update.trailer_link=request.POST['trailer_link']
        photo_crop=request.POST.get('image64data')
        
        if 'photo_banner' not in request.POST:
            photo_banner = request.FILES['photo_banner']
        else:
            photo_banner=movie_update.photo_banner

        if photo_crop == "":
            # print('null')
            mv = NowShowingMovies.objects.get(id=id)
            movie_update.photo_crop = mv.photo_crop
        else:
            # print('crop:',photo_crop)
            # format, imgstr = photo_crop.split(';base64,')
            # ext = format.split('/')[-1]
            # data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
            movie_update.photo_main=photo_crop
        print('check')
        
        movie_update.photo_banner=photo_banner
        movie_update.save();
        return redirect(nowShow)

    context = {'movie_update':movie_update}
    return render(request,'Theatre/update/update_now_movie.html',context)

def screen_update(request,id):
    screen_update = Screen.objects.get(id=id)

    context = {'screen_update':screen_update}
    return render(request,'Theatre/update/update_screen.html',context)


def upcome_update(request,id):
    upcome_update = UpcomingMovies.objects.get(id=id)
    context = {'upcome_update':upcome_update}
    return render(request,'Theatre/update/update_up_movie.html',context)
