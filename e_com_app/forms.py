from django import forms
from e_com_app.models import ShippingAddress
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from e_com_app.models import User



class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username','email','password1','password2']


class ShippingAddressForm(forms.ModelForm):
    address_line_1=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    address_line_2=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    city=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    state=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    postal_code=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    country=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = ShippingAddress
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code','phone_number', 'country']
    

