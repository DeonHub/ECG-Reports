from django.urls import path
from . import views

app_name = 'superuser'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    # Cardios
    path('add-cardiologists/', views.createCardio, name="createCardio"),
    path('view-cardiologists/', views.viewCardios, name="viewCardios"),
    path('view-cardiologist-details/<int:pk>', views.viewCardioDetails, name="viewCardioDetails"),
    path('edit-cardiologist-details/<int:id>/', views.editCardioDetails, name='editCardioDetails'),
    path('delete-cardiologist/<int:id>', views.deleteCardio, name='deleteCardio'),

     # Hospitals
    path('view-hospitals/', views.viewHospitals, name="viewHospitals"),
    path('view-hospital-details/<int:pk>', views.viewHospitalDetails, name="viewHospitalDetails"),
    path('delete-hospital/<int:id>', views.deleteHospital, name='deleteHospital'),

    path('purchase-history/', views.purchaseHistory, name="purchaseHistory"),
    path('view-purchase-details/<int:pk>', views.viewPurchaseDetails, name="viewPurchaseDetails"),

    path('report-history/', views.reportHistory, name="reportHistory"),
    path('view-report-details/<int:pk>', views.viewReportDetails, name="viewReportDetails"),
    path('reset-password/', views.resetPassword, name="resetPassword"),

    path('logout/', views.user_logout, name='user_logout'),

]