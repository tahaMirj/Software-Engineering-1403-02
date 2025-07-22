from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Quiz, Question, Choice, QuizQuestion
from django.contrib import messages

# Create your views here.

def home(request):
    return  render (request , 'group1.html' , {'group_number': '1'})

def start_grammar_quiz(request):
    """
    Create a new grammar quiz instance with 10 random grammar questions
    """
    # Create a new quiz instance
    quiz = Quiz.objects.create(
        title='Grammar Quiz',
        user_id=1,  # Placeholder user ID
        status='not_started'
    )
    
    # Get 10 random grammar questions
    grammar_questions = Question.objects.filter(type='GRAMMAR').order_by('?')[:10]
    
    if grammar_questions.count() < 10:
        messages.error(request, 'Not enough grammar questions available in the database.')
        return redirect('group1:home')
    
    # Create QuizQuestion instances for each selected question
    for question in grammar_questions:
        QuizQuestion.objects.create(
            quiz=quiz,
            question=question,
            user_answer=None,
            is_correct=False
        )
    
    # Store quiz ID in session to track current quiz
    request.session['current_grammar_quiz_id'] = quiz.id
    
    # Redirect to the first question
    return redirect('group1:grammar_quiz_question')

def grammar_quiz_question(request):
    # Get the current quiz from session
    quiz_id = request.session.get('current_grammar_quiz_id')
    if not quiz_id:
        # No active quiz, redirect to start a new one
        return redirect('group1:start_grammar_quiz')
    
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        # Quiz doesn't exist, start a new one
        return redirect('group1:start_grammar_quiz')
    
    # Get all quiz questions for this quiz, ordered by question ID
    quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question').order_by('question__id')
    
    if not quiz_questions.exists():
        messages.error(request, 'No questions found for this quiz.')
        return redirect('group1:group1')
    
    total_questions = quiz_questions.count()
    current_index = quiz.current_question_index
    
    # Check if quiz is completed
    if current_index >= total_questions:
        return redirect('group1:quiz_complete', quiz_id=quiz.id)
    
    # Get current question
    current_quiz_question = quiz_questions[current_index]
    question = current_quiz_question.question
    choices = Choice.objects.filter(question=question).order_by('id')
    
    # Calculate progress
    quiz_progress = int(((current_index + 1) / total_questions) * 100)
    
    # Handle form submission
    user_answer = None
    is_correct = None
    correct_choice = None
    show_feedback = False
    
    if request.method == 'POST':
        if 'submit_answer' in request.POST:
            # Process answer submission
            user_answer = request.POST.get('user_answer')
            correct_choice = choices.filter(is_correct=True).first()
            
            if user_answer and correct_choice:
                is_correct = (int(user_answer) == correct_choice.id)
                
                # Update the quiz question with user's answer
                current_quiz_question.user_answer = user_answer
                current_quiz_question.is_correct = is_correct
                current_quiz_question.save()
                
                show_feedback = True
            
        elif 'next_question' in request.POST:
            # Move to next question
            quiz.current_question_index += 1
            if quiz.current_question_index >= total_questions:
                quiz.status = 'completed'
            else:
                quiz.status = 'in_progress'
            quiz.save()
            
            # Redirect to avoid form resubmission
            return redirect('group1:grammar_quiz_question')
    
    # Determine next URL
    if current_index + 1 >= total_questions:
        next_url = None  # This is the last question
    else:
        next_url = 'group1:grammar_quiz_question'
    
    context = {
        'quiz': quiz,
        'question': question,
        'choices': choices,
        'current_index': current_index + 1,  # Display as 1-based
        'total_questions': total_questions,
        'quiz_progress': quiz_progress,
        'user_answer': user_answer,
        'is_correct': is_correct,
        'correct_choice': correct_choice,
        'show_feedback': show_feedback,
        'next_url': next_url,
        'quiz_title': 'Grammar Quiz',
    }
    return render(request, 'grammar_quiz_question.html', context)

def vocabulary_quiz_question(request):
    context = {
        'quiz_title': 'Vocabulary Quiz',
        'current_index': 1,
        'total_questions': 5,
        'quiz_progress': 20,
    }
    return render(request, 'vocabulary_quiz_question.html', context)

def image_quiz_question(request):
    context = {
        'quiz_title': 'Image Quiz',
        'current_index': 2,
        'total_questions': 5,
        'quiz_progress': 40,
    }
    return render(request, 'image_quiz_question.html', context)

def writing_quiz_question(request):
    context = {
        'quiz_title': 'Writing Quiz',
        'current_index': 3,
        'total_questions': 5,
        'quiz_progress': 60,
    }
    return render(request, 'writing_quiz_question.html', context)

def sentence_building_question(request):
    context = {
        'quiz_title': 'Sentence Building',
        'current_index': 4,
        'total_questions': 5,
        'quiz_progress': 80,
    }
    return render(request, 'sentence_building_question.html', context)

def listening_quiz_question(request):
    context = {
        'quiz_title': 'Listening Quiz',
        'current_index': 5,
        'total_questions': 5,
        'quiz_progress': 100,
    }
    return render(request, 'listening_quiz_question.html', context)

def quiz_complete(request, quiz_id):
    """View to display quiz completion results"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question').prefetch_related('question__choices')
    
    total_questions = quiz_questions.count()
    correct_answers = quiz_questions.filter(is_correct=True).count()
    score_percentage = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    
    # Add correct answer info for each question
    quiz_questions_with_answers = []
    for quiz_question in quiz_questions:
        correct_choice = quiz_question.question.choices.filter(is_correct=True).first()
        quiz_questions_with_answers.append({
            'quiz_question': quiz_question,
            'correct_choice': correct_choice,
        })
    
    context = {
        'quiz': quiz,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': score_percentage,
        'quiz_questions_with_answers': quiz_questions_with_answers,
    }
    return render(request, 'quiz_complete.html', context)

def reset_quiz(request, quiz_id):
    """Reset a quiz to start over"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Reset quiz state
    quiz.status = 'not_started'
    quiz.current_question_index = 0
    quiz.save()
    
    # Reset all quiz questions
    QuizQuestion.objects.filter(quiz=quiz).update(
        user_answer=None,
        is_correct=False
    )
    
    messages.success(request, f'{quiz.title} has been reset. You can start over!')
    return redirect('group1:group1')

