from django.urls import path
from . import views
from compiler.submit.views import submit

app_name = 'problems' 

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('add/', views.add_problem, name='add_problem'),
    path('<int:p_id>/', views.problem_detail, name='problem_detail'),
   

]  
