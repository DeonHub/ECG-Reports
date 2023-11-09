from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
import requests
import datetime
import json
import random
import string
import os
import environ
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
@login_required(login_url='login:login')
@csrf_exempt
def dashboard(request):
    template_name = 'superuser/dashboard.html'
    user=request.user
    # user_id=request.user.id
    page = 'Admin Dashboard'
    today = datetime.date.today()
    year_range = request.GET.get('year_range', today.year)
    if year_range:
        year = int(year_range)
    else:
        year = today.year

    total_cardiologists = Cardiologist.objects.all().count()
    total_cardiologists_male = Cardiologist.objects.filter(gender=1).count()
    total_cardiologists_female = Cardiologist.objects.filter(gender=2).count()

    total_hospitals = Hospital.objects.all().count()

    total_reports = ReportHistory.objects.all().count()
    total_completed = ReportHistory.objects.filter(completed=True).count()
    total_pending = ReportHistory.objects.filter(status='Pending Review').count()

    try:
        credit = Credit.objects.all().first()
        total_amount = credit.total_amount
        total_slots = credit.total_slots
    except:
        total_amount = 0.00
        total_slots = 0    


    january_amount=0
    february_amount=0
    march_amount=0
    april_amount=0
    may_amount=0
    june_amount=0
    july_amount=0
    august_amount=0
    september_amount=0
    october_amount=0
    november_amount=0
    december_amount=0


    january = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=1, date_created__year=year)]
    february = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=2, date_created__year=year)]
    march = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=3, date_created__year=year)]
    april = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=4, date_created__year=year)]
    may = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=5, date_created__year=year)]
    june = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=6, date_created__year=year)]
    july = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=7, date_created__year=year)]
    august = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=8, date_created__year=year)]
    september = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=9, date_created__year=year)]
    october = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=10, date_created__year=year)]
    november = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=11, date_created__year=year)]
    december = [int(x.amount) for x in PurchaseHistory.objects.filter(date_created__month=12, date_created__year=year)]
    
    


    for i in january:
        january_amount += i

    for i in february:
        february_amount += i  

    for i in march:
        march_amount += i 

    for i in april:
        april_amount += i  

    for i in may:
        may_amount += i  

    for i in june:
        june_amount += i  

    for i in july:
        july_amount += i

    for i in august:
        august_amount += i

    for i in september:
        september_amount += i

    for i in october:
        october_amount += i

    for i in november:
        november_amount += i

    for i in december:
        december_amount += i  



    data1 = [total_cardiologists, total_cardiologists_male, total_cardiologists_female, total_hospitals, total_reports, total_completed, total_pending, total_amount, total_slots]
    data2 = [january_amount, february_amount, march_amount, april_amount, may_amount, june_amount, july_amount, august_amount, september_amount, october_amount, november_amount, december_amount]

    return render(request, template_name, {
        'page': page,

        'total_cardiologists': total_cardiologists,
        'total_cardiologists_male': total_cardiologists_male,
        'total_cardiologists_female': total_cardiologists_female,
        'total_hospitals': total_hospitals,
        'total_reports': total_reports,
        'total_completed': total_completed,
        'total_pending': total_pending, 
        'total_amount': total_amount,
        'total_slots': total_slots, 
        'data1': data1,
        'data2': data2,
        'year': year,
        'year_range': year_range,
    })




# Create Fee types
@login_required(login_url='login:login')
def createCardio(request, **kwargs):
    template_name = 'superuser/add-cardio.html'
    page = 'Add Cardiologist'


    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = f'{first_name} {last_name}'
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        town = request.POST.get('town') if request.POST.get('town') else ''

        password = request.POST.get('contact')
        password = make_password(password)

        try:
            profile = request.FILES.get('profile')
        except:
            profile = None 


        try:
            cardio = User.objects.get(email=email)
            messages.error(request, 'Cardiologist with email already exists.') 
            return redirect('superuser:createCardio')
        
        except:

            cardio = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_cardio=True)
            cardio.save()

            Cardiologist.objects.filter(id=cardio.id).create(user_id=cardio.id, gender=gender, profile=profile, country=country, contact=contact, town=town)

            messages.success(request, 'Cardiologist was added cuccessfully')
            return HttpResponseRedirect(reverse('superuser:viewCardios'))      

    else:
        return render(request, template_name, {
            'page': page,
            
        })




# View fee type
@login_required(login_url='login:login')
def viewCardios(request, **kwargs):
    template_name = 'superuser/view-cardios.html'
    user=request.user
    page = 'View Cardiologists'

    cardios = Cardiologist.objects.all()

    return render(request, template_name, {
        'page': page,
        'cardios': cardios
    })



# Edit invoice details
@login_required(login_url='login:login')
def editCardioDetails(request, id, **kwargs):

    template_name = 'superuser/edit-cardio.html'
    user=request.user
    page = 'Edit Cardiologist Detail'    


    cardiologist = Cardiologist.objects.get(id=id)
    cardio = User.objects.get(id=cardiologist.user.id)
    # print(cardiologist.user.id)
    
    if request.method == 'POST':

        new_profile = request.FILES.get('profile', None)
        if new_profile is not None:
            cardiologist.profile = request.FILES.get('profile', None)

        cardio.first_name = request.POST.get('first_name')
        cardio.last_name = request.POST.get('last_name')
        cardio.username = f"{request.POST.get('first_name')} {request.POST.get('last_name')}"
        cardio.email = request.POST.get('email')
        cardio.save()
        
        

        cardiologist.contact = request.POST.get('contact')
        cardiologist.gender = request.POST.get('gender')
        cardiologist.country = request.POST.get('country') if request.POST.get('country') else cardiologist.country
        cardiologist.town = request.POST.get('town')
        cardiologist.save() 
        


        messages.success(request, 'Cardiologist details updated successfully!')
        return redirect('superuser:viewCardios') 


    return render(request, template_name, {
        'cardiologist': cardiologist,
        'page': page,
    }) 




@login_required(login_url='login:login')
def viewCardioDetails(request, **kwargs):
    
    template_name = 'superuser/view-cardio-details.html'
    page = 'View Cardiologist Details'
    pk = kwargs.get('pk')


    cardiologist = get_object_or_404(Cardiologist, pk=pk)

    return render(request, template_name, {
        'cardiologist': cardiologist,
        'page': page
        })





# Delete fee type
def deleteCardio(request, id, *args, **kwargs):
 
    if request.method == "POST":
        cardio = Cardiologist.objects.get(id=id)
        user = User.objects.get(id=cardio.user.id)

        cardio.delete()
        user.delete()

    messages.success(request, 'Cardiologist account deleted successfully!')
    return redirect('superuser:viewCardios')




# Hospitals
@login_required(login_url='login:login')
def viewHospitals(request, **kwargs):
    template_name = 'superuser/view-hospitals.html'
    user=request.user
    page = 'View Hospitals'

    hospitals = Hospital.objects.all()

    return render(request, template_name, {
        'page': page,
        'hospitals': hospitals
    })



@login_required(login_url='login:login')
def viewHospitalDetails(request, **kwargs):
    
    template_name = 'superuser/view-hospital-details.html'
    page = 'View Hospital Details'
    pk = kwargs.get('pk')


    hospital = get_object_or_404(Hospital, pk=pk)

    return render(request, template_name, {
        'hospital': hospital,
        'page': page
        })



# Delete fee type
def deleteHospital(request, id, *args, **kwargs):
 
    if request.method == "POST":
        hospital = Hospital.objects.get(id=id)
        user = User.objects.get(id=hospital.user.id)

        hospital.delete()
        user.delete()

    messages.success(request, 'Hospital account deleted successfully!')
    return redirect('superuser:viewCardios')




@login_required(login_url='login:login')
def purchaseHistory(request, **kwargs):
    template_name = 'superuser/purchase-history.html'
    page = "Admin Purchase History"

    purchases = PurchaseHistory.objects.filter(completed=True)

    return render(request, template_name, {
        'purchases': purchases,
        'page': page

    })

@login_required(login_url='login:login')
def viewPurchaseDetails(request, **kwargs):
    
    template_name = 'superuser/view-purchase-details.html'
    page = 'View Purchase Details'
    pk = kwargs.get('pk')


    purchase = get_object_or_404(PurchaseHistory, pk=pk)

    return render(request, template_name, {
        'purchase': purchase,
        'page': page
        })



@login_required(login_url='login:login')
def reportHistory(request):
    template_name = 'superuser/report-history.html'
    page = "View Report History"


    reports = ReportHistory.objects.all()

    return render(request, template_name, {
        'reports': reports,
        'page': page

    })



@login_required(login_url='login:login')
def viewReportDetails(request, **kwargs):
    
    template_name = 'superuser/view-report-details.html'
    page = 'View Report Details'
    pk = kwargs.get('pk')

    report = get_object_or_404(ReportHistory, pk=pk)

    return render(request, template_name, {
        'report': report,
        'page': page,

        })


@login_required(login_url='login:login')
def resetPassword(request):
    template_name = 'superuser/reset-password.html'
    page = 'Reset Password'
    user=request.user


    if request.method == 'POST':
        password = request.POST.get('password')

        password = make_password(password)
        admin = User.objects.get(id=user.id)

        admin.password = password
        admin.save()

        messages.success(request, 'Password reset successfully!')
        return redirect('superuser:dashboard')

    else:
        return render(request, template_name, {
            'page': page
        })


def user_logout(request):
    logout(request)
    return redirect('login:login') 