from django.shortcuts import render,HttpResponseRedirect, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login


# Create your views here.

def home_page(request):
    return render(request,'accounts/home.html')

def login_attempt(request):
    if(request.method=='POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request,'Username Doesnot exists.')
            return redirect('/login')
        
        user = authenticate(username=username,password=password)
        if user is  None:
            messages.error(request,'Wrong Username or Password')
            return render(request,'accounts/login.html')
        
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if (not profile_obj.is_verified):
            messages.error(request,'Profile not verified. Check your mail.')
            return render(request,'accounts/login.html')

        
        login(request,user)
        return redirect('/home')



    return render(request,'accounts/login.html')

def register_attempt(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        print('***********')
        print(username)
    

        if ( User.objects.filter(username=username).first()):
            messages.success(request,'Username is already taken')
            return HttpResponseRedirect('accounts/register.html')
        
        if (User.objects.filter(email=email).first()):
            messages.success(request,'Email is already taken')
            return HttpResponseRedirect('accounts/register.html')
        
        user_obj = User.objects.create(username = username,email=email)
        user_obj.set_password(password)
        user_obj.save()

        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_after_registration(email,auth_token)
        return render(request,'accounts/token_send.html')

        
        





    return render(request,'accounts/register.html')


def success(request):
    return render(request,'accounts/success.html')


def token_send(request):
    return render(request,'accounts/token_send.html')

def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token= auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your Account is already verified.')
                return redirect('/login')


            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your Account has been verified.')
            return render(request,'accounts/login.html')
        
        else:
            return redirect('/error')
    
    except Exception as e:
        print(e)


def send_mail_after_registration(email, token):
    subject = 'Your account needs to be verified.'
    message = f'Hi paste this link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER

    print('*******************')
    print(email_from)

    recipient_list = [email]
    print(recipient_list)

    send_mail(subject,message,email_from,recipient_list)

def error(request):
    return render(request,'accounts/error.html')


