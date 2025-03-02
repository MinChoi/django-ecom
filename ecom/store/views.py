from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms

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

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registered done!'))
            return redirect('home')
        else:
            messages.warning(request, ('Register fail!'))
    return render(request, 'register.html')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request, category_name):
    category_name = category_name.replace('-', ' ')

    try:
        category_selected = Category.objects.get(name=category_name)
        products = Product.objects.filter(category= category_selected)
        return render(request, 'category.html', {'products':products, 'category': category_selected})
    except:
        messages.warning(request, ('Category doesn\'t exist!'))
        return redirect('home')

    # ??
    products = Product.objects.get(id=pk)
    return render(request, 'category.html', {'product':products, 'category':category})

def category_summary(request):
    categories = Category.objects.all()

    return render(request, 'category_summary.html', {'categories':categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ('Profile updated!'))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.warning(request, ('Login first!'))
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                login(request, current_user)
                messages.success(request, ('Password updated!'))
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = ChangePasswordForm(current_user)
        return render(request, 'update_password.html', {'form':form})
    else:
        messages.warning(request, ('Login first!'))
        return redirect('home')

