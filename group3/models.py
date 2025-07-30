from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

# User model skiped for now


from django.contrib.auth.models import User
from django.db import models
from .storage_backends import teacher_storage

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)

    # Image upload, stored under teacher_attachments/profiles/…
    profile_picture = models.ImageField(
        upload_to='profiles/%Y/%m/%d/',
        storage=teacher_storage,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Teacher name: {self.name}"


class TimeSlot(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='time_slots'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    # Hard-coded day names
    DAY_OF_WEEK_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
    day_of_week = models.PositiveIntegerField(
        choices=DAY_OF_WEEK_CHOICES,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )

    def __str__(self):
        return f"{self.teacher.name} | {self.start_time} - {self.end_time}"

    @property
    def day_name(self):
        """Human-readable day name for templates."""
        return dict(self.DAY_OF_WEEK_CHOICES).get(self.day_of_week, "")


class Session(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='sessions')
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True)
    student_name = models.CharField(max_length=100)
    language = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class_url = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session with {self.student_name} on {self.language}"


class TeachingSample(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teaching_samples')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='teaching_samples/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.teacher.name}"


class Review(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.teacher.name} ({self.rating}/5)"


