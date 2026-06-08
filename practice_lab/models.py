from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class PracticeSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_sessions')
    challenge_words = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} practice session'


class PracticeMessage(models.Model):
    ROLE_CHOICES = [
        ('assistant', 'Assistant'),
        ('user', 'User'),
    ]

    session = models.ForeignKey(PracticeSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'pk']

    def __str__(self):
        return f'{self.role}: {self.content[:40]}'
