import json
from django.conf import settings
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
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
@login_required(login_url='login:login')
@csrf_exempt
def dashboard(request):
    template_name = 'cardio/dashboard.html'
    user=request.user
    # user_id=request.user.id
    page = 'Cardiologist Dashboard'
    cardio = Cardiologist.objects.get(user_id=user.id)
    cardio_name = cardio.user.username.upper()

    total_hospitals = Hospital.objects.all().count()

    total_reports = ReportHistory.objects.all().count()
    total_completed = ReportHistory.objects.filter(completed=True).count()
    total_pending = ReportHistory.objects.filter(status='Pending Review').count()


    return render(request, template_name, {
        'page': page,
        'cardio_name': cardio_name,
        'total_hospitals': total_hospitals,
        'total_reports': total_reports,
        'total_completed': total_completed,
        'total_pending': total_pending,
    })



@login_required(login_url='login:login')
@csrf_exempt
def reportHistory(request):
    template_name = 'cardio/report-history.html'
    page = "View Report History"
    user=request.user
    cardio = Cardiologist.objects.get(user_id=user.id)
    cardio_name = cardio.user.username.upper()

    try:
        signature = cardio.signature.url
    except:
        signature = None    


    reports = ReportHistory.objects.all()

    return render(request, template_name, {
        'reports': reports,
        'page': page,
        'cardio_name': cardio_name,
        'signature': signature

    })


@login_required(login_url='login:login')
@csrf_exempt
def viewReportDetails(request, **kwargs):
    
    template_name = 'cardio/view-report-details.html'
    page = 'View Report Details'
    pk = kwargs.get('pk')
    user=request.user
    cardio = Cardiologist.objects.get(user_id=user.id)
    cardio_id = cardio.user.id
    cardio_name = cardio.user.username.upper()


    report = get_object_or_404(ReportHistory, pk=pk)

    return render(request, template_name, {
        'report': report,
        'page': page,
        'cardio_name': cardio_name,
        'cardio_id': cardio_id

        })


@csrf_exempt
def load_review(request):
    template_name = 'cardio/review.html'
    user=request.user
    cardio = Cardiologist.objects.get(user_id=user.id)
    cardio_name = cardio.user.username.upper()
    response = ''

    if request.method == 'POST': 
        report_id = request.POST.get('report_id')

        report_history = get_object_or_404(ReportHistory, pk=report_id)
        report_history.cardiologist = cardio
        report_history.status = "Under Review"
        report_history.save()
        

        return render(request, template_name, {'response': response})



@login_required(login_url='login:login')
@csrf_exempt
def reviewImage(request, **kwargs):
    
    template_name = 'cardio/review-image.html'
    page = 'Review Image'
    pk = kwargs.get('pk')
    user=request.user
    cardio = Cardiologist.objects.get(user_id=user.id)
    cardio_name = cardio.user.username.upper()


    report = get_object_or_404(ReportHistory, pk=pk)

    try:
        existing_report = Report.objects.get(report_history=report)
        existing = True

    except:
        existing_report = None
        existing = False


    return render(request, template_name, {
        'report': report,
        'page': page,
        'cardio_name': cardio_name,
        'existing': existing,
        'existing_report': existing_report

        })


@csrf_exempt
def finalizeReport(request):
    template_name = "cardio/finalize-report.html"
    user=request.user
    cardio = Cardiologist.objects.get(user_id=user.id)
    doctor_name = cardio.user.username.upper()
    appointment_date = 'Todays date'
    appointment_time = 'Ryt now'


    if request.method == 'POST':
        data = json.loads(request.body)

        report_id = data['report_id']
        report_history = ReportHistory.objects.get(id=report_id)
        email = report_history.hospital.user.email
        hospital_name = report_history.hospital.hospital_name


        clinical_information = data['clinical_information']
        report = data['report']
        rhythm = data['rhythm']
        rate = data['rate']
        p_wave = data['p_wave']
        st_segment = data['st_segment']
        pr_interval = data['pr_interval']
        qrs_complex = data['qrs_complex']
        t_wave = data['t_wave']
        axis = data['axis']
        r_wave_progression = data['r_wave_progression']
        sokolow_lyon_index = data['sokolow_lyon_index']
        r_wave_in_avl = data['r_wave_in_avl']
        cornel_voltage = data['cornel_voltage']
        qtc = data['qtc']
        conclusion = data['conclusion']
        recommendation = data['recommendation']



        try:
            patient_report = Report.objects.get(report_history=report_history)

            patient_report.clinical_information=clinical_information
            patient_report.report=report
            patient_report.rhythm=rhythm
            patient_report.rate=rate
            patient_report.p_wave=p_wave
            patient_report.st_segment=st_segment
            patient_report.pr_interval=pr_interval
            patient_report.qrs_complex=qrs_complex
            patient_report.t_wave=t_wave
            patient_report.axis=axis
            patient_report.r_wave_progression=r_wave_progression
            patient_report.sokolow_lyon_index=sokolow_lyon_index
            patient_report.r_wave_in_avl=r_wave_in_avl
            patient_report.cornel_voltage=cornel_voltage
            patient_report.qtc=qtc
            patient_report.conclusion=conclusion
            patient_report.recommendation=recommendation
            patient_report.finalized=True
            patient_report.save()
            
        except:
                patient_report = Report.objects.create(
                report_history=report_history,
                clinical_information=clinical_information,
                report=report,
                rhythm=rhythm,
                rate=rate,
                p_wave=p_wave,
                st_segment=st_segment,
                pr_interval=pr_interval,
                qrs_complex=qrs_complex,
                t_wave=t_wave,
                axis=axis,
                r_wave_progression=r_wave_progression,
                sokolow_lyon_index=sokolow_lyon_index,
                r_wave_in_avl=r_wave_in_avl,
                cornel_voltage=cornel_voltage,
                qtc=qtc,
                conclusion=conclusion,
                recommendation=recommendation,
                finalized=True
                )

                patient_report.save()


        report_history.status = "Review Completed"
        report_history.completed = True
        report_history.save()

        # Send email to hospital
        subject = 'Appointment Confirmation'
        from_email = settings.EMAIL_HOST_USER  # Change this to your desired sender
        recipient_list = [email]

        # Render email content from template
        message = render_to_string('cardio/report-email.html', {
            'hospital_name': hospital_name,
            'doctor_name': doctor_name,
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
        })

        try:
            send_mail(subject, '', from_email, recipient_list, html_message=message)
        except:
            print("Server error")

        messages.success(request, 'Report saved successfully!')
        return redirect('cardio:reportHistory')

@csrf_exempt
def saveReport(request):
    template_name = "cardio/save-report.html"
    user=request.user


    if request.method == 'POST':
        data = json.loads(request.body)

        report_id = data['report_id']
        report_history = ReportHistory.objects.get(id=report_id)


        clinical_information = data['clinical_information']
        report = data['report']
        rhythm = data['rhythm']
        rate = data['rate']
        p_wave = data['p_wave']
        st_segment = data['st_segment']
        pr_interval = data['pr_interval']
        qrs_complex = data['qrs_complex']
        t_wave = data['t_wave']
        axis = data['axis']
        r_wave_progression = data['r_wave_progression']
        sokolow_lyon_index = data['sokolow_lyon_index']
        r_wave_in_avl = data['r_wave_in_avl']
        cornel_voltage = data['cornel_voltage']
        qtc = data['qtc']
        conclusion = data['conclusion']
        recommendation = data['recommendation']



        try:
            patient_report = Report.objects.get(report_history=report_history)

            patient_report.clinical_information=clinical_information
            patient_report.report=report
            patient_report.rhythm=rhythm
            patient_report.rate=rate
            patient_report.p_wave=p_wave
            patient_report.st_segment=st_segment
            patient_report.pr_interval=pr_interval
            patient_report.qrs_complex=qrs_complex
            patient_report.t_wave=t_wave
            patient_report.axis=axis
            patient_report.r_wave_progression=r_wave_progression
            patient_report.sokolow_lyon_index=sokolow_lyon_index
            patient_report.r_wave_in_avl=r_wave_in_avl
            patient_report.cornel_voltage=cornel_voltage
            patient_report.qtc=qtc
            patient_report.conclusion=conclusion
            patient_report.recommendation=recommendation
            patient_report.save()
            
        except:
                patient_report = Report.objects.create(
                    report_history=report_history,
                    clinical_information=clinical_information,
                    report=report,
                    rhythm=rhythm,
                    rate=rate,
                    p_wave=p_wave,
                    st_segment=st_segment,
                    pr_interval=pr_interval,
                    qrs_complex=qrs_complex,
                    t_wave=t_wave,
                    axis=axis,
                    r_wave_progression=r_wave_progression,
                    sokolow_lyon_index=sokolow_lyon_index,
                    r_wave_in_avl=r_wave_in_avl,
                    cornel_voltage=cornel_voltage,
                    qtc=qtc,
                    conclusion=conclusion,
                    recommendation=recommendation
                )

                patient_report.save()

        messages.success(request, 'Report saved successfully!')
        return redirect('cardio:reportHistory')



@login_required(login_url='login:login')
@csrf_exempt
def resetPassword(request):
    template_name = 'cardio/reset-password.html'
    page = 'Reset Password'
    user=request.user
    cardio = Cardiologist.objects.get(user_id=user.id)
    cardio_name = cardio.user.username.upper()

    if request.method == 'POST':
        password = request.POST.get('password')

        password = make_password(password)
        cardiologist = User.objects.get(id=user.id)

        cardiologist.password = password
        cardiologist.save()

        messages.success(request, 'Password reset successfully!')
        return redirect('cardio:dashboard')

    else:
        return render(request, template_name, {
            'page': page,
            'cardio_name': cardio_name,
        })



@login_required(login_url='login:login')
@csrf_exempt
def viewProfile(request, **kwargs):
    
    template_name = 'cardio/view-profile.html'
    page = 'View Profile'

    user=request.user
    cardio = Cardiologist.objects.get(user_id=user.id)
    cardio_name = cardio.user.username.upper()


    return render(request, template_name, {
        'page': page,
        'cardio_name': cardio_name,
        'cardio': cardio
        })



@login_required(login_url='login:login')
@csrf_exempt
def updateProfile(request, **kwargs):
    
    template_name = 'cardio/update-profile.html'
    page = 'Update Profile'

    user=request.user
    cardiologist = Cardiologist.objects.get(user_id=user.id)
    cardio = User.objects.get(id=cardiologist.user.id)
    cardio_name = cardiologist.user.username.upper()


    if request.method == 'POST':
        
            new_profile = request.FILES.get('profile', None)
            if new_profile is not None:
                cardiologist.profile = request.FILES.get('profile', None)


            new_signature = request.FILES.get('signature', None)
            if new_signature is not None:
                cardiologist.signature = request.FILES.get('signature', None)    


            cardio.first_name = request.POST.get('first_name')
            cardio.last_name = request.POST.get('last_name')
            cardio.username = f"{request.POST.get('first_name')} {request.POST.get('last_name')}"
            cardio.email = request.POST.get('email')
            cardio.save()
            
            

            cardiologist.contact = request.POST.get('contact')
            cardiologist.gender = request.POST.get('gender')
            cardiologist.country = request.POST.get('country') if request.POST.get('country') else cardiologist.country
            cardiologist.town = request.POST.get('town')
            cardiologist.address = request.POST.get('address')
            cardiologist.save() 
            


            messages.success(request, 'Cardiologist details updated successfully!')
            return redirect('cardio:viewProfile') 

    else:
        return render(request, template_name, {
            'page': page,
            'cardio_name': cardio_name,
            'cardiologist': cardiologist
            })



@csrf_exempt
def downloadReport(request, *args, **kwargs):
    user = request.user
    pk = kwargs.get('pk')
    year = datetime.datetime.now().year

    report_history = ReportHistory.objects.get(id=pk)
    report = Report.objects.get(report_history_id=pk)
 

    template_path = 'cardio/user_printer.html'
    context = {
        'report_history': report_history,
        'report': report,
        'year': year
         }


    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')


    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response )

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def user_logout(request):
    logout(request)
    return redirect('login:login') 