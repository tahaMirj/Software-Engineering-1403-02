from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.templatetags.static import static
from django.db.models import F, Count, Case, When, IntegerField
from django.templatetags.static import static
from .models import Quiz, Question, Choice, QuizQuestion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
import string
from .ai import generate_feedback_from_api
from django.db.models import Q
from django.utils.timezone import localtime


# Create your views here.

@login_required
def home(request):
    # Calculate user's score for each quiz type
    skill_scores = QuizQuestion.objects.filter(
        quiz__user_id=request.user.id
    ).values(
        'question__type'
    ).annotate(
        total_questions=Count('id'),
        correct_answers=Count(Case(When(is_correct=True, then=1), output_field=IntegerField()))
    ).order_by('question__type')

    # Calculate percentage and prepare data for the template
    for score in skill_scores:
        score['percentage'] = (score['correct_answers'] * 100) / score['total_questions'] if score['total_questions'] > 0 else 0
        # Get the display name for the question type
        score['type_display'] = dict(Question.QUESTION_TYPES).get(score['question__type'], score['question__type'])


    context = {
        'group_number': '1',
        'user': request.user,
        'skill_scores': skill_scores,
    }
    return render(request, 'group1.html', context)

@login_required
def start_grammar_quiz(request):
    """
    Create a new grammar quiz instance with 10 random grammar questions
    """
    # Clear any previous quiz session data to ensure a fresh start
    if 'current_grammar_quiz_id' in request.session:
        del request.session['current_grammar_quiz_id']

    # Create a new quiz instance
    quiz = Quiz.objects.create(
        title='Grammar Quiz',
        user_id=request.user.id,
        status='in_progress'
    )

    # Get 10 random grammar questions
    grammar_questions = Question.objects.filter(type='GRAMMAR').order_by('?')[:10]

    if grammar_questions.count() < 10:
        messages.error(request, 'Not enough grammar questions available in the database.')
        return redirect('group1:group1')

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
    
    # Data for JavaScript
    js_data = {
        'show_feedback': show_feedback,
        'is_correct': is_correct,
        'correct_choice_id': correct_choice.id if correct_choice else None,
        'user_answer_id': int(user_answer) if user_answer else None,
    }

    context = {
        'quiz': quiz,
        'question': question,
        'choices': choices,
        'current_index': current_index + 1,  # Display as 1-based
        'total_questions': total_questions,
        'quiz_progress': quiz_progress,
        'show_feedback': show_feedback,
        'next_url': next_url,
        'quiz_title': 'Grammar Quiz',
        'js_data': js_data,
    }
    return render(request, 'grammar_quiz_question.html', context)

@login_required
def start_vocabulary_quiz(request):
    """
    Create a new vocabulary quiz instance with 10 random vocabulary questions
    """
    # Clear any previous quiz session data to ensure a fresh start
    if 'current_vocabulary_quiz_id' in request.session:
        del request.session['current_vocabulary_quiz_id']

    # Create a new quiz instance
    quiz = Quiz.objects.create(
        title='Vocabulary Quiz',
        user_id=request.user.id,
        status='in_progress'
    )
    
    # Get 10 random vocabulary questions
    vocabulary_questions = Question.objects.filter(type='VOCAB').order_by('?')[:10]
    
    if vocabulary_questions.count() < 10:
        messages.error(request, 'Not enough vocabulary questions available in the database.')
        return redirect('group1:group1')
    
    # Create QuizQuestion instances for each selected question
    for question in vocabulary_questions:
        QuizQuestion.objects.create(
            quiz=quiz,
            question=question,
            user_answer=None,
            is_correct=False
        )
    
    # Store quiz ID in session to track current quiz
    request.session['current_vocabulary_quiz_id'] = quiz.id
    
    # Redirect to the first question
    return redirect('group1:vocabulary_quiz_question')

def vocabulary_quiz_question(request):
    # Get the current quiz from session
    quiz_id = request.session.get('current_vocabulary_quiz_id')
    if not quiz_id:
        # No active quiz, redirect to start a new one
        return redirect('group1:start_vocabulary_quiz')
    
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        # Quiz doesn't exist, start a new one
        return redirect('group1:start_vocabulary_quiz')
    
    quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question').order_by('id')
    
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
            return redirect('group1:vocabulary_quiz_question')
    
    # Data for JavaScript
    js_data = {
        'show_feedback': show_feedback,
        'is_correct': is_correct,
        'correct_choice_id': correct_choice.id if correct_choice else None,
        'user_answer_id': int(user_answer) if user_answer else None,
    }

    context = {
        'quiz': quiz,
        'question': question,
        'choices': choices,
        'current_index': current_index + 1,  # Display as 1-based
        'total_questions': total_questions,
        'quiz_progress': quiz_progress,
        'show_feedback': show_feedback,
        'quiz_title': 'Vocabulary Quiz',
        'js_data': js_data,
    }
    return render(request, 'vocabulary_quiz_question.html', context)

@login_required
def start_image_quiz(request):
    """
    Create a new image quiz instance with 10 random image questions
    """
    # Clear any previous quiz session data to ensure a fresh start
    if 'current_image_quiz_id' in request.session:
        del request.session['current_image_quiz_id']

    # Create a new quiz instance
    quiz = Quiz.objects.create(
        title='Image Quiz',
        user_id=request.user.id,
        status='in_progress'
    )
    
    # Get 10 random image questions
    image_questions = Question.objects.filter(type='IMAGE').order_by('?')[:10]
    
    if image_questions.count() < 10:
        messages.error(request, 'Not enough image questions available in the database.')
        return redirect('group1:group1')
    
    # Create QuizQuestion instances for each selected question
    for question in image_questions:
        QuizQuestion.objects.create(
            quiz=quiz,
            question=question,
            user_answer=None,
            is_correct=False
        )
    
    # Store quiz ID in session to track current quiz
    request.session['current_image_quiz_id'] = quiz.id
    
    # Redirect to the first question
    return redirect('group1:image_quiz_question')

def image_quiz_question(request):
    # Get the current quiz from session
    quiz_id = request.session.get('current_image_quiz_id')
    if not quiz_id:
        # No active quiz, redirect to start a new one
        return redirect('group1:start_image_quiz')
    
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        # Quiz doesn't exist, start a new one
        return redirect('group1:start_image_quiz')
    
    quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question').order_by('id')
    
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
            return redirect('group1:image_quiz_question')
    
    # Data for JavaScript
    js_data = {
        'show_feedback': show_feedback,
        'is_correct': is_correct,
        'correct_choice_id': correct_choice.id if correct_choice else None,
        'user_answer_id': int(user_answer) if user_answer else None,
    }

    context = {
        'quiz': quiz,
        'question': question,
        'choices': choices,
        'current_index': current_index + 1,  # Display as 1-based
        'total_questions': total_questions,
        'quiz_progress': quiz_progress,
        'show_feedback': show_feedback,
        'quiz_title': 'Image Quiz',
        'js_data': js_data,
    }
    return render(request, 'image_quiz_question.html', context)

@login_required
def start_reading_quiz(request):
    """
    Create a new reading quiz instance with a random main reading question and its sub-questions.
    """
    if 'current_reading_quiz_id' in request.session:
        del request.session['current_reading_quiz_id']

    quiz = Quiz.objects.create(
        title='Reading Quiz',
        user_id=request.user.id,
        status='in_progress'
    )

    # Get one random main reading question, where the question is its own parent
    main_question = Question.objects.filter(type='READING', parent_question_id=F('id')).order_by('?').first()
    
    if not main_question:
        messages.error(request, 'No reading passages available.')
        return redirect('group1:group1')

    # Get all sub-questions for the selected main question, excluding the main question itself
    sub_questions = Question.objects.filter(parent_question=main_question).exclude(pk=main_question.pk).order_by('id')

    if not sub_questions.exists():
        messages.error(request, 'No sub-questions found for the selected reading passage.')
        return redirect('group1:group1')

    # Create QuizQuestion instances for each sub-question
    for sub_question in sub_questions:
        QuizQuestion.objects.create(
            quiz=quiz,
            question=sub_question,
        )

    request.session['current_reading_quiz_id'] = quiz.id
    request.session['main_reading_question_id'] = main_question.id
    
    return redirect('group1:reading_quiz_question')

def reading_quiz_question(request):
    quiz_id = request.session.get('current_reading_quiz_id')
    main_question_id = request.session.get('main_reading_question_id')

    if not quiz_id or not main_question_id:
        return redirect('group1:start_reading_quiz')

    try:
        quiz = Quiz.objects.get(id=quiz_id)
        main_question = Question.objects.get(id=main_question_id)
    except Quiz.DoesNotExist or Question.DoesNotExist:
        return redirect('group1:start_reading_quiz')

    quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question').order_by('question__id')
    
    if not quiz_questions.exists():
        messages.error(request, 'No questions found for this quiz.')
        return redirect('group1:group1')

    total_questions = quiz_questions.count()
    current_index = quiz.current_question_index

    if current_index >= total_questions:
        return redirect('group1:quiz_complete', quiz_id=quiz.id)

    current_quiz_question = quiz_questions[current_index]
    question = current_quiz_question.question
    choices = Choice.objects.filter(question=question).order_by('id')
    
    quiz_progress = int(((current_index + 1) / total_questions) * 100)
    
    show_feedback = False
    is_correct = None
    correct_choice = None
    user_answer = None

    if request.method == 'POST':
        if 'submit_answer' in request.POST:
            user_answer = request.POST.get('user_answer')
            correct_choice = choices.filter(is_correct=True).first()
            
            if user_answer and correct_choice:
                is_correct = (int(user_answer) == correct_choice.id)
                current_quiz_question.user_answer = user_answer
                current_quiz_question.is_correct = is_correct
                current_quiz_question.save()
                show_feedback = True
            
        elif 'next_question' in request.POST:
            quiz.current_question_index += 1
            if quiz.current_question_index >= total_questions:
                quiz.status = 'completed'
            quiz.save()
            return redirect('group1:reading_quiz_question')

    js_data = {
        'show_feedback': show_feedback,
        'is_correct': is_correct,
        'correct_choice_id': correct_choice.id if correct_choice else None,
        'user_answer_id': int(user_answer) if user_answer else None,
    }

    context = {
        'quiz': quiz,
        'question': question,
        'choices': choices,
        'passage_text': main_question.passage_text,
        'current_index': current_index + 1,
        'total_questions': total_questions,
        'quiz_progress': quiz_progress,
        'show_feedback': show_feedback,
        'quiz_title': 'Reading Quiz',
        'js_data': js_data,
        'quiz_width': '900px',
    }
    return render(request, 'reading_quiz_question.html', context)

def writing_quiz_question(request):
    context = {
        'quiz_title': 'Writing Quiz',
        'current_index': 3,
        'total_questions': 5,
        'quiz_progress': 60,
    }
    return render(request, 'writing_quiz_question.html', context)

@login_required
def start_sentence_building_quiz(request):
    # Clear any previous quiz session data to ensure a fresh start
    if 'current_sentence_building_quiz_id' in request.session:
        del request.session['current_sentence_building_quiz_id']

    # Create a new quiz instance
    quiz = Quiz.objects.create(
        title='Sentence Building Quiz',
        user_id=request.user.id,
        status='in_progress'
    )
    
    # Get 10 random sentence building questions
    sentence_questions = Question.objects.filter(type='SENTENCE').order_by('?')[:10]
    
    if sentence_questions.count() < 10:
        messages.error(request, 'Not enough sentence building questions available in the database.')
        return redirect('group1:group1')
    
    # Create QuizQuestion instances for each selected question
    for question in sentence_questions:
        QuizQuestion.objects.create(
            quiz=quiz,
            question=question,
            user_answer=None,
            is_correct=False
        )
    
    # Store quiz ID in session to track current quiz
    request.session['current_sentence_building_quiz_id'] = quiz.id
    
    # Redirect to the first question
    return redirect('group1:sentence_building_question')

def sentence_building_question(request):
    quiz_id = request.session.get('current_sentence_building_quiz_id')
    if not quiz_id:
        return redirect('group1:start_sentence_building_quiz')

    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return redirect('group1:start_sentence_building_quiz')

    quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question').order_by('id')
    if not quiz_questions.exists():
        messages.error(request, 'No questions found for this quiz.')
        return redirect('group1:group1')

    total_questions = quiz_questions.count()
    current_index = quiz.current_question_index

    if current_index >= total_questions:
        return redirect('group1:quiz_complete', quiz_id=quiz.id)

    current_quiz_question = quiz_questions[current_index]
    question = current_quiz_question.question
    
    # The correct sentence is stored in text_or_prompt
    correct_sentence = question.correct_text_answer
    # The words to scramble are in word_list, assumed to be comma-separated
    words_to_scramble = [word.strip() for word in question.word_list]
    random.shuffle(words_to_scramble)

    show_feedback = False
    is_correct = None
    user_submitted_sentence = ''

    if request.method == 'POST':
        if 'submit_answer' in request.POST:
            user_submitted_sentence = request.POST.get('user_answer', '').strip()
            # Normalize sentences for comparison to handle whitespace, case, and punctuation
            if correct_sentence:
                translator = str.maketrans('', '', string.punctuation)
                normalized_user_answer = user_submitted_sentence.lower().translate(translator)
                normalized_correct_answer = correct_sentence.lower().translate(translator)

                normalized_user_answer = ' '.join(normalized_user_answer.split())
                normalized_correct_answer = ' '.join(normalized_correct_answer.split())

                is_correct = normalized_user_answer == normalized_correct_answer
            else:
                is_correct = False
            
            current_quiz_question.user_answer = user_submitted_sentence
            current_quiz_question.is_correct = is_correct
            current_quiz_question.save()
            show_feedback = True

        elif 'next_question' in request.POST:
            quiz.current_question_index += 1
            if quiz.current_question_index >= total_questions:
                quiz.status = 'completed'
            else:
                quiz.status = 'in_progress'
            quiz.save()
            return redirect('group1:sentence_building_question')

    context = {
        'quiz': quiz,
        'question': question,
        'words_to_scramble': words_to_scramble,
        'correct_sentence': correct_sentence,
        'current_index': current_index + 1,
        'total_questions': total_questions,
        'quiz_progress': int(((current_index + 1) / total_questions) * 100),
        'show_feedback': show_feedback,
        'is_correct': is_correct,
        'user_submitted_sentence': user_submitted_sentence,
        'quiz_title': 'Sentence Building Quiz',
    }
    return render(request, 'sentence_building_question.html', context)

@login_required
def start_listening_quiz(request):
    """Create a new listening quiz instance with 10 random listening questions"""
    # Clear any previous quiz session data to ensure a fresh start
    if 'current_listening_quiz_id' in request.session:
        del request.session['current_listening_quiz_id']

    quiz = Quiz.objects.create(
        title='Listening Quiz',
        user_id=request.user.id,
        status='in_progress'
    )

    listening_questions = Question.objects.filter(type='LISTENING').order_by('?')[:10]
    if listening_questions.count() < 10:
        messages.error(request, 'Not enough listening questions available in the database.')
        return redirect('group1:group1')

    for question in listening_questions:
        QuizQuestion.objects.create(
            quiz=quiz,
            question=question,
            user_answer=None,
            is_correct=False
        )

    request.session['current_listening_quiz_id'] = quiz.id
    return redirect('group1:listening_quiz_question')

def listening_quiz_question(request):
    quiz_id = request.session.get('current_listening_quiz_id')
    if not quiz_id:
        return redirect('group1:start_listening_quiz')
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        # If quiz is not found, clear the session and start a new one
        if 'current_listening_quiz_id' in request.session:
            del request.session['current_listening_quiz_id']
        return redirect('group1:start_listening_quiz')

    # If the quiz found in the session is already completed, force a new start
    if quiz.status == 'completed':
        del request.session['current_listening_quiz_id']
        return redirect('group1:start_listening_quiz')

    quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question').order_by('id')
    if not quiz_questions.exists():
        messages.error(request, 'No questions found for this quiz.')
        return redirect('group1:group1')

    total_questions = quiz_questions.count()
    current_index = quiz.current_question_index
    if current_index >= total_questions:
        return redirect('group1:quiz_complete', quiz_id=quiz.id)

    current_quiz_question = quiz_questions[current_index]
    question = current_quiz_question.question
    choices = Choice.objects.filter(question=question).order_by('id')

    quiz_progress = int(((current_index + 1) / total_questions) * 100)

    show_feedback = False
    is_correct = None
    correct_choice = choices.filter(is_correct=True).first()
    user_answer = None

    js_data = {
        'show_feedback': False,
        'is_correct': None,
        'correct_choice_id': correct_choice.id if correct_choice else None,
        'user_answer_id': None,
    }

    if request.method == 'POST':
        if 'submit_answer' in request.POST:
            user_answer = request.POST.get('user_answer')
            if user_answer and correct_choice:
                is_correct = (int(user_answer) == correct_choice.id)
                current_quiz_question.user_answer = user_answer
                current_quiz_question.is_correct = is_correct
                current_quiz_question.save()
                show_feedback = True

                js_data.update({
                    'show_feedback': True,
                    'is_correct': is_correct,
                    'user_answer_id': int(user_answer),
                })
        elif 'next_question' in request.POST:
            quiz.current_question_index += 1
            quiz.save()

            if quiz.current_question_index >= total_questions:
                quiz.status = 'completed'
                quiz.save()
                return redirect('group1:quiz_complete', quiz_id=quiz.id)
            
            return redirect('group1:listening_quiz_question')

    # Resolve voice_url to handle both external URLs and local static files
    resolved_voice_url = question.voice_url
    if resolved_voice_url and not resolved_voice_url.startswith('http'):
        resolved_voice_url = static(resolved_voice_url)

    context = {
        'quiz': quiz,
        'question': question,
        'choices': choices,
        'resolved_voice_url': resolved_voice_url,
        'current_index': current_index + 1,
        'total_questions': total_questions,
        'quiz_progress': quiz_progress,
        'show_feedback': show_feedback,
        'is_correct': is_correct,
        'correct_choice_id': correct_choice.id if correct_choice else None,
        'quiz_title': 'Listening Quiz',
        'js_data': js_data,
        'quiz_width': '700px',  # Custom width for this quiz
    }
    return render(request, 'listening_quiz_question.html', context)

def quiz_complete(request, quiz_id):
    """View to display quiz completion results with AI-generated personalized feedback"""
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

    # ✅ NEW: Generate AI personalized feedback
    incorrect_questions = quiz_questions.filter(is_correct=False).prefetch_related('question__choices')
    api_key = "tpsg-z2NijAI5tE2pUSLpFFppFPSChCGavaA"  

    personalized_feedback = ""
    if incorrect_questions.exists():
        try:
            personalized_feedback = generate_feedback_from_api(incorrect_questions, api_key)
        except Exception as e:
            personalized_feedback = "⚠️ An error occurred while generating feedback."

    context = {
        'quiz': quiz,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': score_percentage,
        'quiz_questions_with_answers': quiz_questions_with_answers,
        'personalized_feedback': personalized_feedback,
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

def review_mistakes(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Get only the incorrect questions
    incorrect_questions = QuizQuestion.objects.filter(
        quiz=quiz,
        is_correct=False
    ).select_related('question').prefetch_related('question__choices')

    context = {
        'quiz': quiz,
        'incorrect_questions': incorrect_questions,
    }

    return render(request, 'review_mistakes.html', context)


@login_required
def retry_mistakes(request, quiz_id):
    original_quiz = get_object_or_404(Quiz, id=quiz_id)

    # Get the questions the user got wrong
    incorrect_questions = QuizQuestion.objects.filter(
        quiz=original_quiz,
        is_correct=False
    ).select_related('question')

    if not incorrect_questions.exists():
        messages.info(request, "You have no mistakes to retry.")
        return redirect('group1:quiz_complete', quiz_id=quiz_id)

    # Create a new quiz instance
    new_quiz = Quiz.objects.create(
        title=f"Retry - {original_quiz.title}",
        user_id=request.user.id,
        status='not_started',
        current_question_index=0
    )

    # Copy only the incorrect questions into the new quiz
    for q in incorrect_questions:
        QuizQuestion.objects.create(
            quiz=new_quiz,
            question=q.question,
            user_answer=None,
            is_correct=False
        )

    # Save new quiz ID in session to continue the flow
    request.session['current_grammar_quiz_id'] = new_quiz.id

    return redirect('group1:grammar_quiz_question')  # or dynamic based on quiz type


@login_required
def progress_dashboard(request):
    """Show user's progress over time with charts"""
    
    quizzes = Quiz.objects.filter(
        user_id=request.user.id,
        status='completed'
    ).order_by('create_date')

    labels = []  # X-axis labels (dates)
    grammar_scores = []
    vocab_scores = []
    image_scores = []
    reading_scores = []
    sentence_scores = []
    listening_scores = []

    for q in quizzes:
        questions = QuizQuestion.objects.filter(quiz=q)
        total = questions.count()
        correct = questions.filter(is_correct=True).count()
        score = int((correct / total) * 100) if total > 0 else 0
        
        labels.append(localtime(q.create_date).strftime("%Y-%m-%d"))

        if "Grammar" in q.title:
            grammar_scores.append(score)
            vocab_scores.append(None)
            image_scores.append(None)
            reading_scores.append(None)
            sentence_scores.append(None)
            listening_scores.append(None)
        elif "Vocabulary" in q.title:
            vocab_scores.append(score)
            grammar_scores.append(None)
            image_scores.append(None)
            reading_scores.append(None)
            sentence_scores.append(None)
            listening_scores.append(None)
        elif "Image" in q.title:
            image_scores.append(score)
            grammar_scores.append(None)
            vocab_scores.append(None)
            reading_scores.append(None)
            sentence_scores.append(None)
            listening_scores.append(None)
        elif "Reading" in q.title:
            reading_scores.append(score)
            grammar_scores.append(None)
            vocab_scores.append(None)
            image_scores.append(None)
            sentence_scores.append(None)
            listening_scores.append(None)
        elif "Sentence" in q.title:
            sentence_scores.append(score)
            grammar_scores.append(None)
            vocab_scores.append(None)
            image_scores.append(None)
            reading_scores.append(None)
            listening_scores.append(None)
        elif "Listening" in q.title:
            listening_scores.append(score)
            grammar_scores.append(None)
            vocab_scores.append(None)
            image_scores.append(None)
            reading_scores.append(None)
            sentence_scores.append(None)

    context = {
        'labels': labels,
        'grammar_scores': grammar_scores,
        'vocab_scores': vocab_scores,
        'image_scores': image_scores,
        'reading_scores': reading_scores,
        'sentence_scores': sentence_scores,
        'listening_scores': listening_scores,
    }

    return render(request, 'progress_dashboard.html', context)
