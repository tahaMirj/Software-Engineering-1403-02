from django.shortcuts import render, redirect
from django.urls import reverse # Import reverse to get URL by name

def home(request):
    return render(request, 'group6.html', {'group_number': '6'})

# redirect to the registration signup page
def group6_signup(request):
    return redirect(reverse('signup'))

# redirect to the registration login page
def group6_login(request):
    return redirect(reverse('login'))

# redirect to the registration logout page
def group6_logout(request):
    return redirect(reverse('logout'))