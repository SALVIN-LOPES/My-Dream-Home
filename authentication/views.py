from django.shortcuts import redirect, render
# from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .forms import CustomerUserForm
from django.contrib import messages
from .models import Customer
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# from authentication.decorators import unauthenticated_user



# Create your views here.
@login_required(login_url='login')

def home(request):

    context = {}
    return render(request,'authentication/home.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username = username,password = password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is Incorrect')


        context = {}
        return render(request,'authentication/login.html',context)

# @unauthenticated_user

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form  = CustomerUserForm()
        if request.method == 'POST':
            print('FORM IS SUBMITTED')

            try:
                user = User.objects.get(email = request.POST.get('email'))
            except User.DoesNotExist:
            # Unable to find a user, this is fine
                form  = CustomerUserForm(request.POST)
                if form.is_valid():
                    print('FORM IS VALID')
                    form.save()
                    print('FORM IS SAVED')
                    print(form)

                    customer = Customer.objects.create(
                        user = User.objects.get(email = request.POST.get('email')),
                        name = request.POST.get('username'),
                        phone = request.POST.get('phone'),
                        email = request.POST.get('email')
                    )
                    # user = form.cleaned_data.get('username')

                    return redirect('login')

                context = {'form':form}
                return render(request,'authentication/register.html',context)
            return render(request,'authentication/register.html',{'form':form})
        return render(request,'authentication/register.html',{'form':form})

                
            
        
@login_required(login_url='login')

def logoutUser(request):
    logout(request)
    return redirect('login')
