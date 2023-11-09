import json
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import requests
from superuser.models import *
import environ
import datetime
import random
import string
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt


env = environ.Env()
environ.Env.read_env()


TEST_SECRET_KEY=env('TEST_SECRET_KEY')
LIVE_SECRET_KEY=env('LIVE_SECRET_KEY')


# Create your views here.
@login_required(login_url='login:login')
@csrf_exempt
def dashboard(request):
    template_name = 'hospital/dashboard.html'
    user=request.user
    # user_id=request.user.id
    page = 'Hospital Dashboard'
    hospital = Hospital.objects.get(user_id=user.id)
    # hospital_name = hospital.hospital_name.upper()
    available_slots = hospital.available_slots

    total_reports = ReportHistory.objects.filter(hospital=hospital).count()
    total_completed = ReportHistory.objects.filter(hospital=hospital, completed=True).count()
    total_pending = ReportHistory.objects.filter(hospital=hospital, status='Pending Review').count()

    return render(request, template_name, {
        'page': page,
        'hospital': hospital,
        'available_slots': available_slots,

        'total_reports': total_reports,
        'total_completed': total_completed,
        'total_pending': total_pending,
    })


def remove_non_numeric(string):
    return ''.join(filter(str.isdigit, string))
    

@csrf_exempt
def load_link(request):
    template_name = 'hospital/link.html'
    user = request.user
    

    if request.method == 'POST': 
        info = request.POST.get('info')
        info = json.loads(info)
 
        user_id = info['user_id']
        hospital = Hospital.objects.get(user_id=user_id)

        email = info['email']
        slots = info['slots']
        amount = info['amount']
        amount = float(amount)

        total_amount = amount * 100
        total_amount = int(total_amount)


        now = datetime.datetime.now()
        invoice_no = remove_non_numeric(str(now))


        purchase = PurchaseHistory.objects.create(
            invoice_no=invoice_no,
            hospital=hospital,
            amount=amount,
            slots_bought=slots
        )
        purchase.save()


        # 100ps = GHS 1 

        url = "https://api.paystack.co/transaction/initialize"

        payload = json.dumps({
            "amount": total_amount,
            "email": email
        })
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TEST_SECRET_KEY}',
        'Cookie': '__cf_bm=8sacAExva.ukx_O5_UIA3ADKjlyZN2jdncsgYe37kuA-1691082991-0-AQVXZihJHivW9qyNq2g19KbiVj0rVUKXpIPg85C2iwJp/9w0wUzRXqboUv31FremjpM0aEu0P1vEMq523e35mm0=; sails.sid=s%3AEB2jwX5vCughtr-rOqxbw1m4eBDPY772.668XInXm6aEPcviAmNTgSVf02FWB7rS8w7zAqNNwp0I'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        url = response['data']['authorization_url']
        access_code = response['data']['access_code']
        reference = response['data']['reference']


        purchase.reference=reference
        purchase.save()

        return render(request, template_name, {'response': url})



@csrf_exempt
def purchaseHistory(request, **kwargs):
    template_name = 'hospital/purchase-history.html'
    page = "Hospital Purchase History"

    user = request.user
    hospital = Hospital.objects.get(user_id=user.id)

    hospital_name = hospital.hospital_name.upper()
    available_slots = hospital.available_slots

    trxref = request.GET.get('trxref')
    reference = request.GET.get('reference')

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    payload = {}
    headers = {
    'Authorization': f'Bearer {TEST_SECRET_KEY}',
    'Cookie': '__cf_bm=w.HWO0alHmjK2DRbYrFN_w51lbwKgbOlNK32CF_HpcA-1691179963-0-AcBR9QqY/fu86rLS5g9bOBLD+VVwf8XuA8C12jxI/LAeaetk/Wi9hwWWu2sNL+XEfDPA3gW/P56kOASp05XFzCg=; sails.sid=s%3Am7rvH9vM9-6TLU06BoSA0wncwno0m58F.CGwlclRV57YzESptIo4JhBbkceQ40rAGjIzo8cWAW5s'
    }

    status = requests.request("GET", url, headers=headers, data=payload).json()['status']


    if status:
        purchase = PurchaseHistory.objects.get(reference=reference)
        purchase.completed = True
        purchase.save()

        hospital = Hospital.objects.get(user_id=user.id)
        hospital.available_slots += int(purchase.slots_bought)
        hospital.save()

        try:
            credit = Credit.objects.all().first()
            credit.total_amount += float(purchase.amount)
            credit.total_slots += int(purchase.slots_bought)
            credit.save()
        except:
            credit = Credit.objects.create(total_amount=float(purchase.amount), total_slots=int(purchase.slots_bought))  
            credit.save() 


    purchases = PurchaseHistory.objects.filter(completed=True, hospital=hospital)

    return render(request, template_name, {
        'purchases': purchases,
        'hospital': hospital,
        'available_slots':available_slots,
        'page': page

    })





@login_required(login_url='login:login')
@csrf_exempt
def purchaseSlot(request):
    template_name = 'hospital/buy-slot.html'
    page = 'Slot Subscription'
    user=request.user
    hospital = Hospital.objects.get(user_id=user.id)
    hospital_name = hospital.hospital_name.upper()
    available_slots = hospital.available_slots
    email = hospital.user.email


    return render(request, template_name, {
        'page': page,
        'hospital': hospital,
        'available_slots': available_slots,
        'email': email,
        'user_id': user.id

    })


def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(y))


@login_required(login_url='login:login')
@csrf_exempt
def uploadImage(request):
    template_name = 'hospital/upload-image.html'
    page = 'Upload Image/File'
    user=request.user
    hospital = Hospital.objects.get(user_id=user.id)
    hospital_name = hospital.hospital_name.upper()
    available_slots = hospital.available_slots
    email = hospital.user.email


    if request.method == 'POST':
        image = request.FILES.get('image')
        patient_name = request.POST.get('patient_name')
        patient_type = request.POST.get('patient_type')
        patient_age = request.POST.get('patient_age')
        patient_number = request.POST.get('patient_number')


        codex = random.randint(10000, 99999)
        chars = random_char(3)
        report_number = f'{chars}{codex}'


        try:
            existing_code = ReportHistory.objects.get(report_number=report_number).report_number

            while True:
                if report_number == existing_code:
                    codex = random.randint(10000, 99999)
                    chars = random_char(3)

                    report_number = f'{chars}{codex}'
                else:
                    break    
        except:
            pass

        report = ReportHistory.objects.create(hospital=hospital, image=image, patient_name=patient_name, patient_type=patient_type, patient_age=patient_age, patient_number=patient_number, report_number=report_number, status='Pending Review')
        report.save()


        # hospital = Hospital.objects.get(user_id=user.id)
        # hospital.available_slots -= 1
        # hospital.save()

        messages.success(request, 'Image/File uploaded successfully!')
        return redirect('hospital:reportHistory') 

    else:
        return render(request, template_name, {
            'page': page,
            'hospital': hospital,
            'available_slots': available_slots,
            'email': email
        })


@login_required(login_url='login:login')
@csrf_exempt
def reportHistory(request):
    template_name = 'hospital/report-history.html'
    page = "Hospital Report History"

    user = request.user
    hospital = Hospital.objects.get(user_id=user.id)

    hospital_name = hospital.hospital_name.upper()
    available_slots = hospital.available_slots

    reports = ReportHistory.objects.filter(hospital=hospital)

    return render(request, template_name, {
        'reports': reports,
        'hospital': hospital,
        'available_slots':available_slots,
        'page': page

    })



@login_required(login_url='login:login')
@csrf_exempt
def viewReportDetails(request, **kwargs):
    
    template_name = 'hospital/view-report-details.html'
    page = 'View Report Details'
    pk = kwargs.get('pk')

    user = request.user
    hospital = Hospital.objects.get(user_id=user.id)

    hospital_name = hospital.hospital_name.upper()
    available_slots = hospital.available_slots

    report = get_object_or_404(ReportHistory, pk=pk)

    return render(request, template_name, {
        'report': report,
        'page': page,
        'hospital': hospital,
        'available_slots':available_slots

        })


@login_required(login_url='login:login')
@csrf_exempt
def resetPassword(request):
    template_name = 'hospital/reset-password.html'
    page = 'Reset Password'
    user=request.user

    hospital = Hospital.objects.get(user_id=user.id)
    hospital_name = hospital.hospital_name.upper()

    if request.method == 'POST':
        password = request.POST.get('password')

        password = make_password(password)
        clinic = User.objects.get(id=user.id)

        clinic.password = password
        clinic.save()

        messages.success(request, 'Password reset successfully!')
        return redirect('hospital:dashboard')

    else:
        return render(request, template_name, {
            'page': page,
            'hospital': hospital,
        })



@login_required(login_url='login:login')
@csrf_exempt
def viewProfile(request, **kwargs):
    
    template_name = 'hospital/view-profile.html'
    page = 'View Profile'

    user=request.user
    hospital = Hospital.objects.get(user_id=user.id)
    hospital_name = hospital.hospital_name.upper()


    return render(request, template_name, {
        'page': page,
        'hospital_name': hospital_name,
        'hospital': hospital
        })



@login_required(login_url='login:login')
@csrf_exempt
def updateProfile(request, **kwargs):
    
    template_name = 'hospital/update-profile.html'
    page = 'Update Profile'

    user=request.user
    hospital = Hospital.objects.get(user_id=user.id)
    hospital_name = hospital.hospital_name.upper()
    cardio = User.objects.get(id=hospital.user.id)


    if request.method == 'POST':
        
            new_logo = request.FILES.get('logo', None)
            if new_logo is not None:
                hospital.logo = request.FILES.get('logo', None)


            cardio.username = request.POST.get('username')
            cardio.email = request.POST.get('email')
            cardio.save()
            

            hospital.hospital_name = request.POST.get('hospital_name')
            hospital.contact = request.POST.get('contact')
            
            hospital.gender = request.POST.get('gender')
            hospital.country = request.POST.get('country') if request.POST.get('country') else hospital.country
            hospital.town = request.POST.get('town')
            hospital.address = request.POST.get('address')
            hospital.save() 
            


            messages.success(request, 'Hospital details updated successfully!')
            return redirect('hospital:viewProfile') 

    else:
        return render(request, template_name, {
            'page': page,
            'hospital_name': hospital_name,
            'hospital': hospital
            })




@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect('login:login') 