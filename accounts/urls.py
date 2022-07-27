from django.urls import path,include
from django.contrib import admin
from .import views

urlpatterns = [
    path('',views.home , name='home'),
    path('login/',views.loginViews , name='login'),
    path('register/',views.regitserView , name='register'),
    path('token/',views.token_send , name='token_send'),
    path('success/',views.success , name='success'),

    path('verify/<auth_token>',views.verify,name='verify'),
    path('error',views.error_page,name='error')
]
