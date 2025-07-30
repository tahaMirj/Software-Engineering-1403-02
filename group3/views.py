import os
from datetime import datetime

from django import forms
from django.contrib import messages
from django.db import transaction
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Teacher, TimeSlot, Session, Review
from django.contrib.auth.decorators import login_required

# Create your views here.

#this function returns us to home
def home(request):
    return  render (request , 'group3.html' , {'group_number': '3'})


#a teacher can also be a student because the entity teacher is made based on a user that already exists in the website
#used for logging in a teacher
def teacher_login(request):
    if request.method == 'POST':
        #get the usernames and the password to check them
        username = request.POST.get('username')
        password = request.POST.get('password')
        #check the user name and the password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                user.teacher  # Check for linked Teacher
            except Teacher.DoesNotExist:
                return render(request, 'teacher_login.html', {'error': 'Account not registered as a teacher.'})
            #use django's already implemented login function
            login(request, user)
            return redirect('group3:teacher_landing')
        else:
            return render(request, 'teacher_login.html', {'error': 'Invalid username or password'})

    return render(request, 'teacher_login.html')

#method for signup of a teacher
def teacher_signup(request):
    if request.method == 'POST':
        username     = request.POST.get('username')
        password     = request.POST.get('password')
        name         = request.POST.get('name')
        email        = request.POST.get('email')
        language     = request.POST.get('language')

        # Files (optional)
        pic_file     = request.FILES.get('profile_picture')
        resume_file  = request.FILES.get('resume')


        #the teacher has to already have a user before in the website
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'teacher_signup.html', {
                'error': 'Invalid username or password.'
            })

        if Teacher.objects.filter(user=user).exists():
            return render(request, 'teacher_signup.html', {
                'error': 'This account is already a teacher.'
            })

        if Teacher.objects.filter(email=email).exists():
            return render(request, 'teacher_signup.html', {
                'error': 'A teacher with this email already exists.'
            })

        with transaction.atomic():
            # Create the teacher record without files first
            teacher = Teacher.objects.create(
                user=user,
                name=name,
                email=email,
                language=language
            )

            # attach the files the teacher provided
            if pic_file:
                teacher.profile_picture = pic_file
            if resume_file:
                teacher.resume = resume_file

            # save the changes
            teacher.save()

        login(request, user)
        messages.success(request, 'Teacher profile created!')
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

#logout function for the teacher
def teacher_logout(request):
    logout(request)
    return redirect('group3:group3')

#this is the page for the teacher to do all the things they want
def teacher_landing(request):
    # If the user is logged in, try to fetch their Teacher profile (or get None)
    teacher = None
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user=request.user).first()

    timeslots = []
    if teacher:
        timeslots = TimeSlot.objects.filter(teacher=teacher)

    return render(request, 'teacher_landing.html', {
        'teacher': teacher,
        'timeslots': timeslots,
    })

#method for editing the profile
@login_required
def edit_profile(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == 'POST':
        # Update biography
        bio = request.POST.get('biography', '').strip()
        teacher.biography = bio

        # udpate profile picture if uploaded
        if 'profile_picture' in request.FILES:
            # Delete old image if exists
            if teacher.profile_picture:
                old_path = teacher.profile_picture.path
                if os.path.isfile(old_path):
                    os.remove(old_path)

            teacher.profile_picture = request.FILES['profile_picture']

        teacher.save()
        return redirect('group3:teacher_profile')

    return render(request, 'edit_profile.html', {
        'teacher': teacher
    })

#view the reviews made for the teacher
@login_required
def view_reviews(request):
    # Look up the Teacher record for this user
    teacher = get_object_or_404(Teacher, user=request.user)

    # get all reviews for that teacher, newest first
    reviews = teacher.reviews.order_by('-created_at')

    return render(request, 'view_reviews.html', {
        'teacher': teacher,
        'reviews': reviews,
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
        # check for all the fields
        if not (start_time and end_time and dow):
            context['error'] = 'All fields are required.'
            return render(request, 'create_timeslot.html', context)

        # parse datetimes
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
        except ValueError:
            context['error'] = 'Invalid date/time format.'
            return render(request, 'create_timeslot.html', context)

        #check if end is before start
        if end_dt <= start_dt:
            context['error'] = 'End time must be after start time.'
            return render(request, 'create_timeslot.html', context)

        #has to be this year
        if start_dt.year != end_dt.year:
            context['error'] = 'Start and end time must be in the same year.'
            return render(request, 'create_timeslot.html', context)

        # check for overlap
        overlapping = TimeSlot.objects.filter(
            teacher=teacher,
            start_time__lt=end_dt,
            end_time__gt=start_dt
        ).exists()
        if overlapping:
            context['error'] = 'This timeslot overlaps with an existing one.'
            return render(request, 'create_timeslot.html', context)

        #after it was fine then make
        TimeSlot.objects.create(
            teacher=teacher,
            start_time=start_dt,
            end_time=end_dt,
            day_of_week=int(dow)
        )
        return redirect('group3:teacher_landing')

    # GET
    return render(request, 'create_timeslot.html')

#edit the timeslot if the teacher wants to
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

        # arse datetimes
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
        except (TypeError, ValueError):
            return render(request, 'edit_timeslot.html', {
                'error': 'Invalid date/time format.',
                'timeslot': timeslot,
            })

        # check the time
        if end_dt <= start_dt:
            return render(request, 'edit_timeslot.html', {
                'error': 'End time must be after start time.',
                'timeslot': timeslot,
            })

        # has to be the same year
        if start_dt.year != end_dt.year:
            return render(request, 'edit_timeslot.html', {
                'error': 'Start and end time must be in the same year.',
                'timeslot': timeslot,
            })

        #check overlap
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

        # save after conditions
        timeslot.start_time = start_dt
        timeslot.end_time = end_dt
        timeslot.day_of_week = int(day_of_week)
        timeslot.save()

        return redirect('group3:teacher_landing')

    return render(request, 'edit_timeslot.html', {'timeslot': timeslot})

#login for students
#well this method gets the user already made in the website earlier
def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('group3:student_landing')
        else:
            error = "Invalid username or password."
            return render(request, 'student_login.html', {
                'error': error,
                'username': username,
            })

    # GET
    return render(request, 'student_login.html')

#landing or portal page for the students
def student_landing(request):
    # If not logged in, then prompt for login
    if not request.user.is_authenticated:
        return render(request, 'student_landing.html')

    #list all the slots
    available_slots = TimeSlot.objects.filter(is_booked=False).order_by('start_time')

    return render(request, 'student_landing.html', {
        'available_slots': available_slots
    })

#logout method
@login_required
def student_logout(request):
    logout(request)
    return redirect('group3:group3')

#login method
@login_required
def teacher_list(request):
#display all the teachers available for the website
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {
        'teachers': teachers
    })


@login_required
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # Only show slots that are not booked
    available_slots = TimeSlot.objects.filter(
        teacher=teacher,
        is_booked=False
    ).order_by('start_time')

    return render(request, 'teacher_detail.html', {
        'teacher': teacher,
        'available_slots': available_slots
    })


#method for booking a session from a specific teacher
@login_required
def book_timeslot(request, slot_id):
    timeslot = get_object_or_404(TimeSlot, id=slot_id)
    teacher = timeslot.teacher

    # Should not be able to book an already-booked timeslot
    if timeslot.is_booked:
        return render(request, 'book_session.html', {
            'error': 'Sorry, this slot was just booked by someone else.',
            'timeslot': timeslot,
            'teacher': teacher,
        })

    # users should not be able to book their own timeslots
    if teacher.user == request.user:
        return render(request, 'book_session.html', {
            'error': "Sorry, you can't book your own class.",
            'timeslot': timeslot,
            'teacher': teacher,
        })

    if request.method == 'POST':
        student_name = request.user.username
        language = teacher.language

        # Create the session
        Session.objects.create(
            teacher=teacher,
            timeslot=timeslot,
            student_name=student_name,
            language=language,
            start_time=timeslot.start_time,
            end_time=timeslot.end_time,
        )

        # Mark the slot as booked
        timeslot.is_booked = True
        timeslot.save()

        return redirect('group3:student_landing')

    # GET: render the booking confirmation
    return render(request, 'book_session.html', {
        'timeslot': timeslot,
        'teacher': teacher,
    })



@login_required
def student_sessions(request):
    # Filter sessions by the username stored in student_name
    sessions = Session.objects.filter(student_name=request.user.username) \
                              .order_by('-start_time')

    return render(request, 'student_sessions.html', {
        'sessions': sessions
    })


@login_required
def add_review(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # make sure the student had a session
    had_session = Session.objects.filter(
        teacher=teacher,
        student_name=request.user.username
    ).exists()
    if not had_session:
        messages.error(request, "You can only review teachers you’ve had sessions with.")
        return redirect('group3:teacher_detail', teacher_id=teacher.id)

    # stop duplicate reviews — render an “already reviewed” page
    already_reviewed = Review.objects.filter(
        teacher=teacher,
        reviewer_name=request.user.username
    ).exists()
    if already_reviewed:
        return render(request, 'already_reviewed.html', {
            'teacher': teacher
        })

    if request.method == 'POST':
        rating  = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        # validate the rating
        error = None
        try:
            rating_val = int(rating)
            if not (1 <= rating_val <= 5):
                error = "Rating must be between 1 and 5."
        except (TypeError, ValueError):
            error = "Please enter a valid integer rating."

        if error:
            return render(request, 'add_review.html', {
                'teacher': teacher,
                'error': error,
                'rating': rating,
                'comment': comment,
            })

        # Create the review
        Review.objects.create(
            teacher=teacher,
            reviewer_name=request.user.username,
            rating=rating_val,
            comment=comment
        )

        # Recalculate and save the teacher's average rating
        avg = teacher.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        teacher.rating = round(avg, 2)
        teacher.save()

        messages.success(request, "Thank you for your review!")
        return redirect('group3:teacher_detail', teacher_id=teacher.id)

    # GET: render the form
    return render(request, 'add_review.html', {
        'teacher': teacher
    })

#method for editing the session already made based on timeslot
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['start_time', 'end_time', 'class_url', 'status', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time':   forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes':      forms.Textarea(attrs={'rows':4}),
        }

#the page for the session detail
@login_required
def session_detail(request, session_id):
    session = get_object_or_404(Session, pk=session_id, teacher__user=request.user)

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('group3:teacher_landing')
    else:
        form = SessionForm(instance=session)

    return render(request, 'session_detail.html', {
        'session': session,
        'form': form,
    })


