import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PartnerProfileForm
from .models import PartnerProfile
from group2_chat.views import chat


def home(request):
    return  redirect('group2:chat:index')


@login_required
def profile_view_or_edit(request, username):
    target_user = get_object_or_404(User, username=username)
    profile, _ = PartnerProfile.objects.get_or_create(user=target_user)

    if request.user == target_user:
        # Current user editing their own profile
        if request.method == 'POST':
            form = PartnerProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('group2:profile_page', username=username)
        else:
            form = PartnerProfileForm(instance=profile)
        return render(request, 'edit_profile.html', {
            'form': form,
            'is_own_profile': True,
        })

    else:
        # Placeholder for showing other user's public profile (to be implemented)
        return render(request, 'view_profile.html', {
            'profile': profile,
            'target_user': target_user,
            'is_own_profile': False,
        })


@login_required
def find_partners(request):

    profile, _ = PartnerProfile.objects.get_or_create(user=request.user)

    match_profiles = profile.find_partners()

    match_users = []

    for profile in match_profiles:
        match_users.append(partner(profile.user.username, profile.biography, profile.learning_goals))

    return render(request, 'search.html', {
        'match_users': match_users,
        'user_profile': profile
    })

class partner:
    def __init__(self, username, bio, goals):
        self.username = username
        self.bio = bio
        self.goals = goals
