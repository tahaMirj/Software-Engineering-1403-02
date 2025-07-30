#!/usr/bin/env python
"""
Test Data Initialization Script for Group 4 - Listening Microservice

This script populates the database with sample data for testing and development.
Run this script from the Django project root:

    python group4/scripts/initialize_test_data.py

Or as a Django management command:
    python manage.py shell < group4/scripts/initialize_test_data.py
"""

import os
import sys
import django
import json
from django.conf import settings

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'english_website.settings')
django.setup()

from django.contrib.auth.models import User
from group4.models import Reading, ReadingCategory, ReadingTag, Question, QuestionOption

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')


def load_json_data(filename):
    """Load data from a JSON file in the data directory"""
    file_path = os.path.join(DATA_DIR, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {filename} in {DATA_DIR}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filename}: {str(e)}")
        return []


def create_categories():
    """Create reading categories from JSON file"""
    categories_data = load_json_data('categories.json')
    
    if not categories_data:
        print("⚠️  No categories data found, skipping category creation")
        return []
    
    categories = []
    for cat_data in categories_data:
        category, created = ReadingCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'color': cat_data['color'],
                'image_path': cat_data.get('image_path', ''),
                'is_active': True
            }
        )
        
        # Update existing categories with new data
        if not created:
            category.description = cat_data['description']
            category.color = cat_data['color']
            category.image_path = cat_data.get('image_path', '')
            category.is_active = True
            category.save()
        
        categories.append(category)
        print(f"{'Created' if created else 'Updated'} category: {category.name}")
    
    return categories


def create_tags(categories):
    """Create reading tags from JSON file"""
    tags_data = load_json_data('tags.json')
    
    if not tags_data:
        print("⚠️  No tags data found, skipping tag creation")
        return []
    
    tags = []
    for tag_data in tags_data:
        try:
            category = next(cat for cat in categories if cat.name == tag_data['category'])
            tag, created = ReadingTag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'category': category}
            )
            
            # Update existing tag category if needed
            if not created and tag.category != category:
                tag.category = category
                tag.save()
            
            tags.append(tag)
            print(f"{'Created' if created else 'Updated'} tag: {tag.name}")
        except StopIteration:
            print(f"⚠️  Warning: Category '{tag_data['category']}' not found for tag '{tag_data['name']}'")
    
    return tags


def create_readings(categories, tags):
    """Create sample reading passages from JSON file"""
    readings_data = load_json_data('readings.json')
    
    if not readings_data:
        print("⚠️  No readings data found, skipping reading creation")
        return []
    
    readings = []
    for reading_data in readings_data:
        try:
            # Get category
            category = next(cat for cat in categories if cat.name == reading_data['category'])
            
            # Create reading
            reading, created = Reading.objects.get_or_create(
                title=reading_data['title'],
                defaults={
                    'description': reading_data['description'],
                    'content': reading_data['content'],
                    'difficulty': reading_data['difficulty'],
                    'category': category,
                }
            )
            
            # Update existing reading with new data
            if not created:
                reading.description = reading_data['description']
                reading.content = reading_data['content']
                reading.difficulty = reading_data['difficulty']
                reading.category = category
                reading.save()
            
            # Clear existing tags if reading already exists (for clean re-initialization)
            if not created:
                reading.tags.clear()
            
            # Add tags
            for tag_name in reading_data.get('tags', []):
                try:
                    tag = next(tag for tag in tags if tag.name == tag_name)
                    reading.tags.add(tag)
                except StopIteration:
                    print(f"⚠️  Warning: Tag '{tag_name}' not found for reading '{reading_data['title']}'")
            
            readings.append(reading)
            print(f"{'Created' if created else 'Updated'} reading: {reading.title}")
            
        except StopIteration:
            print(f"⚠️  Warning: Category '{reading_data['category']}' not found for reading '{reading_data['title']}'")
    
    return readings


def create_questions(readings):
    """Create sample questions for readings from JSON file"""
    questions_data = load_json_data('questions.json')
    
    if not questions_data:
        print("⚠️  No questions data found, skipping question creation")
        return
    
    for q_data in questions_data:
        try:
            # Find the reading
            reading = next(r for r in readings if r.title == q_data['reading_title'])
            
            for question_data in q_data['questions']:
                # Create question
                question, created = Question.objects.get_or_create(
                    reading=reading,
                    order=question_data['order'],
                    defaults={
                        'question_text': question_data['question_text'],
                        'question_type': question_data['question_type'],
                        'correct_answer': question_data.get('correct_answer', ''),
                        'points': question_data['points'],
                    }
                )
                
                # Update question fields if it already exists
                if not created:
                    question.question_text = question_data['question_text']
                    question.question_type = question_data['question_type']
                    question.correct_answer = question_data.get('correct_answer', '')
                    question.points = question_data['points']
                    question.save()
                
                # Clear existing options if question already exists (for clean re-initialization)
                if not created:
                    question.options.all().delete()
                
                # Create options for multiple choice questions
                if question_data['question_type'] == 'multiple_choice' and 'options' in question_data:
                    for order, option_data in enumerate(question_data['options'], 1):
                        option, opt_created = QuestionOption.objects.get_or_create(
                            question=question,
                            order=order,
                            defaults={
                                'option_text': option_data['text'],
                                'is_correct': option_data['is_correct'],
                            }
                        )
                
                print(f"{'Created' if created else 'Updated'} question: {question.question_text[:50]}...")
                
        except StopIteration:
            print(f"⚠️  Warning: Reading '{q_data['reading_title']}' not found for questions")


def main():
    """Main function to initialize all test data"""
    print("🚀 Starting test data initialization...")
    print(f"📁 Data directory: {DATA_DIR}")
    print("=" * 50)
    
    try:
        # Create categories
        print("\n📁 Creating categories...")
        categories = create_categories()
        
        # Create tags
        print("\n🏷️  Creating tags...")
        tags = create_tags(categories)
        
        # Create readings
        print("\n📖 Creating readings...")
        readings = create_readings(categories, tags)
        
        # Create questions
        print("\n❓ Creating questions...")
        create_questions(readings)
        
        print("\n" + "=" * 50)
        print("✅ Test data initialization completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Categories: {ReadingCategory.objects.count()}")
        print(f"   - Tags: {ReadingTag.objects.count()}")
        print(f"   - Readings: {Reading.objects.count()}")
        print(f"   - Questions: {Question.objects.count()}")
        print(f"   - Question Options: {QuestionOption.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error during initialization: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
