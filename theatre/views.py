from django.shortcuts import render,redirect
from django.contrib import messages

# Create your views here.

def theatreLogin(request):
    return render(request,'Theatrelogin.html')