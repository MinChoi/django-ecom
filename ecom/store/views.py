from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pprint import pprint


def home(request):
    products = Product.objects.all()

    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # print('test:')
        # print(request.POST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('Login done!'))
            return redirect('home')
        else:
            messages.warning(request, ('Login fail!'))

    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('Logout done!'))
    return redirect('home')