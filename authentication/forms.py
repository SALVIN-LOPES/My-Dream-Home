from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db.models.fields import files
from django.forms import fields, widgets
from django.forms.models import ModelForm

from authentication.models import House, Image

class CustomerUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class HouseForm(ModelForm):
    class Meta:
        model=House
        fields='__all__'
        widgets={
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'property_type':forms.Select(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            'view':forms.Select(attrs={'class':'form-control'}),
            'floor':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.TextInput(attrs={'class':'form-control'}),
            'purpose':forms.Select(attrs={'class':'form-control'}),
        }

class ImageForm(ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))

    # class Meta(NoteForm.Meta):
    #     fields = NoteForm.Meta.fields + ['images',]

        