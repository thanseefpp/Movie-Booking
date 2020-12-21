from django.urls import path

from .import views


urlpatterns = [
    path('admin/',views.adminlogin,name='adminlogin'),
    path('adminDashboard',views.adminDashboard,name='adminDashboard'),
    path('adminout/',views.adminout,name = 'adminout'),
    path('theatre_management/',views.theatremgmt,name='theatremgmt'),
    path('add_owner/',views.ownerAdd,name='ownerAdd'),
    path('user_list/',views.userList,name='user_list'),
    path('user_activity/',views.userActivity,name='user_activity'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('edit_theatre/<int:id>/',views.edit_theatre,name='edit_theatre'),
    path('delete_user/<int:id>/',views.delete_user,name='delete_user'),
    
]