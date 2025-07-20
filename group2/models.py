from typing import List
from django.db import models
from django.contrib.auth.models import User

class PartnerFindingProfile(models.Model):

    LANGUAGE_PROFICIENCY_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )

    LEARNING_GOAL_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO 
    user = models.OneToOneField(to=User)
    biography = models.TextField(default='')
    appear_in_search = models.BooleanField(default=True)
    language_proficiency = models.TextField(choices=LANGUAGE_PROFICIENCY_CHOICES, blank=True)
    learning_goal = models.TextField(choices=LEARNING_GOAL_CHOICES, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def search(self) -> List[User]:
        pass
