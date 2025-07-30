from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


#user model will be shared accross the entire website
# so it is not here

from django.contrib.auth.models import User
from django.db import models
from .storage_backends import teacher_storage

#teacher model showing a teacher entity, can add biography and images and stuff like that
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)

    # this right here is for uploading the images to the storage backednds
    profile_picture = models.ImageField(
        upload_to='profiles/%Y/%m/%d/',
        storage=teacher_storage,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Teacher name: {self.name}"

#timeslot entity showing a time that a teacher may have as the time for a session
class TimeSlot(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='time_slots'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    # which day is it?
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

#a session which shows a meeting between a student and a teacher
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
    #add the url of the class so that a student may join
    class_url = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session with {self.student_name} on {self.language}"


#this model can be used for a sample that a teacher may provide
class TeachingSample(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teaching_samples')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='teaching_samples/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.teacher.name}"


# okay so this model is a review that has a many to one relationship witht the teacher model
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


