from django.urls import path
from . import views

app_name = 'submission'

urlpatterns = [
    path('run/<int:p_id>/', views.run_code, name='run_code'),
    path('submit/<int:p_id>/', views.submit_code, name='submit_code'),
    path('history/<int:p_id>/', views.submission_history, name='submission_history'),
    path('detail/<int:submission_id>/', views.detail, name='detail'),
    path('ai/<int:p_id>/', views.ai_helper, name='ai_helper'),
]