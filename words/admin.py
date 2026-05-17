from django.contrib import admin
from .models import Word, UserWord


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'cefr_level', 'created_at')
    list_filter = ('cefr_level', 'created_at')
    search_fields = ('word', 'translation')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'review_count', 'correct_count', 'added_at')
    list_filter = ('user', 'added_at')
    search_fields = ('user__username', 'word__word')
    readonly_fields = ('added_at',)
