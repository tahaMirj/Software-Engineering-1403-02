from django.shortcuts import render

# Create your views here.

def home(request):
    return  render (request , 'group1.html' , {'group_number': '1'})

def grammar_quiz_question(request):
    # Mock data for demonstration
    question = {
        'id': 1,
        'text_or_prompt': "The team members are working hard on their project, but they haven't finished it _______."
    }
    choices = [
        {'id': 1, 'text': 'already'},
        {'id': 2, 'text': 'yet'},
        {'id': 3, 'text': 'still'},
        {'id': 4, 'text': 'since'},
    ]
    # Progress and state
    current_index = 3
    total_questions = 10
    quiz_progress = int((current_index / total_questions) * 100)
    user_answer = None
    is_correct = None
    correct_choice = {'id': 2, 'text': 'yet'}
    next_url = '#'  # Placeholder

    # If POST, simulate feedback
    if request.method == 'POST':
        user_answer = request.POST.get('user_answer')
        is_correct = (user_answer == str(correct_choice['id']))

    context = {
        'question': question,
        'choices': choices,
        'current_index': current_index,
        'total_questions': total_questions,
        'quiz_progress': quiz_progress,
        'user_answer': user_answer,
        'is_correct': is_correct,
        'correct_choice': correct_choice,
        'next_url': '#',  # Placeholder for next question
        'quiz_title': 'Grammar Quiz',
    }
    return render(request, 'grammar_quiz_question.html', context)
