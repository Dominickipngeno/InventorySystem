from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, AddInventory, UpdateInventoryForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

import json
import plotly.express as px  # Correct import
import plotly.utils
from django_pandas.io import read_frame

from django.contrib.auth.forms import AuthenticationForm
from .models import Inventory

# Create your views here.
def index(request):
    inventories= Inventory.objects.all()
    context= {
        'title':"Index Page|| Inventories",
         'inventories': inventories
    }
    return render(request, 'ims/index.html', context=context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as {username}')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')
@login_required
def per_product(request,pk):
    inventory=get_object_or_404(Inventory,pk=pk)
    context = {
        'inventory': inventory
    }

    return render(request, "ims/per_product.html", context=context)


def add_products(request):
    if request.method =="POST":
        form =AddInventory(request.POST)

        if form.is_valid():
            new_inventory= form.save(commit=False)
            new_inventory.sales=float(form.data['cost_per_item'])* float(form.data['quantity_sold'])

            new_inventory.save()
            messages.success(request, "Successfully added products")
            return redirect("index")
        
    else:
            form = AddInventory()
    return render (request, "ims/inventory_add_product.html",{"form": form})
        
def delete_inventory(request,pk):

    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.success(request, "Successfully Deletd")
    return redirect ("index")  


def inventory_update (request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method=="POST":
        updateform= UpdateInventoryForm(data=request.POST)
        if updateform.is_valid():
            inventory.name=updateform.data['name']
            inventory.quantity_in_stock=updateform.data['quantity_in_stock']
            inventory.quantity_sold= updateform.data['quantity_sold']
            inventory.cost_per_item= updateform.data['cost_per_item']
            inventory.sales= float(inventory.cost_per_item) * float(inventory.quantity_sold)

            inventory.save()
            messages.info(request, "Product Successfully Updated")
            return redirect("index")
    else:
        updateform= UpdateInventoryForm(instance=inventory)
        context= {
            "form": updateform
        }
        return render(request, "ims/inventory_update.html", context=context)
    
def dashbaord(request):
    inventories= Inventory.objects.all()
    df= read_frame(inventories)

    # Group by 'last_sales_date' and aggregate sales (sum, in this case)
    sales_graph = df.groupby(by="name", as_index=False).agg({'sales': 'sum'})

    # Create a line plot using Plotly Express
    sales_graph = px.line(sales_graph, x="name", y="sales", title="Sales Trend")

    # Convert the Plotly graph to JSON
    sales_graph_json = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)


    best_performing_product_df= df.groupby(by= "name").sum().sort_values(by="quantity_sold")
    best_performing_product=px.bar(best_performing_product_df,
                                   x= best_performing_product_df.index,
                                   y=best_performing_product_df.quantity_sold,
                                   title= "Best perforrming products") 
    best_performing_product=json.dumps(best_performing_product, cls=plotly.utils.PlotlyJSONEncoder)
    

    most_product_df= df.groupby(by= "name").sum().sort_values(by="quantity_in_stock")
    most_product=px.pie(most_product_df,
                                   names= most_product_df.index,
                                   values=most_product_df.quantity_in_stock,
                                   title= "Most products in Stock ") 
    most_product=json.dumps(most_product, cls=plotly.utils.PlotlyJSONEncoder)
    # Pass the graph JSON to the template context
    context = {
        "sales_graph": sales_graph_json,
        "best_performing_product": best_performing_product,
        "most_product": most_product
    }

    return render(request, "ims/dashboard.html", context=context)