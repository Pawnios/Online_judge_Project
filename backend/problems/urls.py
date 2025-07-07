from django.urls import path
from . import views

app_name = 'problems' 

urlpatterns = [
    path('', views.problemFormView, name='list'),
    path('ofv/', views.problemFormView, name='problem_form_view'),
    # path('sv/', views.showView, name='showProblem'),
    # path('up/<int:f_oid>', views.updateView, name= 'updateProblem'),
    # path('del/<int:f_oid>', views.deleteView, name= 'deleteProblem'),
]