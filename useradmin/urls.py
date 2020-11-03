from django.urls import path

from .import views


urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('adminDashboard',views.adminDashboard,name='adminDashboard'),
    path('adminout/',views.adminout,name = 'adminout'),
    path('theatre_management/',views.theatremgmt,name='theatremgmt'),
    path('add_owner/',views.ownerAdd,name='ownerAdd'),
]