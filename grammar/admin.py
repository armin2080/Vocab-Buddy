from django.contrib import admin

from .models import (
    GrammarCoachEntry,
    GrammarExercise,
    GrammarExerciseAttempt,
    GrammarPracticeSession,
    GrammarTopic,
)


class GrammarExerciseInline(admin.TabularInline):
    model = GrammarExercise
    extra = 1


@admin.register(GrammarTopic)
class GrammarTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'cefr_level', 'order')
    list_filter = ('cefr_level',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'explanation')
    inlines = [GrammarExerciseInline]


@admin.register(GrammarExercise)
class GrammarExerciseAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'topic', 'correct_option', 'order')
    list_filter = ('topic', 'correct_option')
    search_fields = ('prompt', 'explanation')


class GrammarExerciseAttemptInline(admin.TabularInline):
    model = GrammarExerciseAttempt
    extra = 0
    readonly_fields = ('exercise', 'selected_option', 'is_correct')
    can_delete = False


@admin.register(GrammarPracticeSession)
class GrammarPracticeSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'correct', 'total', 'completed_at')
    list_filter = ('topic', 'completed_at')
    search_fields = ('user__username', 'topic__title')
    inlines = [GrammarExerciseAttemptInline]


@admin.register(GrammarCoachEntry)
class GrammarCoachEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'cefr_level', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'cefr_level', 'topic', 'created_at')
    search_fields = ('user__username', 'sentence', 'corrected_sentence', 'explanation')
