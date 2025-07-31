from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from .models import Profile, ChatRequest, Message, Rating
from .forms import ProfileForm, RatingForm
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
import os
from django.conf import settings

# -------------------- search ---------------------

LEARNING_CHOICES = [
    ('vocabulary', 'Vocabulary'),
    ('grammar', 'Grammar'),
    ('listening', 'Listening'),
    ('speaking', 'Speaking'),
    ('reading', 'Reading'),
    ('writing', 'Writing'),
]

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    selected_interests = request.GET.getlist('interest')

    profiles = Profile.objects.exclude(user=request.user)

    if query:
        profiles = profiles.filter(Q(user__username__icontains=query) | Q(firstname__icontains=query) | 
                                   Q(lastname__icontains=query))

    if selected_interests:
        filtered_profiles = []
        for profile in profiles:
            if any(interest in profile.learning_interest for interest in selected_interests):
                filtered_profiles.append(profile)
        profiles = filtered_profiles

    context = {
        'profiles': profiles,
        'query': query,
        'learning_choices': [
            ('vocabulary', 'Vocabulary'),
            ('grammar', 'Grammar'),
            ('listening', 'Listening'),
            ('speaking', 'Speaking'),
            ('reading', 'Reading'),
            ('writing', 'Writing'),
        ],
        'selected_interests': selected_interests,
    }

    return render(request, 'search_results.html', context)

# -------------------- Profile --------------------

@login_required
def serve_avatar(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'group5' , 'media', 'avatars', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        raise Http404("Avatar not found.")

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    usernames = sorted([make_safe_identifier(username), make_safe_identifier(request.user.username)])
    room_name = f"{usernames[0]}_{usernames[1]}"
    return render(request, 'view_profile.html', {
        'target': user,
        'user': request.user,
        'room_name': room_name
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            pro = profile_form.save()
            if 'avatar' in request.FILES:
                pro.avatar = request.FILES["avatar"]
                pro.save()
            return redirect('group5:my_profile')
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {
        'form': profile_form,
        'user': request.user
    })

@login_required
def my_profile(request):
    profile = request.user.profile
    return render(request, 'setting-account.html', {
        'profile_user': request.user,
        'profile': profile,
    })

# -------------------- Chat Request --------------------
@login_required
def send_chat_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)

    if to_user == request.user:
        messages.error(request, "شما نمی‌توانید به خودتان درخواست بفرستید.")
        return redirect('group5:chat_partners')

    if ChatRequest.exists_active_request(request.user, to_user):
        messages.warning(request, 'شما قبلاً با این کاربر درخواست یا چت فعال دارید.')
    else:
        ChatRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, 'درخواست چت با موفقیت ارسال شد.')

    return redirect('group5:chat_requests')

@login_required
def chat_requests_view(request):
    user = request.user
    sent_req = ChatRequest.objects.filter(from_user=user)
    received_req = ChatRequest.objects.filter(to_user=user)
    def categorize_requests(queryset):
        result = {'pending': [], 'rejected': [], 'accepted': []}
        for req in queryset:
            result[req.status].append(req) if req.status in result else result['rejected'].append(req)
        return result

    sent = categorize_requests(sent_req)
    received = categorize_requests(received_req)
    return render(request, 'chat_requests.html', {
        'sent_requests_p': sent['pending'],
        'sent_requests_a': sent['accepted'],
        'sent_requests_r': sent['rejected'],
        'received_requests_p': received['pending'],
        'received_requests_a': received['accepted'],
        'received_requests_r': received['rejected'],
        'user': request.user
    })

@login_required
def respond_to_chat_request(request, request_id, action):
    chat_request = get_object_or_404(ChatRequest, id=request_id)
    if action == "cancel":
        chat_request.status = "cancelled"
        messages.warning(request, "شما درخواست را کنسل کردید")
    else:
        if chat_request.to_user != request.user:
            messages.error(request, "شما اجازه ندارید به این درخواست پاسخ دهید.")
            return redirect('group5:chat_requests')
        if chat_request.status != 'pending':
            messages.warning(request, "این درخواست قبلاً بررسی شده.")
            return redirect('group5:chat_requests')
        if action == 'accept':
            chat_request.status = 'accepted'
            messages.success(request, "درخواست را قبول کردید.")
        elif action == 'reject':
            chat_request.status = 'rejected'
            messages.info(request, "درخواست را رد کردید.")
        else:
            messages.error(request, "عملیات نامعتبر.")
            return redirect('group5:chat_requests')
    chat_request.save()
    return redirect('group5:chat_requests')

# -------------------- Chat Room --------------------
@login_required
def chat_room(request, room_name):
    username = request.user.username
    names = make_email_username(room_name).split("_")
    
    allowed = ChatRequest.objects.filter(
        status='accepted',
        from_user__username__in=names,
        to_user__username__in=names
    ).exists()
    if not allowed:
        # messages.error(request, "شما اجازه دسترسی به این اتاق را ندارید.")
        return redirect('group5:chat_partners')

    partner_name = ""
    if names[0] == username:
        partner_name = names[1]
    else:
        partner_name = names[0]
        
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    
    partner = User.objects.get(username = partner_name)

    return render(request, 'chat_room.html', {
        'room_name': room_name,
        'user': request.user,
        'partner' : partner,
        'messages' : messages
    })

@login_required
def serve_file(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'group5' , 'media', 'chat_file', filename)
    
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        raise Http404("file not found.")

@login_required
def chat_partners(request):
    accepted_requests = ChatRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        status='accepted'
    )
    partners = []
    for req in accepted_requests:
        partner = req.to_user if req.from_user == request.user else req.from_user
        usernames = sorted([make_safe_identifier(request.user.username), make_safe_identifier(partner.username)])
        room_name = f"{usernames[0]}_{usernames[1]}"
        last_msg = Message.objects.filter(room_name = room_name).order_by("timestamp").last()
        if last_msg:
            last_msg = last_msg.content
            if len(last_msg) > 20:
                last_msg = last_msg[:20] + "..."
        else:
            last_msg = "Start the chat."
        partners.append({
            'user': partner,
            'room_name': room_name,
            'last_msg' : last_msg
        })
    return render(request, 'chat_partners.html', {
        'partners': partners,
        'user': request.user,
    })

@csrf_exempt
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        path = default_storage.save(f"group5/media/chat_files/{file.name}", file)
        return JsonResponse({"url": default_storage.url(path)})
    return JsonResponse({"error": "No file"}, status=400)

# --------------------- HOME ---------------------
@login_required
def home(request):
    return render(request, 'group5.html', {'user': request.user})

# -------------------- RATING --------------------
@login_required
def rate_partner(request, username):
    partner = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                rater=request.user,
                ratee=partner,
                defaults={'score': form.cleaned_data['score'], 'comment': form.cleaned_data['comment']}
            )
            return redirect('group5:view_rating', username=partner.username)
    else:
        try:
            existing_rating = Rating.objects.get(rater=request.user, ratee=partner)
            form = RatingForm(initial={'score': existing_rating.score, 'comment': existing_rating.comment})
        except Rating.DoesNotExist:
            form = RatingForm()
    return render(request, 'rate_partner.html', {
        'partner': partner,
        'form': form,
        'user': request.user,
    })

@login_required
def view_rating(request, username):
    partner = get_object_or_404(User, username=username)
    ratings = Rating.objects.filter(ratee=partner)
    avg_score = ratings.aggregate(models.Avg('score'))['score__avg']
    return render(request, 'view_rating.html', {
        'partner': partner,
        'ratings': ratings,
        'avg_score': avg_score
    })

# --------------------- COMING SOON ---------------------
@login_required
def general_settings(request):
    return render(request, "setting-general.html")

@login_required
def billing_settings(request):
    return render(request, "setting-billing.html")

# --------------------- UTILS ---------------------

def make_safe_identifier(email):
    return email.replace('@', '_at_').replace('.', '_dot_')

def make_email_username(email):
    return email.replace('_at_', '@').replace('_dot_', '.')
