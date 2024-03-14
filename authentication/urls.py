from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('',views.home,name = 'home'),
    path('login/',views.loginPage,name = 'login'),
    path('logout/',views.logoutUser,name = 'logout'),
    path('register/',views.register,name = 'register'),
    path('buy/',views.buyPage,name="buy"),
    path('sell/',views.sellPage,name="sell"),
    path('individual-house/<int:pk>/',views.individualHouse,name="individual_house"),
    path('filter/',views.filterPage,name="filter"),
    path('profile/',views.profilePage, name="profile"),
    path('edit-house/<int:pk>/',views.editHousePage,name="edit_house"),
    path('change-selling/<int:pk>',views.changeSellingPage,name="change_selling"),
    path('change-withdrawing/<int:pk>',views.changeWithdrawingPage,name="change_withdrawing"),
    path('change-customer/<int:pk>',views.changeCustomerPage,name="change_customer"),
    path('our-story/',views.showourstory,name = "our_story"),
    path('terms-and-conditions/',views.terms_and_conditions,name = "terms_and_conditions"),
    path('privacy-policy/',views.privacy_policy,name = "privacy_policy"),
    path('delete-house/<int:pk>',views.deleteHousePage,name="delete_house"),

]

