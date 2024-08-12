from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Inventory 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class AddInventory(ModelForm):   
    class Meta:
        model=Inventory
        fields = ['name', 'cost_per_item','quantity_in_stock','quantity_sold']  

class UpdateInventoryForm(ModelForm):
    class Meta:
        model= Inventory
        fields= ('name', 'cost_per_item','quantity_in_stock', 'quantity_sold')
        
