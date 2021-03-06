from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('Theatre_Movies/<int:id>/',views.theatre_movies,name='theatre_movies'),
    path('login_page/',views.login,name='login'),
    path('register_page/',views.register,name='register'),
    path('otp/',views.otp,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('book_show/<int:id>/',views.book_show,name='book_show'),
    path('seat_select/<int:id>/',views.seat_book,name='seat_book'),
    path('checkout/',views.checkout,name='checkout'),
    path('checkout_Ticket/<int:price>/<str:val>/<int:id>/',views.orderPlace,name='order_place'),
    path('seatreconnect/',views.seatreconnect,name='seatreconnect'),
    path('booked_address/<int:id>/<int:pk>/',views.bookedAddress,name='booked_address'),
    path('pay_success/',views.pay_success,name='pay_success'),
    path('contact_us/',views.contact,name='contact'),
]

