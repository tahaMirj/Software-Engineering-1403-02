from django.contrib import admin
from .models import Category, Words 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name')
    # fields that can be searched
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Words) 
class WordsAdmin(admin.ModelAdmin):
    list_display = ('word_id', 'text', 'category', 'get_difficulty_display', 'image_url')
    list_filter = ('category', 'difficulty')
    search_fields = ('text', 'image_url')
    ordering = ('text',)

    # display the human-readable difficulty
    def get_difficulty_display(self, obj):
        return obj.get_difficulty_display()
    get_difficulty_display.short_description = 'Difficulty'

