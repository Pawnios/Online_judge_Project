from django.urls import path
from executor.views import submit_compile

urlpatterns = [
    path("", submit_compile, name="submitcompile"),
]