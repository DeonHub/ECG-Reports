from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model



# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_cardio = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username



class Cardiologist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to = 'profile-uploads/', default = 'superuser/static/superuser/media/profile.png', blank=True)
    contact = models.CharField(max_length=255, default='1234567890', null=True)
    gender = models.IntegerField(null=True)
    country = models.CharField(max_length=255, default='Ghana', null=True)
    town = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    
    signature = models.ImageField(upload_to = 'signature-uploads/', default = '', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'





class Hospital(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=255, null=True)
    available_slots = models.IntegerField(default=0)
    logo = models.ImageField(upload_to = 'logo-uploads/', default = 'superuser\static\superuser\media\ekg.png', blank=True)
    contact = models.CharField(max_length=255, default='1234567890', null=True)
    country = models.CharField(max_length=255, default='Ghana', null=True)
    town = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.hospital_name



class Credit(models.Model):
    total_amount = models.FloatField(default=0.00)
    total_slots = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.total_slots} slots'



class PurchaseHistory(models.Model):
    reference = models.CharField(max_length=100, null=True, default="")
    invoice_no = models.CharField(max_length=100, null=True, default="")
    hospital = models.ForeignKey(Hospital, on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0.00)
    slots_bought = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.hospital.hospital_name} bought {self.slots_bought} credits'





class ReportHistory(models.Model):
    cardiologist = models.ForeignKey(Cardiologist, related_name='cardiologist', null=True, on_delete=models.DO_NOTHING)
    hospital = models.ForeignKey(Hospital, related_name='hospital', null=True, on_delete=models.DO_NOTHING)

    patient_name = models.CharField(max_length=100, default='Samuel Inkoom')
    patient_type = models.CharField(max_length=100, default='None')
    patient_age = models.IntegerField(default=25, null=True)
    patient_number = models.CharField(max_length=255, default='1234567890', null=True)

    image = models.ImageField(upload_to='cardio-uploads/', default = '', null=True)
    report = models.FileField(upload_to='report-uploads/', null=True)
    report_number = models.CharField(max_length=100, default='ABC12345')
    status = models.CharField(max_length=100, null=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.hospital} - {self.report_number}'



class Report(models.Model):
    report_history = models.ForeignKey(ReportHistory, related_name='report_history', null=True, on_delete=models.CASCADE)
    study = models.CharField(max_length=255, null=True)
    clinical_information = models.CharField(max_length=255, null=True)
    report = models.CharField(max_length=255, null=True)
    rhythm = models.CharField(max_length=255, null=True)
    rate = models.CharField(max_length=255, null=True)
    p_wave = models.CharField(max_length=255, null=True)
    st_segment = models.CharField(max_length=255, null=True)
    pr_interval = models.CharField(max_length=255, null=True)
    qrs_complex = models.CharField(max_length=255, null=True)
    t_wave = models.CharField(max_length=255, null=True)
    axis = models.CharField(max_length=255, null=True)
    r_wave_progression = models.CharField(max_length=255, null=True)
    sokolow_lyon_index = models.CharField(max_length=255, null=True)
    r_wave_in_avl = models.CharField(max_length=255, null=True)
    cornel_voltage = models.CharField(max_length=255, null=True)
    qtc = models.CharField(max_length=255, null=True)
    conclusion = models.CharField(max_length=255, null=True)
    recommendation = models.CharField(max_length=255, null=True)
    finalized = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.report_history.hospital.hospital_name} report'



class Verifications(models.Model):
    email = models.EmailField(max_length=254)
    token = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    

    def __str__(self):
        return self.email
