from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('login/',views.loginPage,name = 'login'),
    path('logout/',views.logoutUser,name = 'logout'),

    path('register/',views.register,name = 'register'),
]