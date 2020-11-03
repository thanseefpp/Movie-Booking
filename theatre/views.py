from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Screen

# Create your views here.


def theatreLogin(request):
    if request.user.is_staff:
        owner = User.objects.filter(is_staff=True)
        return redirect('theatreDashboard')

    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            auth.login(request,user)
            return redirect(theatreDashboard)
        else:
            messages.error(request, '😢 Wrong username/password! 😢')
            return redirect('theatreLogin')
    else:
        return render(request,'Theatre/Theatrelogin.html')


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
        screen = Screen.objects.all()
        for i in screen:
            total = i.vip_seats
            total2 =i.normal_seats
            total3 = i.executive_seats
            total4 = i.premium_seats
            total5= total+total2+total3+total4
        print(total5)
        context = {'screen':screen,'total':total5}
        return render(request,'Theatre/screen_manage.html',context)
    else:
        return redirect('theatreLogin')

 # total_seats = Screen.objects.annotate(i_sum= F('vip_seats')+ F('premium_seats')).filter(i_sum=200)

def addScreens(request):
    if request.user.is_staff:
        if request.method == 'POST':
            screen_table=Screen()
            screen_name = request.POST['screen_name']
            vip_seat = request.POST['vip_seat']
            premium_seat = request.POST['premium_seat']
            executive_seat = request.POST['executive_seat']
            normal_seat = request.POST['normal_seat']
            screen_table = Screen(screen_name=screen_name,vip_seats=vip_seat,premium_seats=premium_seat,executive_seats=executive_seat,normal_seats=normal_seat)
            print(screen_table)
            screen_table.save()
            return redirect('screens')
        else:
            return render(request,'Theatre/addscreen.html')
    else:
        return redirect('theatreLogin')
    