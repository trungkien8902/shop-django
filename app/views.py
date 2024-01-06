from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_notlogin = "hidden" 
        user_login = "show"
    else:
        items=[]
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_notlogin = "show" 
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', "")
    products = Product.objects.all()
    context = {'active_category':active_category, 'categoryes':categories, 'products': products, 'cartItems': cartItems, "user_login": user_login,"user_notlogin":user_notlogin }
    return render(request, 'app/index.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'user or password not correct!')

    context = {}
    return render(request, 'app/login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')

# def register(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     context = {'form': form}
#     return render(request, 'app/register.html', context)

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=make_password(form.cleaned_data['password1'])
            data=User(username=username,email=email,password=password)
            data.save()            
            messages.success(request, "Registered Successfully")
            return redirect('/login')
    else: #Here GET condition
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'app/register.html', context)
