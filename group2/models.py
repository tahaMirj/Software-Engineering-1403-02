from typing import List
from django.db import models
from django.contrib.auth.models import User

class PartnerProfile(models.Model):
    CEFR_LEVELS = (
        ('A1', 'Beginner (A1)'),
        ('A2', 'Elementary (A2)'),
        ('B1', 'Intermediate (B1)'),
        ('B2', 'Upper-Intermediate (B2)'),
        ('C1', 'Advanced (C1)'),
        ('C2', 'Proficient (C2)'),
    )

    GOAL_CHOICES = (
        ('academic', 'Academic English'),
        ('career', 'Career Advancement'),
        ('conversation', 'Casual Conversation'),
        ('exam', 'Exam Preparation'),
        ('travel', 'Travel'),
    )

    AVAILABILITY_CHOICES = (
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('weekends', 'Weekends'),
        ('flexible', 'Flexible'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(blank=True, help_text="Tell others about yourself and your learning journey.")
    native_language = models.CharField(max_length=50, blank=True)
    english_level = models.CharField(max_length=2, choices=CEFR_LEVELS, blank=True)
    learning_goals = models.CharField(max_length=20, choices=GOAL_CHOICES, blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, blank=True)
    appear_in_search = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def find_partners(self) -> List['PartnerProfile']:
        # return PartnerProfile.objects.all()
        return PartnerProfile.objects.filter(
            learning_goals=self.learning_goals,
            english_level=self.english_level,
            appear_in_search=True
        ).exclude(id=self.id)
