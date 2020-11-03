from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.

def theatreLogin(request):
    if request.user.is_authenticated:
        owner = User.objects.filter(is_staff=True)
        if owner.is_staff=True:
            return redirect('theatreDashboard')
        else:
            return redirect('')
    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect(index)
        else:
            messages.error(request, '😢 Wrong username/password!')
            return redirect('login')
    else:
        return render(request,'login.html')  
    return render(request,'Theatre/Theatrelogin.html')

def theatreDashboard(request):
    return render(request,'Theatre/theatredashboard.html')