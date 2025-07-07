from django.urls import path
from . import views

app_name = 'problems' 

urlpatterns = [
    path('', views.problem_list, name='problem_list'),

    path('add/', views.add_problem, name='add_problem'),
    # path('up/<int:f_oid>', views.updateView, name= 'updateProblem'),
    # path('del/<int:f_oid>', views.deleteView, name= 'deleteProblem'),
    path('<int:p_id>/', views.show_problem, name='showProblem'),
]