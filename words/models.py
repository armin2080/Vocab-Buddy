from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Word(models.Model):
    """German vocabulary words with translations and CEFR levels"""
    
    CEFR_LEVELS = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper-Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Proficient'),
    ]
    
    word = models.CharField(max_length=255, unique=True)
    translation = models.TextField()
    cefr_level = models.CharField(max_length=2, choices=CEFR_LEVELS)
    example_sentences = models.TextField(blank=True, default='')
    context_paragraph = models.TextField(blank=True, default='')
    verb_forms = models.TextField(blank=True, default='')
    is_verb = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['word']
        indexes = [
            models.Index(fields=['cefr_level']),
            models.Index(fields=['word']),
        ]
    
    def __str__(self):
        return f"{self.word} ({self.cefr_level})"


class UserWord(models.Model):
    """User's collection of words with review tracking"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_words')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    review_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'word']
        ordering = ['-added_at']
        indexes = [
            models.Index(fields=['user', 'word']),
            models.Index(fields=['user', 'last_reviewed']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.word.word}"
    
    def compute_score(self):
        """
        Calculate spaced repetition score based on:
        - Time since last review (logarithmic growth)
        - Review frequency (inverse relationship)
        """
        import math
        
        if self.last_reviewed is None:
            days_since_last = 1
        else:
            days_since_last = (datetime.now().replace(tzinfo=None) - self.last_reviewed.replace(tzinfo=None)).days + 1
        
        time_score = math.log(days_since_last + 1)
        review_score = 1 / (self.review_count + 1)
        return time_score * review_score
    
    def get_accuracy(self):
        """Calculate accuracy percentage"""
        if self.review_count == 0:
            return 0
        return round((self.correct_count / self.review_count) * 100, 1)
