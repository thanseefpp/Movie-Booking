from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import *
# image crop
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
from theatre.models import *
from django.views.generic import View
from django.core.files.base import ContentFile


def adminlogin(request):
    if request.session.has_key('username'):
        return redirect('adminDashboard')

    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        if username == 'admin' and password == 'admin':
            request.session['username'] = username
            return redirect('adminDashboard')

        else:
            messages.error(request, "😢 Wrong username/password! 😢")
            return redirect(adminlogin)
    else:
        return render(request,'useradmin/adminlogin.html')
    


def adminDashboard(request):
    if request.session.has_key('username'):
        user = User.objects.filter(is_staff=False,is_superuser=False)
        dealer = Dealer.objects.all()
        booked = Booked.objects.all()
        showing_movies = NowShowingMovies.objects.all()
        list = []
        for i in booked:
            val = i.paid_amount
            list.append(val)
        total_price = sum(list)
        context = {'user':user,'dealer':dealer,'total_price':total_price,'showing_movies':showing_movies}
        return render(request,'useradmin/dashboard.html',context)
    else:
        return redirect('adminlogin')


def adminout(request):
    if request.session.has_key('username'):
        request.session.delete()
        return redirect('adminlogin')
    else:
        return redirect('adminlogin')


def theatremgmt(request):
    if request.session.has_key('username'):
        owner=Dealer.objects.all()
        context = {'owner':owner}
        return render(request,'useradmin/theatre_table.html',context)
    else:
        return redirect('adminlogin')


def ownerAdd(request):
    if request.session.has_key('username'):
        if request.method=="POST":
            ownername = request.POST['ownername']
            TheatreName = request.POST['TheatreName']
            number = request.POST['number']
            dealer_name = request.POST['ownername']
            theatre_name = request.POST['TheatreName']
            dealer_phone = request.POST['number']
            theatre_location = request.POST['place']
            theatre_close = request.POST['time']
            photo_main = request.POST['image64data']
            value = photo_main.strip('data:image/png;base64,')
            format, imgstr = photo_main.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)

            dicti = {"ownername":ownername,"TheatreName":TheatreName,"number":number}

            if User.objects.filter(first_name=TheatreName).exists():
                messages.error(request,'Theatre Name is already Exist')
                return render(request,'useradmin/theatre_add_owner.html',dicti)
            elif User.objects.filter(username=ownername).exists():
                messages.error(request,"Username is already taken") 
                return render(request,'useradmin/theatre_add_owner.html',dicti)
            elif User.objects.filter(last_name=number).exists():
                messages.error(request,"Phone Number is Exist") 
                return render(request,'useradmin/theatre_add_owner.html',dicti)
            else:
                user = User.objects.create_user(username=ownername,first_name=TheatreName,last_name=number,is_staff=True)
                user.save();
                dealer = Dealer.objects.create(theatre_close=theatre_close,theatre_location=theatre_location,dealer_name=dealer_name,theatre_name=theatre_name,dealer_phone=dealer_phone,theatre_image=data,user_id=user)
                dealer.save();
                print("USER CREATED")
                return redirect(theatremgmt)
        else:
            return render(request,'useradmin/theatre_add_owner.html')
    else:
        return redirect('adminlogin')


def edit_theatre(request,id):
    theatre_info = Dealer.objects.get(id=id)
    if request.method == 'POST':
        theatre_info.dealer_name=request.POST['ownername']
        theatre_info.dealer_phone=request.POST['number']
        theatre_info.theatre_name=request.POST['TheatreName']
        theatre_info.theatre_location=request.POST['place']
        theatre_info.theatre_close=request.POST['time']
        theatre_image=request.POST.get('image64data')

        if theatre_image == "":
            dealer = Dealer.objects.get(id=id)
            theatre_info.theatre_image = dealer.theatre_image
        else:
            theatre_info.theatre_image=theatre_image
        print('check')
        theatre_info.save();
        return redirect(theatremgmt)
    context = {'theatre_info':theatre_info}
    return render(request,'useradmin/theatre_owner_edit.html',context)


def userList(request):
    user = User.objects.filter(is_staff=False,is_superuser=False)
    context = {'user':user}
    return render(request,'useradmin/userlist.html',context)


def userActivity(request):
    booked = Booked.objects.all() 
    context = {'booked':booked}
    return render(request,'useradmin/user_activity.html',context)


def delete(request,id):
    delete_user = Dealer.objects.get(id=id)
    delete_user.delete()
    return redirect('theatremgmt')


def delete_user(request,id):
    delete_user = User.objects.get(id=id)
    delete_user.delete()
    return redirect(userList)