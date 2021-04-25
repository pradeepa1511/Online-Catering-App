from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']
        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_customer = true
            if commit:
                user.save()
            return user

class CateringSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']
        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_catering = true
            if commit:
                user.save()
            return user

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CateringForm(forms.ModelForm):
    class Meta:
        model = Catering
        fields = '__all__'                    

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['item_name','price']


