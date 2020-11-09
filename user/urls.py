from django.urls import path

from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login_page/',views.login,name='login'),
    path('register_page/',views.register,name='register'),
    path('otp/',views.otp,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('book_show/',views.bookShow,name='book_show'),
    
]

