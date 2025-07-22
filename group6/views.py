from django.shortcuts import render, redirect 
from django.urls import reverse # to get URL patterns by name
from .models import Words, Category 
import random # for shuffling word order in learning sessions
from django.contrib.auth.decorators import login_required # to restrict access to logged-in users


# renders the main page of group6
def home(request):
    # get all available categories from database to create menu
    categories = Category.objects.all()

    # get current learning session data 
    current_session = request.session.get('learning_session')
    current_word_data = None 
    feedback_message = None 

    # check if a learning session is currently active for the user
    if current_session:
        # if a session exists, get the index of the current word in the session's word list
        current_word_index = current_session.get('current_word_index', 0)
        # get the list of word IDs that are part of this session
        words_in_session = current_session.get('words', []) # list of primary keys (word_id)

        # validate that the current_word_index is within the bounds of the words_in_session list
        if 0 <= current_word_index < len(words_in_session):
            # get the word_id of the current word
            current_word_id = words_in_session[current_word_index]
            # get the actual Word from the database using its primary key (word_id)
            current_word = Words.objects.get(word_id=current_word_id)
            # prepare the word to pass to the template
            current_word_data = {
                'word_id': current_word.word_id, 
                'image_url': current_word.image_url, 
                'text': current_word.text, 
                # 'guessed' flag shows if the user has already revealed/guessed this word 
                'guessed': current_session.get('guessed_current_word', False)
            }

        # Retrieve and remove any feedback message from the session (e.g., "Correct!", "Incorrect!").
        # Using .pop() ensures the message is shown only once.
        feedback_message = request.session.pop('feedback_message', None)

    # render the group6.html template
    return render(request, 'group6.html', {
        'group_number': '6', 
        'categories': categories, 
        'current_word': current_word_data,
        'feedback_message': feedback_message, 
        'session_active': current_session is not None, # Boolean checking if a session is in progress
        'user_is_authenticated': request.user.is_authenticated # Boolean checking if the user is logged in
    })

# start_learning_session view handles the start of a new learning session
# requires the user to be logged in
@login_required(login_url='/registration/login/') # if user is not authenticated, redirect to this URL
def start_learning_session(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        difficulty = request.POST.get('difficulty')

        # query the database for Words that match the selected category and difficulty
        words = Words.objects.filter(category_id=category_id, difficulty=difficulty)
        
        if not words.exists():
            request.session['feedback_message'] = "کلمه‌ای با این مشخصات پیدا نشد. لطفا دسته‌بندی و سطح دیگری را انتخاب کنید."
            return redirect(reverse('group6:group6'))

        # get a list of primary keys (word_id) for the filtered words
        # .values_list('word_id', flat=True) returns a flat list of just the word_ids
        word_ids = list(words.values_list('word_id', flat=True))
        random.shuffle(word_ids)

        # Store the learning session details in the user's Django session.
        request.session['learning_session'] = {
            'words': word_ids,
            'current_word_index': 0, # start with the first word in the shuffled list
            'guessed_current_word': False, 
            'user_id': request.user.id # store the ID of the authenticated user for session validation
        }
        # mark the session as modified to ensure Django saves the changes
        request.session.modified = True

        # home view will detect the active session and display the first word
        return redirect(reverse('group6:group6'))
    
    return redirect(reverse('group6:group6'))

# process_guess handles user interactions during a learning session
@login_required(login_url='/registration/login/') 
def process_guess(request):
    if request.method == 'POST':
        # get the user's typed guess and the action button clicked
        user_guess = request.POST.get('user_guess', '').strip() # .strip() removes leading/trailing whitespace
        action = request.POST.get('action') # value will be 'show_answer', 'next_word', or 'end_session'

        # get the learning session from the user's session
        learning_session = request.session.get('learning_session')

        # --- Session Validation ---
        # check if a learning session is active AND if the session belongs to the current user
        # the user_id check prevents one logged-in user from interfering with another's session
        if not learning_session or learning_session.get('user_id') != request.user.id:
            request.session['feedback_message'] = "جلسه یادگیری فعال نیست یا متعلق به شما نیست. لطفا یک جلسه جدید شروع کنید."
            request.session['learning_session'] = None # Clear potentially invalid or hijacked session
            request.session.modified = True
            return redirect(reverse('group6:group6'))

        current_word_index = learning_session.get('current_word_index', 0)
        words_in_session = learning_session.get('words', [])

        # check that the current word index is still valid within the session's word list
        if not (0 <= current_word_index < len(words_in_session)):
            request.session['feedback_message'] = "خطا در جلسه یادگیری. لطفا یک جلسه جدید شروع کنید."
            request.session['learning_session'] = None # Reset session on invalid state
            request.session.modified = True
            return redirect(reverse('group6:group6'))

        # get the word_id of the current word
        current_word_id = words_in_session[current_word_index]
        # getch the actual Word from the database
        current_word = Words.objects.get(word_id=current_word_id)

        # --- Action Handling ---
        if action == 'show_answer':
            learning_session['guessed_current_word'] = True 
            if user_guess.lower() == current_word.text.lower():
                request.session['feedback_message'] = "حدس شما درست بود!"
            else:
                request.session['feedback_message'] = f"حدس شما غلط بود. کلمه درست: {current_word.text}"
            request.session.modified = True # save session changes
            return redirect(reverse('group6:group6')) 

        elif action == 'next_word':
            learning_session['current_word_index'] += 1 
            learning_session['guessed_current_word'] = False # reset the 'guessed' flag for the new word

            # check if all words in the session have been presented
            if learning_session['current_word_index'] >= len(words_in_session):
                request.session['feedback_message'] = "جلسه یادگیری به پایان رسید!"
                request.session['learning_session'] = None # end the session
            
            request.session.modified = True # save session changes
            return redirect(reverse('group6:group6')) 

        elif action == 'end_session':
            request.session['feedback_message'] = "جلسه یادگیری شما به پایان رسید."
            request.session['learning_session'] = None # clear the learning session data
            request.session.modified = True # save session changes
            return redirect(reverse('group6:group6'))
    
    return redirect(reverse('group6:group6'))



# redirects to the main registration signup
def group6_signup(request):
    return redirect(reverse('signup')) 

# redirects to the main registration login 
def group6_login(request):
    return redirect(reverse('login')) 

# redirects to the main registration logout 
def group6_logout(request):
    return redirect(reverse('logout')) 