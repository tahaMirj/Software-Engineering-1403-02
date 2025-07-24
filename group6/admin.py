from django.contrib import admin
from .models import Category, Words, UserWordStats, UserLevel

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


@admin.register(UserWordStats)
class UserWordStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'correct_count', 'incorrect_count', 'timestamp') 
    list_filter = ('user', 'word__category', 'word__difficulty', 'timestamp') 
    search_fields = ('user__username', 'word__text')
    raw_id_fields = ('user', 'word')
    # ensures the most recent stats are shown first in the admin
    ordering = ('-timestamp',)

@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_level_display', 'updated_at')
    list_filter = ('level',)
    search_fields = ('user__username',)
    # orders users by their most recently updated level (descending)
    ordering = ('-updated_at',)

    # display the human-readable level
    def get_level_display(self, obj):
        return obj.get_level_display()
    get_level_display.short_description = 'Level'


