from django.urls import path
from compiler.submit.views import submit

urlpatterns = [
    path("compiler", submit, name="submit"),
]