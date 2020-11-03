from django.urls import path

from .import views


urlpatterns = [
    path('theatre_login/',views.theatreLogin,name='theatreLogin'),
    path('theatre_dashboard/',views.theatreDashboard,name='theatreDashboard')
]