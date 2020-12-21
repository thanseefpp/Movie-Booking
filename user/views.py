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
from .models import *
from django.http.response import Http404
import razorpay
from datetime import *

def index(request):
    if request.user.is_authenticated:
        user=request.user
        email=request.user.email
        name=request.user.username
        customer = Customer.objects.get_or_create(user=user,name=name,email=email)
    else:
        pass
    dealer = Dealer.objects.all()
    context = {'dealer':dealer}
    return render(request,'user/index_theatre.html',context)


def theatre_movies(request,id):
    dealer = Dealer.objects.get(id=id)
    movie = NowShowingMovies.objects.filter(dealer=dealer)
    upcoming = UpcomingMovies.objects.filter(dealer=dealer)
    context = {'movie':movie,'upcoming':upcoming}
    return render(request,'user/index_movies.html',context)


def book_show(request,id):
    movie = NowShowingMovies.objects.filter(id=id)
    for i in movie:
        date = i.show_date
    context = {'movie':movie,'show_time':date}
    return render(request,'user/index_movie_details.html',context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        content = request.POST['content']
        dict = {
            'name':name,
            'email':email,
            'subject':subject,
        }
        table = Contact.objects.create(name=name,email=email,subject=subject,contents=content)
        table.save();
        messages.success(request,'Contact form successfully submitted')
        return render(request,'user/contact.html',dict)

    return render(request,'user/contact.html')


def seat_book(request,id):
    movie = NowShowingMovies.objects.get(id=id)
    if  SeatSelected.objects.filter(movie=movie).exists():
        screen = SeatSelected.objects.filter(movie=movie)
        listed_val = []
        list = []
        for i in screen:
            value = i.occupied_seats
            splited = value.split(",")
            for j in splited:
                listed_val.append(j)
                
        occupaid_values = listed_val
        print('occu',occupaid_values)
    else:
        list = ''
        occupaid_values = json.dumps(list)
        print('list:',occupaid_values)

    print('movie choose')
    val=movie.id
    # print('id :',val)
    screen_count = movie.screen
    # print('screen :',screen_count)
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

    context = {'movie_id':val,'row_count':row_count,'normal_price':normal_price,
    'executive_price':executive_price,'vip_price':vip_price,'screen':screen_count,
    'vip_seats':vip_seats,'premium_seats':premium_seats,'executive_seats':executive_seats,
    'normal_seats':normal_seats,'premium_price':premium_price,'totalSeat':value,'occupaid':occupaid_values}
    return render(request,'user/seats.html',context)



def checkout(request):
    if request.method == 'POST':
        selectedSeats = request.POST.get('seatNumber')
        totalSeatprice = request.POST.get('totalPrice')
        print('selectedSeats:',selectedSeats,'totalprice:',totalSeatprice)
        dict = {'selectseat':selectedSeats,'totalSeatprice':totalSeatprice}
        return JsonResponse(dict,safe=False)
    else:
        pass


def orderPlace(request,price,val,id):
    try:
        client = razorpay.Client(auth=("rzp_test_eMnSXZs7JW5fj7", "v12bdGlbSimIYQOff93S9ziv"))
        order_amount = price
        order_amount *= 100
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'

        #creating Order
        response = client.order.create(dict(amount=order_amount,currency=order_currency,receipt=order_receipt,payment_capture='0'))
        order_id = response['id']
        order_status = response['status']
        
        print('id',id)
        print('seat',val)
        print('price',price)
        movie = NowShowingMovies.objects.get(id=id)
        dealer=movie.dealer.id
        movie_id=movie.id
        print('dealer:',dealer,movie_id)

        seatvalues = val
        print('seat:',seatvalues)
        totalprice = price
        context = {'movie':movie,'seatvalues':seatvalues,'totalprice':totalprice,
        'order_id':order_id,'dealer':dealer,'movie_id':movie_id}
        return render(request,'user/index_checkout.html',context)
    except:
        raise Http404("Page does not exist")
    


def bookedAddress(request,id,pk):
    if request.method == 'POST':
        transaction_id = datetime.now().timestamp()
        firstname = request.POST.get('firstname')
        number = request.POST.get('number')
        email = request.POST.get('email')
        totalPrice = request.POST.get('totalPrice')
        selectedSeats = request.POST.get('selectedSeats')
        payment_status = request.POST.get('payment_status')
        print('payment_status',payment_status)
        movieid = NowShowingMovies.objects.get(id=pk)
        dealerid = Dealer.objects.get(id=id)
        movie_id = movieid.id
        dealer_id = dealerid.id

        screentable = SeatSelected.objects.create(dealer=dealerid,movie=movieid,occupied_seats=selectedSeats)
        screentable.save();

        print('screenselet_table_check :',screentable)
        date_now = datetime.now()
        print('datetime:',date_now)
        customer = request.user.customer
        user = User.objects.get(username=request.user)
        print('User:',user)
        customer= Customer.objects.get(user=user)
        print('customer id:',customer)
        booking = Booked.objects.create(customer=customer,email=email,phone_number=number,
            firstname=firstname,paid_amount=totalPrice,transaction_id=transaction_id,
            payment_status=payment_status,complete=True,date_booking=date_now,
            dealer=dealerid,seatSelect=screentable)
        booking.save();

        return JsonResponse('hi',safe=False)
    else:
        pass


def pay_success(request):
    user = request.user
    customer = Customer.objects.filter(user=user.id)
    for i in customer:
        value = i.id
    booked_details = Booked.objects.filter(customer=value)
    # print('csmr',booked_details)
    for k in booked_details:
        dealer = k.dealer
    dealer_id = dealer.id
    for i in booked_details:
        seat_id = i.seatSelect
    seat = SeatSelected.objects.filter(id=seat_id.id)
    for j in seat:
        movie = j.movie
    dealer_table = Dealer.objects.filter(id=dealer_id)
    for i in dealer_table:
        theatre_name = i.theatre_name
    context = {'booked_details':booked_details,'theatre_name':theatre_name,
        'seat_id':seat_id,'movie':movie}
    return render(request,'user/pay_success.html',context)


def seatreconnect(request):
    if request.method == 'GET':
        seatCount = request.GET.get('seatCount', None)
        seatNumber = request.GET.get('seatNumber', None)
        typeOfSeat = request.GET.get('typeOfSeat', None)
        totalPrice = request.GET.get('totalPrice', None)
        selectedSeats = request.GET.get('selectedSeats', None)
        selectedMoviePrice = request.GET.get('selectedMoviePrice', None)
        print('get function check:',seatCount,seatNumber,typeOfSeat,selectedSeats,totalPrice,selectedMoviePrice)
        return JsonResponse(seatNumber,safe=False)


# Login , Register , OTP , Logout

def login(request):
    if request.user.is_authenticated:
        return redirect(index)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        dict = {'username':username}
        print('user',user)
        if user is not None:
            print('checking')
            if user.is_staff == False and user.is_superuser == False:    
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
        number = request.POST['number']
        email = request.POST['email']
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
                'Authorization': 'Token 2b42f2e1762714e2ec4f9923541d795bf87ecc23'
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


def otp(request,backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':
        otp=request.POST['otp']
       
        id=request.session['id']
        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': id,
        'otp_code': otp}
        files = [

        ]
        headers = {
        'Authorization': 'Token 2b42f2e1762714e2ec4f9923541d795bf87ecc23'
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

            auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
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
