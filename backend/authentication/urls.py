from django.urls import path,include
from authentication.views import register_user,login_user,logout_user,homepage

urlpatterns = [
    path('register/',register_user,name='register_user'),
    path('login/',login_user,name='login_user'),
    path('logout/',logout_user,name='logout_user'),
    path('homepage/',homepage ,name='homepage'),
]