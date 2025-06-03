from django.db import models

# Create your models here.


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    tage = models.CharField(max_length=50)
    metadata = models.CharField(max_length=50)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question {self.id} - {self.type} - {self.difficulty}"

class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    order_in_quiz = models.PositiveIntegerField()

    def __str__(self):
        return f"QuizQuestion {self.id} - Question ID: {self.question.id} - Order: {self.order_in_quiz}"

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='in_progress')
    # TODO: Fix this questions that is a array in class diagram
    questions = models.ManyToManyField(QuizQuestion)
    score = models.IntegerField(default=0)
    # TODO: Fix this time that is a date in class diagram
    missed_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class VocabularyQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    order_in_quiz = models.PositiveIntegerField()

    def __str__(self):
        return f"VocabularyQuestion {self.id} - Question ID: {self.question.id} - Order: {self.order_in_quiz}"

class GrammarQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    order_in_quiz = models.PositiveIntegerField()

    def __str__(self):
        return f"GrammarQuestion {self.id} - Question ID: {self.question.id} - Order: {self.order_in_quiz}"

class SentenceQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    order_in_quiz = models.PositiveIntegerField()

    def __str__(self):
        return f"SentenceQuestion {self.id} - Question ID: {self.question.id} - Order: {self.order_in_quiz}"

class Vocab(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=100)
    definition = models.TextField()
    example = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vocab {self.id} - {self.word}"
