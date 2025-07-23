from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.conf import settings
from .models import Reading, ReadingCategory, Question, Results, AttemptHistory
import json
import edge_tts
import asyncio
import io
import base64

# =============================================================================
# MAIN PAGE VIEWS (HTML Templates)
# =============================================================================

def home(request):
    """
    Group 4 - Listening Service Home Page
    
    Displays the main landing page for the listening microservice.
    Shows user progress, recent activities, and quick access to readings.
    
    TODO: Add user progress display, recent listening history
    NOTE: Implementation may change based on UI/UX requirements
    """
    return render(request, 'group4.html', {'group_number': '4'})


def practice_selection(request):
    """
    Practice Mode Selection Page

    Allows users to choose between different difficulty levels
    """
    return render(request, 'practice_level_selection.html')


def quiz_selection(request):
    """
    Quiz Mode Selection Page

    Allows users to select a quiz based on their preferred difficulty level
    """
    return render(request, 'test_level_selection.html')


def reading_list_practice(request):
    """
    Reading List Page with Filtering
    
    Displays all available reading materials with filtering options:
    - Filter by difficulty level (A1-C2)
    - Filter by category
    - Pagination support
    
    Query Parameters:
    - level: difficulty filter
    - category: topic filter
    - page: pagination
    - per_page: items per page
    """
    # Get filter parameters
    level = request.GET.get('level', '')
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 20))
    
    # Start with all readings
    readings = Reading.objects.all()
    
    # Apply filters
    if level:
        readings = readings.filter(difficulty=level)
    
    if category:
        readings = readings.filter(category__name=category)
    
    if search:
        readings = readings.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(content__icontains=search)
        )
    
    # Add annotations for user statistics if needed
    readings = readings.select_related('category').prefetch_related('tags', 'questions')
    
    # Pagination
    paginator = Paginator(readings, per_page)
    page_obj = paginator.get_page(page)
    
    # Get all categories for filter dropdown
    categories = ReadingCategory.objects.filter(is_active=True).order_by('name')
    
    # Get all difficulty levels
    difficulty_levels = Reading.DIFFICULTY_LEVELS
    
    context = {
        'mode': 'practice',
        'readings': page_obj,
        'categories': categories,
        'difficulty_levels': difficulty_levels,
        'current_level': level,
        'current_category': category,
        'current_search': search,
        'paginator': paginator,
    }

    return render(request, 'search_readings.html', context)


def reading_list_quiz(request):
    """
    Reading List Page for Quiz Mode with Filtering
    
    Similar to practice mode but for quiz/assessment purposes.
    Displays all available reading materials with filtering options:
    - Filter by difficulty level (A1-C2)
    - Filter by category
    - Pagination support
    
    Query Parameters:
    - level: difficulty filter
    - category: topic filter
    - page: pagination
    - per_page: items per page
    """
    # Get filter parameters (same as practice mode)
    level = request.GET.get('level', '')
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 20))
    
    # Start with all readings that have questions
    readings = Reading.objects.filter(questions__isnull=False).distinct()
    
    # Apply filters (same logic as practice mode)
    if level:
        readings = readings.filter(difficulty=level)
    
    if category:
        readings = readings.filter(category__name=category)
    
    if search:
        readings = readings.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(content__icontains=search)
        )
    
    # Add annotations for user statistics if needed
    readings = readings.select_related('category').prefetch_related('tags', 'questions')
    
    # Pagination
    paginator = Paginator(readings, per_page)
    page_obj = paginator.get_page(page)
    
    # Get all categories for filter dropdown
    categories = ReadingCategory.objects.filter(is_active=True).order_by('name')
    
    # Get all difficulty levels
    difficulty_levels = Reading.DIFFICULTY_LEVELS
    
    context = {
        'mode': 'quiz',  # Only difference from practice mode
        'readings': page_obj,
        'categories': categories,
        'difficulty_levels': difficulty_levels,
        'current_level': level,
        'current_category': category,
        'current_search': search,
        'paginator': paginator,
    }

    return render(request, 'search_readings.html', context)


def reading_detail(request, reading_id):
    """
    Reading Detail Information Page
    
    Shows detailed information about a specific reading:
    - Reading title, description, difficulty level
    - Available accents and audio files
    - Exercise count and types
    - User's previous attempts/scores
    - Options to enter Practice or Quiz mode
    
    Args:
    - reading_id: ID of the reading to display
    
    TODO: Fetch reading details from database
    NOTE: UI layout may change based on design decisions
    """
    # TODO: Fetch reading from database or return 404
    # TODO: Get user's previous attempts if authenticated
    context = {'reading_id': reading_id}
    return render(request, 'group4/reading_detail.html', context)


def practice_mode(request, reading_id):
    """
    Practice Mode Interface
    
    Interactive listening practice page with full features:
    - Audio player with speed control (0.5x to 2x)
    - Subtitle display with size/visibility controls
    - Sentence-level audio jumping
    - Accent switching (American, British, etc.)
    - Reading text visible for reference
    - No scoring/evaluation
    
    Args:
    - reading_id: ID of the reading for practice
    """
    # Get the specific reading or return 404 if not found
    reading = get_object_or_404(Reading, id=reading_id)
    
    context = {
        'reading': reading,
        'mode': 'practice'
    }
    return render(request, 'practice_view.html', context)


def quiz_mode(request, reading_id):
    """
    Quiz Mode Interface
    
    Assessment-focused listening interface:
    - Audio player (limited controls)
    - No subtitle display during quiz
    - No reading text visible
    - Exercise questions displayed
    - Answer submission and scoring
    - Results and feedback
    
    Args:
    - reading_id: ID of the reading for quiz
    """
    # Get the specific reading or return 404 if not found
    reading = get_object_or_404(Reading, id=reading_id)
    
    # Get all questions for this reading, ordered by their order field
    questions = Question.objects.filter(reading=reading).prefetch_related('options').order_by('order')
    
    context = {
        'reading': reading,
        'questions': questions,
        'mode': 'quiz'
    }
    return render(request, 'quiz_view.html', context)


# =============================================================================
# AUDIO API ENDPOINTS (JSON Responses)
# =============================================================================

@require_http_methods(["POST"])
@csrf_exempt
def generate_audio(request, reading_id):
    """
    Generate New Audio via edge-tts
    
    Creates audio for reading using Microsoft Edge Text-to-Speech:
    - Fetches reading content from database
    - Generates audio using edge-tts library
    - Returns audio data directly as base64-encoded data URL
    - No file storage needed - generated fresh each time
    
    POST Body (optional):
    - voice: voice to use (default: en-US-AriaNeural)
    - rate: speech rate (default: +0%)
    - pitch: speech pitch (default: +0Hz)
    
    Returns:
    JSON with audio_url (data URL) and duration
    """
    pass


# =============================================================================
# SUBTITLE AND TIMING API ENDPOINTS
# =============================================================================

# i Have deemed these unnecessary, keeping them here in case they are needed later
# @require_http_methods(["GET"])
# def get_subtitles(request, reading_id):
#     """
#     Get Subtitle Data with Timestamps
    
#     Returns synchronized subtitle/transcript data:
#     - Sentence-level timestamps (start/end times)
#     - Text content for each subtitle segment
#     - Formatting options (size, visibility)
#     - Highlighting support for current sentence
    
#     Query Parameters:
#     - size: subtitle size (small, medium, large)
#     - show: visibility (true/false)
#     - highlight: enable current sentence highlighting
    
#     Returns:
#     JSON with subtitle segments and timing data
    
#     TODO: Implement subtitle data retrieval
#     TODO: Add formatting options processing
#     NOTE: Timestamps must match audio duration and speed settings
#     """
#     # TODO: Get subtitle preferences from query params
#     # TODO: Fetch subtitle data from database
#     # TODO: Apply formatting preferences
#     return JsonResponse({
#         'subtitles': [
#             {
#                 'sentence_id': 1,
#                 'start_time': 0.0,
#                 'end_time': 3.5,
#                 'text': 'Welcome to our listening exercise.'
#             },
#             {
#                 'sentence_id': 2,
#                 'start_time': 3.5,
#                 'end_time': 7.2,
#                 'text': 'Please listen carefully to the following passage.'
#             }
#         ],
#         'settings': {
#             'size': 'medium',
#             'show': True,
#             'highlight': True
#         }
#     })


# @require_http_methods(["GET"])
# def get_sentence_timestamp(request, reading_id, sentence_id):
#     """
#     Get Specific Sentence Timestamp
    
#     Returns timing information for a specific sentence:
#     - Used for sentence-level audio jumping
#     - Provides exact start/end times
#     - Supports subtitle synchronization
    
#     Args:
#     - reading_id: ID of the reading
#     - sentence_id: ID of the specific sentence
    
#     Returns:
#     JSON with sentence timing and text data
    
#     TODO: Implement sentence lookup by ID
#     TODO: Add error handling for invalid sentence IDs
#     NOTE: Sentence IDs must be consistent across audio and subtitle data
#     """
#     # TODO: Fetch sentence data from database
#     # TODO: Return timing information
#     return JsonResponse({
#         'sentence_id': sentence_id,
#         'start_time': 15.3,
#         'end_time': 19.7,
#         'text': 'This is the selected sentence.',
#         'reading_id': reading_id
#     })


# =============================================================================
# EXERCISE AND PROGRESS API ENDPOINTS
# =============================================================================


@require_http_methods(["POST"])
@csrf_exempt
def submit_exercise(request, reading_id):
    """
    Submit Exercise Answers
    
    Processes user's answer submissions for all questions in a reading:
    - Validates answer format
    - Calculates score/correctness for each question
    - Updates user progress
    - Provides detailed feedback
    
    Args:
    - reading_id: ID of the reading
    
    POST Body:
    - answers: dictionary of question_id -> user_answer
    - reading_id: ID of the reading (redundant but for validation)
    
    Returns:
    JSON with scoring results and detailed feedback
    """
    pass


@require_http_methods(["GET"])
def user_progress(request):
    """
    Get User Progress Data
    
    Returns comprehensive user progress information:
    - Overall listening level and statistics
    - Recent quiz scores and improvements
    - Completed readings and time spent
    - Accent-specific performance data
    - Recommendations for next steps
    
    Returns:
    JSON with user progress metrics
    
    TODO: Implement user identification (session/auth)
    TODO: Calculate progress metrics and statistics
    NOTE: Progress tracking may need privacy considerations
    """
    # TODO: Identify user (session ID or authentication)
    # TODO: Calculate progress statistics
    # TODO: Generate recommendations
    return JsonResponse({
        'user_level': 'intermediate',
        'total_completed': 15,
        'average_score': 78.5,
        'recent_scores': [85, 72, 90, 68, 88],
        'time_spent_minutes': 240,
        'accent_performance': {
            'american': 82,
            'british': 74
        },
        'recommendations': ['Try more advanced readings', 'Practice British accent']
    })
