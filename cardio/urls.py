from django.urls import path
from . import views

app_name = 'cardio'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('report-history/', views.reportHistory, name="reportHistory"),
    path('finalize-report/', views.finalizeReport, name="finalizeReport"),
    path('save-report/', views.saveReport, name="saveReport"),
    

    path('view-report-details/<int:pk>', views.viewReportDetails, name="viewReportDetails"),
    path('review-image/<int:pk>', views.reviewImage, name="reviewImage"),

    path('view-profile/', views.viewProfile, name="viewProfile"),
    path('update-profile/', views.updateProfile, name="updateProfile"),

    path('logout/', views.user_logout, name='user_logout'),
    path('reset-password/', views.resetPassword, name="resetPassword"),
    path('ajax/load-link/', views.load_review, name='ajax_load_review'),

    path('download-report/<int:pk>', views.downloadReport, name="downloadReport"),

    # path('', views.login, name="login"),
    # path('login/', views.logins, name="logins"),
    # path('index/', views.index, name="index"),
]