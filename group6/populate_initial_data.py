import os
import django
import sys # Import sys for better error handling
from django.db.utils import OperationalError, ProgrammingError # Specific database errors

print("Script started: Setting up Django environment...")

try:
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'english_website.settings')
    django.setup()
    print("Django environment setup complete.")
except Exception as e:
    print(f"Error during Django setup: {e}", file=sys.stderr)
    sys.exit(1) # Exit if setup fails

print("Importing models...")
try:
    # Import your models
    from group6.models import Category, Words, DifficultyChoices
    print("Models imported successfully.")
except Exception as e:
    print(f"Error importing models: {e}", file=sys.stderr)
    sys.exit(1) # Exit if model import fails


def populate_data():
    """
    Populates the database with initial Categories and Words.
    This function will create new entries only if they don't already exist.
    """
    print("Starting data population function...")

    # --- Create Categories ---
    categories_to_create = [
        "Animals",
        "Fruits"
    ]

    created_categories = {} # To store created category objects for linking words
    print(f"Attempting to create/get {len(categories_to_create)} categories...")
    for cat_name in categories_to_create:
        try:
            category, created = Category.objects.get_or_create(name=cat_name)
            created_categories[cat_name] = category # Store the object
            if created:
                print(f"  Created Category: {category.name}")
            else:
                print(f"  Category already exists: {category.name}")
        except (OperationalError, ProgrammingError) as db_error:
            print(f"  DATABASE ERROR processing category '{cat_name}': {db_error}", file=sys.stderr)
            print("  This often means a connection issue or table not found. Check Aiven firewall/migrations.", file=sys.stderr)
            sys.exit(1) # Exit if a critical DB error occurs during category creation
        except Exception as e:
            print(f"  General ERROR processing category '{cat_name}': {e}", file=sys.stderr)
            # Continue to next category even if one fails, but log it clearly
    print("Category processing complete.")

    # --- Create Words ---
    words_to_create = [
        # Animals
        {"text": "Cat", "image_url": "/static/images/cat.jpg", "category": "Animals", "difficulty": DifficultyChoices.BEGINNER},
        {"text": "Dog", "image_url": "/static/images/dog.jpg", "category": "Animals", "difficulty": DifficultyChoices.BEGINNER},
        {"text": "Rabbit", "image_url": "/static/images/rabbit.jpg", "category": "Animals", "difficulty": DifficultyChoices.BEGINNER},
        {"text": "Horse", "image_url": "/static/images/horse.jpg", "category": "Animals", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Bear", "image_url": "/static/images/bear.jpg", "category": "Animals", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Wolf", "image_url": "/static/images/wolf.jpg", "category": "Animals", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Shark", "image_url": "/static/images/shark.jpg", "category": "Animals", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Snake", "image_url": "/static/images/snake.jpg", "category": "Animals", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Giraffe", "image_url": "/static/images/giraffe.jpg", "category": "Animals", "difficulty": DifficultyChoices.ADVANCED},
        {"text": "Rhino", "image_url": "/static/images/rhino.jpg", "category": "Animals", "difficulty": DifficultyChoices.ADVANCED},

        #Fruits
        {"text": "Apple", "image_url": "/static/Fruits/images/apple.jpg", "category": "Fruits", "difficulty": DifficultyChoices.BEGINNER},
        {"text": "Banana", "image_url": "/static/Fruits/images/banana.jpg", "category": "Fruits", "difficulty": DifficultyChoices.BEGINNER},
        {"text": "Grape", "image_url": "/static/Fruits/images/grape.jpg", "category": "Fruits", "difficulty": DifficultyChoices.BEGINNER},
        {"text": "Strawberry", "image_url": "/static/Fruits/images/strawberry.jpg", "category": "Fruits", "difficulty": DifficultyChoices.BEGINNER},
        {"text": "Cherry", "image_url": "/static/Fruits/images/cherry.jpg", "category": "Fruits", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Peach", "image_url": "/static/Fruits/images/peach.jpg", "category": "Fruits", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Plum", "image_url": "/static/Fruits/images/plum.jpg", "category": "Fruits", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Watermelon", "image_url": "/static/Fruits/images/watermelon.jpg", "category": "Fruits", "difficulty": DifficultyChoices.INTERMEDIATE},
        {"text": "Mango", "image_url": "/static/Fruits/images/mango.jpg", "category": "Fruits", "difficulty": DifficultyChoices.ADVANCED},
        {"text": "Avocado", "image_url": "/static/Fruits/images/avocado.jpg", "category": "Fruits", "difficulty": DifficultyChoices.ADVANCED},
    ]

    print(f"Attempting to create/get {len(words_to_create)} words...")
    for word_data in words_to_create:
        cleaned_image_url = word_data["image_url"].replace('\\', '/')
        
        category_obj = created_categories.get(word_data["category"])
        if category_obj:
            try:
                word, created = Words.objects.get_or_create(
                    text=word_data["text"],
                    defaults={
                        "image_url": cleaned_image_url,
                        "category": category_obj,
                        "difficulty": word_data["difficulty"]
                    }
                )
                if created:
                    print(f"  Created Word: {word.text} (Category: {word.category.name}, Difficulty: {word.get_difficulty_display()})")
                else:
                    print(f"  Word already exists: {word.text}")
            except (OperationalError, ProgrammingError) as db_error:
                print(f"  DATABASE ERROR processing word '{word_data['text']}': {db_error}", file=sys.stderr)
                print("  This often means a connection issue or table not found. Check Aiven firewall/migrations.", file=sys.stderr)
                sys.exit(1) # Exit if a critical DB error occurs during word creation
            except Exception as e:
                print(f"  General ERROR processing word '{word_data['text']}': {e}", file=sys.stderr)
        else:
            print(f"  Error: Category '{word_data['category']}' not found for word '{word_data['text']}'", file=sys.stderr)

    print("Data population complete.")

if __name__ == '__main__':
    populate_data()
