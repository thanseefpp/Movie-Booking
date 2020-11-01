from django.shortcuts import render,redirect
from django.contrib import messages

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
            messages.error(request, "😢 Wrong username/password!")
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