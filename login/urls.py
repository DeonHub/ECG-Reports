from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('account-registration/', views.register, name="register"),

    path('forgot-password/', views.forgotPassword, name="forgotPassword"),
    path('verify-code/', views.verifyCode, name="verifyCode"),

    path('reset-password/<str:token>', views.resetPassword, name='resetPassword'),

    # path('index/', views.index, name="index"),
]