from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

