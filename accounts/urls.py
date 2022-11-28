from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),
    path('reset_password/<uidb64>/<token>/',
         views.reset_password, name='reset_password'),
    path('password_reset/', views.password_reset, name='password_reset')
]
