from django.urls import path

from .import views


urlpatterns = [
    path('theatre_login/',views.theatreLogin,name='theatreLogin'),
    path('theatre_dashboard/',views.theatreDashboard,name='theatreDashboard'),
    path('theatreout',views.theatreout,name='theatreout'),
    path('screen_management/',views.screens,name='screens'),
    path('add_screen/',views.addScreens,name='addScreens'),
    path('theatre_activity/',views.theatreUserActivity,name='theatre_user_activity'),
    path('upcoming_show/',views.upcomingShow,name='upcoming_show'),
    path('now_showing/',views.nowShow,name='now_show'),
    
]