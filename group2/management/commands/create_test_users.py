# yourapp/management/commands/create_test_users.py

import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from group2.models import PartnerProfile  # adjust to match your app name

class Command(BaseCommand):
    help = 'Always create 100 new users with PartnerProfiles and password "root"'

    def handle(self, *args, **kwargs):
        english_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        goals = ['academic', 'career', 'conversation', 'exam', 'travel']
        availability = ['morning', 'afternoon', 'evening', 'weekends', 'flexible']
        native_languages = ['Spanish', 'Chinese', 'Arabic', 'Hindi', 'French', 'German', 'Japanese', 'Portuguese']

        created_count = 0
        user_number = 1

        while created_count < 100:
            username = f"user{user_number}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@example.com",
                    password="root"
                )
                PartnerProfile.objects.create(
                    user=user,
                    biography=f"I am {username}, learning English for {random.choice(goals)}.",
                    native_language=random.choice(native_languages),
                    english_level=random.choice(english_levels),
                    learning_goals=random.choice(goals),
                    availability=random.choice(availability),
                    appear_in_search=True
                )
                created_count += 1
            user_number += 1  # Always increment to avoid conflict

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} new users with profiles."))
