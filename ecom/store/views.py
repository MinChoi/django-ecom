from pydoc import describe

from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q

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
            messages.success(request, ('Registered done! Let\'s update info!'))
            return redirect('update_info')
        else:
            messages.warning(request, ('Register fail!'))
    return render(request, 'register.html', {'form':form})


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

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, ('User info updated!'))
            return redirect('home')
        return render(request, 'update_info.html', {'form':form})
    else:
        messages.warning(request, ('Login first!'))
        return redirect('home')


def search(request):
    if request.method == "POST":
        search_text = request.POST.get('search')

        search_products = Product.objects.filter(
            Q(name__icontains=search_text)
            | Q(description__icontains=search_text)
        )

        if not search_products:
            messages.warning(request, "No products are found")

        return render(request, 'search.html', {'search_products':search_products})
    return render(request, 'search.html', {})