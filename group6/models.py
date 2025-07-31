from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User # Import Django's built-in User model for foreign key relationships

class DifficultyChoices(models.IntegerChoices):
    BEGINNER = 1, 'Beginner'
    INTERMEDIATE = 2, 'Intermediate'
    ADVANCED = 3, 'Advanced'


class Category(models.Model):
    # category_id: Primary Key, Auto-increment
    category_id = models.AutoField(primary_key=True, verbose_name="Category ID")
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name="Category Name")

    class Meta:
        db_table = 'Categories'
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Words(models.Model):
    # word_id: Primary Key, Auto-increment
    word_id = models.AutoField(primary_key=True, verbose_name="Word ID")
    text = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Word Text")
    image_url = models.CharField(max_length=255, null=False, blank=False, verbose_name="Image URL")
    
    # category: Foreign Key to Category (Not Null)
    # on_delete=models.RESTRICT prevents deletion of a category if words are linked to it
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        db_column='category_id',
        null=False,
        verbose_name="Category"
    )
    
    difficulty = models.SmallIntegerField(
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.BEGINNER,
        null=False,
        verbose_name="Difficulty Level",
        validators=[
            MinValueValidator(1, message="Difficulty must be at least 1."),
            MaxValueValidator(3, message="Difficulty must be at most 3.")
        ]
    )

    class Meta:
        db_table = 'Words'
        verbose_name = "Word"
        verbose_name_plural = "Words"
        constraints = [
            models.CheckConstraint(
                check=models.Q(difficulty__in=[1, 2, 3]),
                name='difficulty_level_check',
            )
        ]

    def __str__(self):
        return f"{self.text} ({self.get_difficulty_display()})"
    

# this table tracks how many times a user has correctly or incorrectly guessed a specific word
class UserWordStats(models.Model):
    # stat_id: AutoField as the primary key for each stat entry
    stat_id = models.AutoField(primary_key=True, verbose_name="Stat ID")
    
    # user: ForeignKey to Django's built-in User model
    # on_delete=models.CASCADE: If a user is deleted, all their associated word stats are also deleted
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id', 
        null=False,
        verbose_name="User"
    )
    
    # word: ForeignKey to Words
    # on_delete=models.CASCADE: If a word is deleted, its associated stats entries are also deleted
    word = models.ForeignKey(
        Words,
        on_delete=models.CASCADE,
        db_column='word_id',
        null=False,
        verbose_name="Word"
    )
    
    correct_count = models.IntegerField(default=0, verbose_name="Correct Guesses")

    incorrect_count = models.IntegerField(default=0, verbose_name="Incorrect Guesses")

    # timestamp: DateTimeField to record when this stat entry was last updated (or created)
    # auto_now_add=True: Automatically sets the timestamp when the object is first created
    # this is crucial for retrieving "last N words" for level calculation
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Last Updated")

    class Meta:
        db_table = 'user_word_stats'
        verbose_name = "User Word Stat"
        verbose_name_plural = "User Word Stats"
        unique_together = ('user', 'word')
        # Ordering by timestamp ensures that when we query, the most recent stats come last (or first if descending)
        ordering = ['timestamp']

    def __str__(self):
        return f"Stats for {self.user.username} on '{self.word.text}': Correct={self.correct_count}, Incorrect={self.incorrect_count}"

# the overall learning level assigned to each user
class UserLevel(models.Model):
    # user: OneToOneField establishes a one-to-one relationship with Django's User model
    # primary_key=True: both the foreign key to User and the primary key for this table
    # this ensures each user has exactly one UserLevel entry
    # on_delete=models.CASCADE: If a user is deleted, their associated level entry is also deleted
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='user_id', 
        verbose_name="User"
    )
    
    # level: SmallIntegerField to store the user's current level
    # null=False: Ensures every user has an assigned level
    level = models.SmallIntegerField(
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.BEGINNER,
        null=False,
        verbose_name="Current Level"
    )
    
    # updated_at: DateTimeField to record the last time the user's level was updated
    # auto_now=True: Automatically updates the timestamp every time the object is saved
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")

    class Meta:
        db_table = 'user_level'
        verbose_name = "User Level"
        verbose_name_plural = "User Levels"

    def __str__(self):
        # get_level_display() is a Django-generated method for fields with choices
        return f"{self.user.username}'s Level: {self.get_level_display()}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    # type of notification (e.g., 'level_change', 'practice_reminder')
    notification_type = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notifications' 
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        # order notifications by creation date, newest first
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username} ({self.notification_type}): {self.message[:50]}..."