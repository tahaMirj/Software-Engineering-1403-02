from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Teacher, TimeSlot
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
            return redirect('group3:teacher_landing')
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
        return redirect('group3:teacher_landing')

    return render(request, 'teacher_signup.html')


@login_required
def teacher_profile(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('group3:teacher_signup')  # fallback if no teacher profile found

    context = {'teacher': teacher}
    return render(request, 'teacher_profile.html', context)


def teacher_logout(request):
    logout(request)
    return redirect('group3:group3')


def teacher_landing(request):
    # If the user isn’t logged in, just render the portal template
    # (the template itself handles the login/signup links).
    if not request.user.is_authenticated:
        return render(request, 'teacher_landing.html')

    # Otherwise, look up their teacher profile and timeslots.
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        # If somehow they have an account but no Teacher profile,
        # you could redirect or just render with no timeslots.
        return render(request, 'teacher_landing.html', {
            'timeslots': []
        })

    timeslots = TimeSlot.objects.filter(teacher=teacher)
    return render(request, 'teacher_landing.html', {
        'timeslots': timeslots
    })


@login_required
def create_timeslot(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time   = request.POST.get('end_time')
        dow        = request.POST.get('day_of_week')

        # Echo back values on error
        context = {
            'start_time': start_time,
            'end_time': end_time,
            'day_of_week': dow,
        }

        # Basic presence check
        if not (start_time and end_time and dow):
            context['error'] = 'All fields are required.'
            return render(request, 'create_timeslot.html', context)

        # Parse datetimes
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
        except ValueError:
            context['error'] = 'Invalid date/time format.'
            return render(request, 'create_timeslot.html', context)

        # 1) End must be after start
        if end_dt <= start_dt:
            context['error'] = 'End time must be after start time.'
            return render(request, 'create_timeslot.html', context)

        # 2) Same calendar year
        if start_dt.year != end_dt.year:
            context['error'] = 'Start and end time must be in the same year.'
            return render(request, 'create_timeslot.html', context)

        # 3) Overlap check
        overlapping = TimeSlot.objects.filter(
            teacher=teacher,
            start_time__lt=end_dt,
            end_time__gt=start_dt
        ).exists()
        if overlapping:
            context['error'] = 'This timeslot overlaps with an existing one.'
            return render(request, 'create_timeslot.html', context)

        # Passed all checks — create it
        TimeSlot.objects.create(
            teacher=teacher,
            start_time=start_dt,
            end_time=end_dt,
            day_of_week=int(dow)
        )
        return redirect('group3:teacher_landing')

    # GET
    return render(request, 'create_timeslot.html')


@login_required
def edit_timeslot(request, slot_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    timeslot = get_object_or_404(TimeSlot, id=slot_id, teacher=teacher)

    if timeslot.is_booked:
        return render(request, 'edit_timeslot.html', {
            'error': 'This timeslot is already booked and cannot be edited.',
            'timeslot': timeslot,
        })

    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        day_of_week = request.POST.get('day_of_week')

        # Parse datetimes
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
        except (TypeError, ValueError):
            return render(request, 'edit_timeslot.html', {
                'error': 'Invalid date/time format.',
                'timeslot': timeslot,
            })

        # 1) End must be after start
        if end_dt <= start_dt:
            return render(request, 'edit_timeslot.html', {
                'error': 'End time must be after start time.',
                'timeslot': timeslot,
            })

        # 2) Must be in same calendar year
        if start_dt.year != end_dt.year:
            return render(request, 'edit_timeslot.html', {
                'error': 'Start and end time must be in the same year.',
                'timeslot': timeslot,
            })

        # 3) Overlap check (exclude this slot)
        overlapping = TimeSlot.objects.filter(
            teacher=teacher,
            start_time__lt=end_dt,
            end_time__gt=start_dt
        ).exclude(id=timeslot.id).exists()

        if overlapping:
            return render(request, 'edit_timeslot.html', {
                'error': 'This updated timeslot overlaps with another one.',
                'timeslot': timeslot,
            })

        # Passed all checks — save
        timeslot.start_time = start_dt
        timeslot.end_time = end_dt
        timeslot.day_of_week = int(day_of_week)
        timeslot.save()

        return redirect('group3:teacher_landing')

    return render(request, 'edit_timeslot.html', {'timeslot': timeslot})


