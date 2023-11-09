from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( 
User,
Cardiologist,
Hospital,
Credit,
PurchaseHistory,
ReportHistory,
Verifications
    )

class AppAdmin(admin.ModelAdmin):
    pass