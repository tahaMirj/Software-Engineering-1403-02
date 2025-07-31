from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.conf import settings
from .models import Reading, ReadingCategory, Question
import re
import json
import edge_tts
import asyncio
import io
import base64
from pydub import AudioSegment

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
    # ابتدا محتوای متنی ریدینگ را از دیتابیس دریافت می کنیم
    reading = get_object_or_404(Reading, id=reading_id)
    content = reading.content

    # سپس پارامترهای موردنیاز (در صورت وجود) را دریافت می کنیم
    try:
        # پارس کردن JSON body
        body_data = json.loads(request.body.decode('utf-8'))
        voice = body_data.get('voice', 'en-US-AriaNeural')
        rate = body_data.get('rate', '0%')
        pitch = body_data.get('pitch', '0Hz')
    except (json.JSONDecodeError, AttributeError):
        # اگر JSON نبود، از POST data استفاده کن
        voice = request.POST.get('voice', 'en-US-AriaNeural')
        rate = request.POST.get('rate', '0%')
        pitch = request.POST.get('pitch', '0Hz')

    # قبل از فرستادن برای تبدیل به صوت متن را به جمله ها تقسیم می کنیم
    sentences = re.split(r'(?<=[.!?])(?!\d)(?![.!?])\s+(?=[A-Z])', content)
    
    # اگر جمله ای بیش از 20 کلمه داشت، آن را به قسمت های کوچکتر تقسیم می کنیم
    lines = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 20:
            # جمله طولانی را در نقاط مناسب (کاما، و، که) تقسیم می کنیم
            parts = re.split(r'(\s*,\s*|\s+and\s+|\s+or\s+|\s+but\s+|\s+which\s+|\s+that\s+)', sentence)
            current_part = ""
            for part in parts:
                # اگر قسمت فعلی + قسمت جدید کمتر از 20 کلمه باشد
                if len((current_part + part).split()) <= 20:
                    current_part += part
                else:
                    # قسمت فعلی را اضافه کن و قسمت جدید را شروع کن
                    if current_part.strip():
                        lines.append(current_part.strip())
                    current_part = part
            # آخرین قسمت را اضافه کن
            if current_part.strip():
                lines.append(current_part.strip())
        else:
            lines.append(sentence)

    # تولید صوت با timestamp دقیق و sentence-level با Edge-TTS
    try:
        async def generate_audio_with_sentence_timing():
            # متن کامل را با نقطه و فاصله بین جملات ترکیب کن
            full_text = '. '.join([line.strip() for line in lines if line.strip()])
            communicate = edge_tts.Communicate(full_text, voice)
            audio_data = b""
            word_boundaries = []
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
                elif chunk["type"] == "WordBoundary":
                    word_boundaries.append({
                        'text': chunk["text"],
                        'offset': chunk["offset"] / 10000000.0,  # seconds
                        'duration': chunk["duration"] / 10000000.0
                    })
            # حالا جملات را با word boundaries مچ کن
            timestamps = []
            sentence_idx = 0
            sentence_words = lines[sentence_idx].strip().replace('  ', ' ').split()
            word_idx = 0
            sentence_start = None
            for i, wb in enumerate(word_boundaries):
                # شروع جمله
                if word_idx == 0:
                    sentence_start = wb['offset']
                word_idx += 1
                # پایان جمله؟
                if word_idx == len(sentence_words):
                    sentence_end = wb['offset'] + wb['duration']
                    timestamps.append({
                        'sentence_id': sentence_idx + 1,
                        'text': lines[sentence_idx].strip(),
                        'start_time': sentence_start,
                        'end_time': sentence_end
                    })
                    sentence_idx += 1
                    if sentence_idx < len(lines):
                        sentence_words = lines[sentence_idx].strip().replace('  ', ' ').split()
                        word_idx = 0
            total_duration_seconds = timestamps[-1]['end_time'] if timestamps else 0
            return audio_data, timestamps, total_duration_seconds
        # اجرای تولید صوت
        audio_data, timestamps, total_duration_seconds = asyncio.run(generate_audio_with_sentence_timing())
        print(f"Generated audio with {len(timestamps)} sentence timestamps")
        # تبدیل به base64 برای ارسال به فرانت اند
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        audio_url = f"data:audio/mp3;base64,{audio_base64}"
        return JsonResponse({
            'audio_url': audio_url,
            'duration': total_duration_seconds,
            'timestamps': timestamps
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
