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
    path('addMovie/',views.addMovie,name='addMovie'),
    path('upcoming_movie/',views.upcomingMovie,name='upcoming_movie'),
    path('mobile/',views.mobile,name='mobile'),
    path('now_delete/<int:id>/',views.Nowdelete,name='now_delete'),
    path('now_update/<int:id>/',views.now_update,name='now_update'),
    path('screen_delete/<int:id>/',views.screen_delete,name='screen_delete'),
    path('screen_update/<int:id>/',views.screen_update,name='screen_update'),
    path('upcome_delete/<int:id>/',views.upcome_delete,name='upcome_delete'),
    path('upcome_update/<int:id>/',views.upcome_update,name='upcome_update'),
    

]