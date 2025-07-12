from django.db import models
from django.contrib.postgres.fields import JSONField  # For word_list

# No User model here; user_id is an integer placeholder for now.

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()  # Will be replaced with FK to User later
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed')], default='in_progress')
    current_question_index = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz {self.id} (User {self.user_id}) - {self.status}"

class Question(models.Model):
    QUESTION_TYPES = [
        ('IMAGE', 'Image'),
        ('GRAMMAR', 'Grammar'),
        ('READING', 'Reading'),
        ('VOCAB', 'Vocab'),
        ('LISTENING', 'Listening'),
        ('WRITING', 'Writing'),
    ]
    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    text_or_prompt = models.TextField()
    passage_text = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    word_list = models.JSONField(null=True, blank=True)  # Requires Django 3.1+
    correct_text_answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Question {self.id} - {self.type} - {self.difficulty_level}"

class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice {self.id} for Question {self.question.id}"

class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"QuizQuestion {self.id} (Quiz {self.quiz.id}, Question {self.question.id})"
