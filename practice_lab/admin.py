from django.contrib import admin

from .models import PracticeMessage, PracticeSession


@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PracticeMessage)
class PracticeMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'created_at')
    list_filter = ('role',)
    readonly_fields = ('created_at',)
