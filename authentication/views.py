from django.forms import formsets
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render
# from .models import *
from .models import House, Image
from django.http import HttpResponse, request
from django.contrib.auth.models import User,auth
from .forms import CustomerUserForm, HouseForm, ImageForm
from django.contrib import messages
from .models import Customer
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
import random
# from authentication.decorators import unauthenticated_user

# get current balance
def get_cur_balance(request):
    cur_user  = request.user
    customer = Customer.objects.filter(email = cur_user.email).first()
    return customer.balance
    # return 1200

sale_houses = list(House.objects.all())
# Create your views here.
@login_required(login_url='login')
def home(request):
    cur_balance = get_cur_balance(request)
    print("user email = ",request.user.email)
    # print(request.user.email)
    saleHouse = random.sample(sale_houses,3)
    sale={}
    for i in saleHouse:
        image = Image.objects.filter(house_id = i.id).first()
        sale[image] = i
    context={'sale':sale,'cur_balance':cur_balance}
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
                if(user):
                    form  = CustomerUserForm(request.POST)
                    context={'message':"User with that Email already Exist...!",'form':form}
                    return render(request,'authentication/register.html',context)
            except User.DoesNotExist:
            # Unable to find a user, this is fine
                form  = CustomerUserForm(request.POST)
                if form.is_valid():
                    form.save()

                    customer = Customer.objects.create(
                        user = User.objects.get(email = request.POST.get('email')),
                        name = request.POST.get('username'),
                        phone = request.POST.get('phone'),
                        email = request.POST.get('email'),
                        balance = 100000000,
                    )
                    # user = form.cleaned_data.get('username')

                    return redirect('login')

                context = {'form':form}
                return render(request,'authentication/register.html',context)
            return render(request,'authentication/register.html',{'form':form})
        return render(request,'authentication/register.html',{'form':form})

@login_required(login_url='login')
def filterPage(request):
    cur_balance = get_cur_balance(request)
    loc = request.POST.get('location').lower()
    priceRange = int(request.POST.get('rangeInput'))
    p_type = request.POST.get('property_type')
    view_cat = request.POST.get('view_categories')
    cty = request.POST.get('city').lower()
    states = request.POST.get('state').lower()

    form_detail={'loc':loc,'p_type':p_type,'view_cat':view_cat,'cty':cty,'states':states,'priceRange':priceRange}
    cur_user = request.user
    houses_obj = House()
    price = priceRange*100000
    minRange = 0
    maxRange = 0
    if((price) > 10000000):
        minRange = price - 10000000
        maxRange = price + 10000000
    else:
        minRange = price - (price//2)
        maxRange = price + (price//2) 
    print(price)
    print(minRange)
    print(maxRange)
    if(len(loc)==0):
        if(len(cty)==0):
            if(len(states) == 0):
                if(p_type == "All"):
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter(~Q(email=cur_user.email) , purpose="Sell", price__gte = minRange , price__lte = maxRange )
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  view = view_cat)
                else:
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  property_type = p_type)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  property_type = p_type , view = view_cat)
            else:
                if(p_type == "All"):
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  state = states)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  state = states,view = view_cat)
                else:
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  state = states,property_type = p_type)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  state = states,property_type = p_type , view = view_cat)
        else:
            if(len(states) == 0):
                if(p_type == "All"):
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  city = cty)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  city = cty,view = view_cat)
                else:
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  city = cty,property_type = p_type)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  city = cty,property_type = p_type , view = view_cat)
            else:
                if(p_type == "All"):
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  city = cty,state = states)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  city = cty,view = view_cat , state = states)
                else:
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  city = cty,property_type = p_type , state = states)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  city = cty,property_type = p_type , view = view_cat , state = states)
    else:
        if(len(cty)==0):
            if(len(states) == 0):
                if(p_type == "All"):
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , view = view_cat)
                else:
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , property_type = p_type)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , property_type = p_type , view = view_cat)
            else:
                if(p_type == "All"):
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , state = states)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , state = states,view = view_cat)
                else:
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , state = states,property_type = p_type)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , state = states,property_type = p_type , view = view_cat)
        else:
            if(len(states) == 0):
                if(p_type == "All"):
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , city = cty)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange ,purpose="Sell",  location = loc , city = cty,view = view_cat)
                else:
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange , purpose="Sell" , location = loc , city = cty,property_type = p_type)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange , purpose="Sell" , location = loc , city = cty,property_type = p_type , view = view_cat)
            else:
                if(p_type == "All"):
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange , purpose="Sell" , location = loc , city = cty, state = states)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange , purpose="Sell" , location = loc , city = cty,view = view_cat , state = states)
                else:
                    if(view_cat == "Any"):
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange , purpose="Sell" , location = loc , city = cty,property_type = p_type , state = states)
                    else:
                        houses_obj = House.objects.filter( ~Q(email=cur_user.email) , price__gte = minRange , price__lte = maxRange , purpose="Sell" , location = loc , city = cty,property_type = p_type , view = view_cat , state = states)
    
    
    img_house={}
    for hou in houses_obj:
        photo = Image.objects.filter(house_id = hou.id).first()
        img_house[photo]= hou
    context={ 'message':"There is no house for Sell at present...!",'img_house':img_house , 'form_detail':form_detail,'cur_balance':cur_balance , 'houses_obj':houses_obj}
    return render(request,'authentication/filter.html',context)

@login_required(login_url='login')
def sellPage(request):
    cur_balance = get_cur_balance(request)
    print(cur_balance)
    if(request.method=="POST"):
        locations = request.POST.get('location')
        p_type = request.POST.get('property_type')
        prices = request.POST.get('price')
        view_cat = request.POST.get('view_categories')
        floors = request.POST.get('floor')
        addr = request.POST.get('address')
        cty = request.POST.get('city')
        states = request.POST.get('state')
        images = request.FILES.getlist('images')
        cur_user = request.user
        customer_obj = Customer.objects.get(email = cur_user.email)
        house_obj = House.objects.create(
            customer = customer_obj,
            email = customer_obj.email,
            location = locations.lower(),
            property_type = p_type,
            price = prices,
            view = view_cat,
            floor = floors,
            address=addr,
            
            city=cty.lower(),
            state=states.lower(),
            purpose = "Sell",
        )
        house_obj.save()
        for i in images:
            
            imageModel = Image.objects.create(
                house = house_obj,
                image = i,
            )
            imageModel.save()
        return redirect('profile')
    context = {'cur_balance':cur_balance}
    return render(request,"authentication/sell.html",context)

@login_required(login_url='login')
def buyPage(request):
    cur_balance = get_cur_balance(request)
    
    cur_user = request.user
    houses = House.objects.filter(~Q(email=cur_user.email), purpose="Sell")
    img_house={}
    for hou in houses:
        photo = Image.objects.filter(house_id = hou.id).first()
        img_house[photo]= hou
    context={'img_house':img_house,'cur_balance':cur_balance}
    return render(request,"authentication/buy.html",context)

@login_required(login_url='login')
def profilePage(request):
    cur_balance = get_cur_balance(request)
    
    cur_user = request.user
    houses = House.objects.filter(email=cur_user.email)
    img_house={}
    for hou in houses:
        photo = Image.objects.filter(house_id = hou.id).first()
        img_house[photo]= hou
    context={'img_house':img_house,'cur_balance':cur_balance,'message':"You don't have any house yet...! "}
    return render(request,"authentication/profile.html",context)

@login_required(login_url='login')
def individualHouse(request,pk):
    cur_balance = get_cur_balance(request)
    house = House.objects.get(id = pk)
    single_photo = Image.objects.filter(house_id = pk).first()
    photo = Image.objects.filter(house_id = pk).exclude(id=single_photo.id)
    context={'house_detail':house , 'photo':photo,'single_photo':single_photo,'cur_balance':cur_balance}
    return render(request,"authentication/house.html",context)

@login_required(login_url='login')
def editHousePage(request,pk):
    cur_balance = get_cur_balance(request)
    house = House.objects.get(id = pk)
    single_photo = Image.objects.filter(house_id = pk).first()
    photo = Image.objects.filter(house_id = pk).exclude(id=single_photo.id)
    context={'house_detail':house , 'photo':photo,'single_photo':single_photo,'cur_balance':cur_balance}
    
    if request.method == "POST":
        locations = request.POST.get('location')
        p_type = request.POST.get('property_type')
        prices = request.POST.get('price')
        view_cat = request.POST.get('view_categories')
        floors = request.POST.get('floor')
        addr = request.POST.get('address')
        cty = request.POST.get('city')
        states = request.POST.get('state')
        # pur = request.POST.get('purpose')
        images = request.FILES.getlist('images')
        
        cur_user = request.user
       

        customer_obj = Customer.objects.get(email = cur_user.email)
        
        house_obj = House.objects.filter(id=pk).update(
            customer = customer_obj,
            email = customer_obj.email,
            location = locations.lower(),
            property_type = p_type,
            price = prices,
            view = view_cat,
            floor = floors,
            address=addr,
            
            city=cty.lower(),
            state=states.lower(),
            purpose = "Withdraw",
        )
        
        HOUSE_OBJ = House.objects.get(id=pk)

        if(len(images)>0):
            Image.objects.filter(house_id = pk).delete()
            for i in images:
                imageModel = Image.objects.create(
                    house = HOUSE_OBJ,
                    image = i,
                )
                imageModel.save()
        
        return redirect('profile')
    return render(request,"authentication/edit_house.html",context)

@login_required(login_url='login')
def deleteHousePage(request , pk):
    House.objects.filter(id=pk).delete()
    return redirect("profile")

@login_required(login_url='login')
def changeSellingPage(request,pk):
    House.objects.filter(id=pk).update(purpose = "Sell")
    return redirect('profile')

@login_required(login_url='login')
def changeWithdrawingPage(request,pk):
    House.objects.filter(id=pk).update(purpose = "WithDraw")
    return redirect('profile')

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
@login_required(login_url='login')
def changeCustomerPage(request,pk):
    cur_balance = get_cur_balance(request)
    house_obj = House.objects.get(id=pk)
    
    if(cur_balance >= house_obj.price ):
        cur_user = request.user
        customer_obj = Customer.objects.get(email=cur_user.email)
        newBalance = cur_balance - house_obj.price
        customer_obj.balance = newBalance
        customer_obj.save()
        oldCustomer = Customer.objects.get(email = house_obj.email)
        oldCustomer.balance += house_obj.price
        oldCustomer.save()
        house_obj.customer = customer_obj
        house_obj.email = cur_user.email
        house_obj.save()
        return redirect('buy')
    else:
        messages.error(request, "You don't have enough money...!")
        return redirect('buy')

@login_required(login_url='login')
def showourstory(request):

    context = {}
    return render(request,"authentication/story.html",context)

@login_required(login_url='login')
def terms_and_conditions(request):

    context = {}
    return render(request,"authentication/terms-and-conditions.html.",context)

@login_required(login_url='login')
def privacy_policy(request):

    context = {}
    return render(request,'authentication/privacypolicy.html',context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
