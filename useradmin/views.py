from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.


def adminlogin(request):
    if request.session.has_key('username'):
        return redirect('adminDashboard')

    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        if username == 'thanseef' and password == '1234':
            request.session['username'] = username
            return redirect('adminDashboard')

        else:
            messages.error(request, "😢 Wrong username/password! 😢")
            return redirect(adminlogin)
    else:
        return render(request,'useradmin/adminlogin.html')
    


def adminDashboard(request):
    if request.session.has_key('username'):
        return render(request,'useradmin/adminDashboard.html')
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
        owner=User.objects.filter(is_staff=True)
        context = {'owner':owner}
        return render(request,'useradmin/admintheatre.html',context)
    else:
        return redirect('adminlogin')


def ownerAdd(request):
    if request.session.has_key('username'):
        if request.method=="POST":
            ownername = request.POST['ownername']
            TheatreName = request.POST['TheatreName']
            number = request.POST['number']
            password = request.POST['password']
            confirmpassword = request.POST['confirmpassword']
            dicti = {"ownername":ownername,"TheatreName":TheatreName,"number":number}
            if password == confirmpassword:
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
                    user = User.objects.create_user(username=ownername, password=password, first_name=TheatreName,last_name=number,is_staff=True)
                    user.save();
                    print("USER CREATED")
                    return redirect(theatremgmt)
            else:
                messages.error(request,'Password wrong')
                return render(request,'useradmin/theatre_add_owner.html',dicti)
        else:
            return render(request,'useradmin/theatre_add_owner.html')
    else:
        return redirect('adminlogin')


def userList(request):
    user = User.objects.filter(is_staff=False,is_superuser=False)
    context = {'user':user}
    return render(request,'useradmin/userlist.html',context)


def userActivity(request):
    return render(request,'useradmin/user_activity.html')