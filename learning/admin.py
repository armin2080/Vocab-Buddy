from django.contrib import admin
from .models import ReviewSession


@admin.register(ReviewSession)
class ReviewSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'completed')
