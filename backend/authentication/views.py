from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required
def homepage(request):
    template=loader.get_template("homepage.html")
    context={

    }
    return HttpResponse(template.render(context,request))

#register user
def register_user(request):
    #if the method is post
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username) #find user objects similar to username

    #if user exists then dont create it
        if user.exists():
            messages.info(request,'User with Username f`{username}` already exists!')
            return redirect("/register")
        
    #create this user
        user=User.objects.create_user(username=username)

        user.set_password(password)
        user.save()
        messages.info(request,'You have registered successfully!')
        return redirect('/register')
    
    #if the method is get
    template=loader.get_template('register.html')
    context={}
    return HttpResponse(template.render(context,request))

#login
def login_user(request):
    #if the method is post
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

    
        if not User.objects.filter(username=username).exists():
            messages.info(request,'This username does not exists!')
            return redirect('/login')
        
        user=authenticate(username=username,password=password)

        if user is None:
            messages.info(request, 'Invalid Password!')
            return redirect('/login')
            
        login(request,user)
        messages.info(request,'Login Successful')
        return redirect('/') 
    
    template=loader.get_template('login.html')
    context={}
    return HttpResponse(template.render(context,request))

@login_required
def logout_user(request):
    logout(request)
    messages.info(request,'Logout Successful')
    return redirect('/')