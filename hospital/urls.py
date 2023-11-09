from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('ajax/load-link/', views.load_link, name='ajax_load_link'),

    path('slot-subscription/', views.purchaseSlot, name="purchaseSlot"),
    path('upload-image/', views.uploadImage, name="uploadImage"),

    path('purchase-history/', views.purchaseHistory, name="purchaseHistory"),
    path('report-history/', views.reportHistory, name="reportHistory"),
    path('view-report-details/<int:pk>', views.viewReportDetails, name="viewReportDetails"),
    

    path('view-profile/', views.viewProfile, name="viewProfile"),
    path('update-profile/', views.updateProfile, name="updateProfile"),
    path('reset-password/', views.resetPassword, name="resetPassword"),
    
    path('logout/', views.user_logout, name='user_logout'),
]