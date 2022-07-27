import profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
# Create your views here.

def home(request):
    context = {}
    return render(request,'home.html',context)

def loginViews(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'User not found')
            return redirect('/login')
        
        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request,'profile is not verifyed check your email')
            return redirect('/login')

        user = authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'wrong password')
            return redirect('/login')

        login(request,user)
        return redirect('/')

    return render(request,'login.html')

def regitserView(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:

            if User.objects.filter(username=username).first():
                messages.success(request,'User name is takan')
                return redirect('/register')
            
            if User.objects.filter(email=email).first():
                messages.success(request,'Email is takan')
                return redirect('/register')

            user_obj = User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user=user_obj,auth_token = auth_token)
            profile_obj.save()
            send_mail_regitser(email , auth_token)

            return redirect('/token')
        except Exception as e:
            print(e)

    return render(request,'register.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'your acc is already verify')
                return redirect('/login')


            profile_obj.is_verified =True
            profile_obj.save()
            messages.success(request,'Your account has been verify')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def success(request):
    return render(request,'success.html')


def token_send(request):
    return render(request,'token_send.html')



def send_mail_regitser(email ,token):
    subject = "Your account is verifyed"
    message = f'Hi pastes the link http://localhost:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject , message,email_from,recipient_list)


def error_page(request):
    return render(request,'error.html')