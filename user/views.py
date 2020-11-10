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



def index(request):
    return render(request,'user/index.html')


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
                'Authorization': 'Token 0d21f1e3cb977b24ebd925ec71d3fec0cb0a41f3'
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
        'Authorization': 'Token 0d21f1e3cb977b24ebd925ec71d3fec0cb0a41f3'
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


def bookShow(request):
    return render(request,'user/bookshow.html')