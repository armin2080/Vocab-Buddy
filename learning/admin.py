from django.contrib import admin
from .models import QuizResult, ReviewSession


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'correct', 'created_at')


@admin.register(ReviewSession)
class ReviewSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'completed')
