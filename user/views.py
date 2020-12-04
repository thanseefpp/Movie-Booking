from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import json
import requests
from django.core.files import File
from django.core.files.base import ContentFile
from useradmin.models import *
from theatre.models import *


def index(request):
    dealer = Dealer.objects.all()
    # if request.user.is_authenticated:
    #     dealer = Dealer.objects.all()
    context = {'dealer':dealer}
    return render(request,'user/index.html',context)


def theatre_movies(request,id):
    dealer = Dealer.objects.get(id=id)
    movie = NowShowingMovies.objects.filter(dealer=dealer)
    # if request.user.is_authenticated:
    #     dealer = Dealer.objects.get(id=id)
    #     movie = NowShowingMovies.objects.filter(dealer=dealer)
    context = {'movie':movie}
    return render(request,'user/TheatreMovies.html',context)


def book_show(request,id):
    movie = NowShowingMovies.objects.filter(id=id)
    context = {'movie':movie}
    return render(request,'user/bookshow.html',context)


def seat_book(request,id):
    movie = NowShowingMovies.objects.get(id=id)
    screen_count = movie.screen
    print('screen :',screen_count)
    vip_seats = screen_count.vip_seats
    vip_price = screen_count.vip_price
    row_count = screen_count.row
    premium_seats = screen_count.premium_seats
    premium_price = screen_count.premium_price
    executive_seats = screen_count.executive_seats
    executive_price = screen_count.executive_price
    normal_seats = screen_count.normal_seats
    normal_price = screen_count.normal_price
    value = normal_seats + vip_seats + premium_seats + executive_seats
    print('value:',value)
    print('v,p,e,n:',vip_price,premium_price,executive_price,normal_price)
    print('vip,premium_seats,executive_seats,normal_seats:',vip_seats,premium_seats,executive_seats,normal_seats)

    context = {'row_count':row_count,'normal_price':normal_price,'executive_price':executive_price,'vip_price':vip_price,'screen':screen_count,'vip_seats':vip_seats,'premium_seats':premium_seats,'executive_seats':executive_seats,'normal_seats':normal_seats,'premium_price':premium_price,'totalSeat':value}
    return render(request,'user/seats.html',context)



def checkout(request):
    selectedSeats = request.POST.get('seatNumber')
    print('selectedSeats:',selectedSeats)
    return JsonResponse("order_place",safe=False)


def orderPlace(request):
    return render(request,'user/checkout.html')


def seatreconnect(request):
    if request.method == 'GET':
        seatCount = request.GET.get('seatCount', None)
        seatNumber = request.GET.get('seatNumber', None)
        typeOfSeat = request.GET.get('typeOfSeat', None)
        totalPrice = request.GET.get('totalPrice', None)
        selectedSeats = request.GET.get('selectedSeats', None)
        selectedMoviePrice = request.GET.get('selectedMoviePrice', None)
        print('get function check:',seatCount,seatNumber,typeOfSeat,selectedSeats,totalPrice,selectedMoviePrice)
        # array = []
        # for i in seatNumber.split(","):
        #     value=i
        #     array.append(value) 
        # print('array:',array)
        return JsonResponse(seatNumber,safe=False)


# Login , Register , OTP , Logout

def login(request):
    if request.user.is_authenticated:
        return redirect(index)
    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        dict = {'username':username}
        if user is not None and is_staff == False and is_superuser == False:
            auth.login(request,user)
            return redirect(index)
        else:
            messages.error(request, '😢 Wrong username/password!')
            return render(request,'user/login/login.html',dict)
    else:
        return render(request,'user/login/login.html')



def register(request):
    if request.user.is_authenticated:
        return redirect(index)

    elif request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        dicti = {"username":username,"email":email,'mobile':number}
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already taken')
                return render(request,'user/login/register.html',dicti)
            elif User.objects.filter(username=username).exists():
                messages.error(request,"username already taken") 
                return render(request,'user/login/register.html',dicti)
            elif User.objects.filter(last_name=number).exists():
                messages.error(request,'Mobile number already taken')
                return render(request,'user/login/register.html',dicti)

            else:
                request.session['username']=username
                request.session['password']=password
                request.session['email']=email
                request.session['number']=number
                
                url = "https://d7networks.com/api/verifier/send"
                number=str(91) + number
                payload = {'mobile': number,
                'sender_id': 'SMSINFO',
                'message': 'Your otp code is {code}',
                'expiry': '900'}
                files = []
                headers = {
                'Authorization': 'Token ca23c2854b8ab3dc239f449be501299d5fefe86f'
                }
                response = requests.request("POST", url, headers=headers, data = payload, files = files)
                print(response.text.encode('utf8'))
                data=response.text.encode('utf8')
                datadict=json.loads(data.decode('utf-8'))
                print('datadict:',datadict)
                
                id=datadict['otp_id']
                status=datadict['status']
                print('id:',id)
                request.session['id'] = id
                return render(request,'user/login/otp.html')
        else:
            messages.error(request,"Wrong Password")
            return render(request,'user/login/register.html',dicti)
    else:
        return render(request, 'user/login/register.html')


def otp(request):
    if request.method == 'POST':
        otp=request.POST['otp']
       
        id=request.session['id']
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
        datadict=json.loads(data.decode('utf-8'))
        status=datadict['status']
        
        if status=='success':
            username = request.session['username']   
            password =  request.session['password']
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username,password=password)

            else:
                email=request.session['email']
                number=request.session['number']
                user=User.objects.create_user(username=username,email=email,password=password,last_name=number,first_name=password)
                user.save();

            auth.login(request,user)
            return redirect(index)

        else:
            messages.error(request,'Incorrect OTP')
            return render(request,'user/login/otp.html')

    return render(request,'user/login/otp.html')



def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(index)
    else:
        return redirect(index)
