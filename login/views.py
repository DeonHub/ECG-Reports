from django.shortcuts import render
from superuser.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from .models import *
from superuser.models import *
import requests
import datetime
import json
import random
import string
import os
import environ
from django.core.mail import EmailMessage
import base64
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    template_name = 'login/index.html'
    return render(request, template_name, {  
    })


@csrf_exempt
def login(request):
    template_name = 'login/login.html'
    page = 'Login'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin:
                return redirect('superuser:dashboard')
            if user.is_hospital:
                return redirect('hospital:dashboard')
            elif user.is_cardio:
                return redirect('cardio:dashboard')
            else:
                return redirect('login')
        else:
            messages.info(request, "Invalid email or password")
            return redirect('login:login')

    return render(request, template_name, {
        'page': page
    })


@csrf_exempt
def forgotPassword(request):
    template_name = 'login/forgot-password.html'
    page = 'Forgot Password'

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_active:

            token = random.randint(100000, 999999)


            # Send email
            subject = f'ACCOUNT VERIFICATION CODE'
            body = f"Your verification code is {token}."
            senders_mail = settings.EMAIL_HOST_USER
            to_address = [f'{email}']


            send_email = EmailMessage(subject, body, senders_mail, to_address)

            try:
                send_email.send()
            except: 
                print("Server error")
                pass

            verification = Verifications.objects.create(email=email, token=token)
            verification.save()

            messages.info(request, "Please check your email for a verification code")
            return redirect('login:verifyCode')

        else:
            messages.info(request, "Verification Failed. Please check the email address provided.")
            return redirect('login:forgotPassword')

    return render(request, template_name, {
        'page': page
    })



@csrf_exempt
def verifyCode(request):
    template_name = 'login/verify-code.html'
    page = 'Verify Code'

    if request.method == "POST":
        token = request.POST.get('token')

        try:
            code = Verifications.objects.get(token=token)
            code.verified = True
            code.save()

            random_string = ''.join([str(random.randint(0, 9)) for _ in range(64)])
            token = token+random_string

            token = base64.b64encode(token.encode("utf-8")).decode("utf-8")


            messages.success(request, 'Verification Successful. Please reset your password.') 
            return redirect('login:resetPassword', token) 
        
        except:
            messages.success(request, 'Verification Failed. Please check the email address provided.') 
            return redirect('login:verifyCode')  


    else:               
        return render(request,  template_name, {
            'page': page
        })



@csrf_exempt
def resetPassword(request, **kwargs):
    template_name = 'login/reset-password.html'
    page = 'Reset Password'

    token = kwargs.get('token')
    token = base64.b64decode(token).decode("utf-8")
    token = token[:6]


    if request.method == 'POST':
        password = request.POST.get('password')

        password = make_password(password)

        try:
            verification = Verifications.objects.get(token=token)
            admin = User.objects.get(email=verification.email)

            admin.password = password
            admin.save()

            verification.delete()
            verification.save()


            messages.success(request, 'Password reset successfully. Please login to continue')
        except:
            messages.success(request, 'Invalid or expired token. Please try again.')

        return redirect('login:login')

    else:
        return render(request, template_name, {
            'page': page,
            'token': token
        })



@csrf_exempt
def register(request):
    template_name = 'login/register.html'
    page = 'Account Registration'

    if request.method == 'POST':
        hospital_name = request.POST.get('hospital_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        password = request.POST.get('password')
        password = make_password(password)

        contact = request.POST.get('contact')
        country = request.POST.get('country')
        town = request.POST.get('town')
        address = request.POST.get('address')

        try:
            logo = request.FILES.get('logo')
        except:
            logo = None 


        try:
            hospital = User.objects.get(email=email)
            messages.error(request, 'Account with email already exists.') 
            return redirect('login:register')
        
        except:

            hospital = User.objects.create(username=username, email=email, password=password, is_hospital=True)
            hospital.save()

            Hospital.objects.filter(id=hospital.id).create(user_id=hospital.id, hospital_name=hospital_name, logo=logo, country=country, contact=contact, town=town, address=address, available_slots=available_slots)

            messages.success(request, 'Account was created cuccessfully. Please login to continue')
            return redirect('login:login')    

    return render(request, template_name, {
        'page': page
    })
