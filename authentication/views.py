from django.shortcuts import render

# Create your views here.
def index(request):

    context = {}
    return render(request,'authentication/index.html',context)

def login(request):

    context = {}
    return render(request,'authentication/login.html',context)

def register(request):

    context = {}
    return render(request,'authentication/register.html',context)
