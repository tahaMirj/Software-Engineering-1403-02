from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

STATUS_CHOICES = [
    ('pending', 'در انتظار'),
    ('accepted', 'پذیرفته شده'),
    ('rejected', 'رد شده'),
    ('cancelled', 'کنسل شد'),
]

class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    ratee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    score = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rater', 'ratee')

    def __str__(self):
        return f"{self.rater.username} rated {self.ratee.username} : {self.score}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='group5/media/avatars/', blank=True, null=True)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    LEARNING_INTEREST_CHOICES = [
        ('vocabulary', 'Vocabulary'),
        ('grammar', 'Grammar'),
        ('listening', 'Listening'),
        ('speaking', 'Speaking'),
        ('reading', 'Reading'),
        ('writing', 'Writing'),
    ]

    learning_interest = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ChatRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} | {self.status}"

    @staticmethod
    def exists_active_request(user1, user2):
        return ChatRequest.objects.filter(
            Q(from_user=user1, to_user=user2) | Q(from_user=user2, to_user=user1),
            status__in=['pending', 'accepted']
        ).exists()


class Message(models.Model):
    room_name = models.CharField(max_length=255, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='group5/media/chat_files/', blank=True, null=True)
    file_url = models.URLField(blank = True , null = True)
    
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.content}"
