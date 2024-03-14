from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True ,on_delete=models.CASCADE)
    name=models.CharField(max_length=70 , null=True,blank=True)
    balance = models.IntegerField(null=True,blank=True)
    phone = models.CharField(max_length = 200,null=True,blank=True)
    email = models.CharField(max_length = 200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.name 


class House(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL , null=True)
    email = models.CharField(max_length=300,blank=True,null=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    property_type = models.CharField(max_length=200 ,blank=True, null=True )
    price=models.IntegerField(null=True , blank=True)
    view=models.CharField(max_length=200, null=True ,blank=True)
    floor=models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(max_length=2000 ,null=True,blank=True)
    city=models.CharField(max_length=200,null=True,blank=True)
    state=models.CharField(max_length=200,null=True,blank=True)
    purpose = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.customer.name

class Image(models.Model):
    house = models.ForeignKey(House,default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="house_images")

    def __str__(self):
        return self.house.address