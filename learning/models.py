from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def accuracy(self):
        return (self.correct / self.total) * 100 if self.total else 0


class ReviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
