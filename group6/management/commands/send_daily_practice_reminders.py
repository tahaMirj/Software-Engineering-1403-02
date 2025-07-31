from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from group6.models import Notification 

class Command(BaseCommand):
    help = 'Sends a daily practice reminder notification to users who have not practiced recently.'

    def handle(self, *args, **options):
        self.stdout.write("Starting daily practice reminder job...")
        
        # we want to send a reminder if the user hasn't received one in the last 24 hours
        twenty_four_hours_ago = timezone.now() - timedelta(hours=23, minutes=59) # slightly less than 24h to ensure daily trigger

        # get all active users
        users = User.objects.filter(is_active=True)

        for user in users:
            # check if the user has received a 'practice_reminder' notification in the last 24 hours
            recent_reminder = Notification.objects.filter(
                user=user,
                notification_type='practice_reminder',
                created_at__gte=twenty_four_hours_ago
            ).exists() # for checking if any record matches

            if not recent_reminder:
                Notification.objects.create(
                    user=user,
                    message="It's time to practice! Let's learn some new words.",
                    notification_type='practice_reminder',
                    is_read=False # new reminders are unread by default
                )
                self.stdout.write(self.style.SUCCESS(f"Successfully sent practice reminder to {user.username}"))
            else:
                self.stdout.write(f"Skipping {user.username}: already received a recent practice reminder.")

        self.stdout.write("Daily practice reminder job finished.")