from django.db import models


class Reading(models.Model):
    """Represents a reading passage"""

    DIFFICULTY_LEVELS = (
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2"),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_LEVELS)
    category = models.ForeignKey('ReadingCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='readings')
    tags = models.ManyToManyField('ReadingTag', blank=True, related_name='readings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['difficulty', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.difficulty})"
    
    def get_image_url(self):
        """Get the full URL for the reading's image (from category)"""
        if self.category:
            return self.category.get_image_url()
        else:
            # Return default image if no category
            return "static/group4/images/base/prac.png"


class Question(models.Model):
    """Questions associated with reading passages"""
    
    QUESTION_TYPES = (
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('fill_blank', 'Fill in the Blank'),
        ('ordering', 'Ordering/Sequencing'),
    )
    
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(help_text="The question being asked")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    correct_answer = models.TextField(blank=True, help_text="The correct answer (for non-multiple choice questions only)")
    explanation = models.TextField(blank=True, help_text="Explanation of the correct answer")
    points = models.IntegerField(default=1, help_text="Points awarded for correct answer")
    order = models.IntegerField(default=0, help_text="Order of question in the reading")
    
    class Meta:
        ordering = ['reading', 'order']
        unique_together = ('reading', 'order')
    
    def __str__(self):
        return f"{self.reading.title} - Q{self.order}: {self.question_text[:50]}..."
    
    def get_correct_answer(self):
        """Get the correct answer based on question type"""
        if self.question_type == 'multiple_choice':
            # For multiple choice, get the correct option
            correct_option = self.options.filter(is_correct=True).first()
            return correct_option.option_text if correct_option else None
        else:
            # For other question types, use the stored correct_answer
            return self.correct_answer
    
    def get_correct_option_id(self):
        """Get the ID of the correct option for multiple choice questions"""
        if self.question_type == 'multiple_choice':
            correct_option = self.options.filter(is_correct=True).first()
            return correct_option.id if correct_option else None
        return None
    
    def get_correct_option_order(self):
        """Get the order number of the correct option for multiple choice questions"""
        if self.question_type == 'multiple_choice':
            correct_option = self.options.filter(is_correct=True).first()
            return correct_option.order if correct_option else None
        return None
    
    def check_answer(self, user_answer):
        """
        Check if user's answer is correct
        
        Args:
            user_answer: For multiple choice, pass option_id or option_order
                        For other types, pass the answer text
        
        Returns:
            bool: True if answer is correct
        """
        if self.question_type == 'multiple_choice':
            # Assume user_answer is the option ID
            try:
                selected_option = self.options.get(id=user_answer)
                return selected_option.is_correct
            except QuestionOption.DoesNotExist:
                return False
        else:
            # For text-based questions, compare text (case-insensitive)
            return self.correct_answer.strip().lower() == str(user_answer).strip().lower()


class QuestionOption(models.Model):
    """Multiple choice options for questions"""
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['question', 'order']
        unique_together = ('question', 'order')
    
    def __str__(self):
        return f"{self.question.reading.title} - Q{self.question.order} - Option {self.order}"


class ReadingCategory(models.Model):
    """Categories/topics for organizing readings"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color for UI display")
    image_path = models.CharField(max_length=500, blank=True, null=True, 
                                 help_text="Full path or URL to image (e.g., 'static/images/categories/tech.jpg' or 'https://cdn.example.com/images/tech.jpg')")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Reading Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_image_url(self):
        """Get the full URL for the category's image"""
        if self.image_path:
            # Check if it's already a full URL (starts with http/https)
            if self.image_path.startswith(('http://', 'https://')):
                return self.image_path
            else:
                # Local path, prepend with static URL handling
                return self.image_path
        else:
            # Return default image based on category name
            default_name = self.name.lower().replace(' ', '_').replace('&', 'and')
            return f"static/images/categories/default/{default_name}.jpg"


class ReadingTag(models.Model):
    """Tags for reading passages (topics, themes, grammar points, etc.)"""
    
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(ReadingCategory, on_delete=models.CASCADE, related_name='tags')
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.category.name}: {self.name}"
