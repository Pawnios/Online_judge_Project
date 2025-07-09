from django.urls import path,include
from authentication.views import register_user,login_user,logout_user,homepage, profile_view

urlpatterns = [
    path('register/',register_user,name='register_user'),
    path('login/',login_user,name='login_user'),
    path('logout/',logout_user,name='logout_user'),
    path('',homepage ,name='homepage'),
    path('profile/', profile_view, name='profile_view'),
]