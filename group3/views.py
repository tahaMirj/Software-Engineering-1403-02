from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Teacher
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return  render (request , 'group3.html' , {'group_number': '3'})


def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                user.teacher  # Check for linked Teacher
            except Teacher.DoesNotExist:
                return render(request, 'teacher_login.html', {'error': 'Account not registered as a teacher.'})

            login(request, user)
            return redirect('group3:teacher_profile')
        else:
            return render(request, 'teacher_login.html', {'error': 'Invalid username or password'})

    return render(request, 'teacher_login.html')


def teacher_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        language = request.POST.get('language')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'teacher_signup.html', {
                'error': 'Username already exists.'
            })

        # Check if teacher with same email already exists
        if Teacher.objects.filter(email=email).exists():
            return render(request, 'teacher_signup.html', {
                'error': 'A teacher with this email already exists.'
            })

        # If all good, create user and teacher
        user = User.objects.create_user(username=username, password=password)
        teacher = Teacher.objects.create(user=user, name=name, email=email, language=language)

        login(request, user)
        return redirect('group3:teacher_profile')

    return render(request, 'teacher_signup.html')


@login_required
def teacher_profile(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('group3:teacher_signup')  # fallback if no teacher profile found

    context = {'teacher': teacher}
    return render(request, 'teacher_profile.html', context)




