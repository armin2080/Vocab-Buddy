from django.conf import settings
from django.db import models
from django.utils import timezone


class GrammarTopic(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    cefr_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='A1')
    summary = models.CharField(max_length=240)
    explanation = models.TextField()
    examples = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'cefr_level', 'title']

    def __str__(self):
        return self.title

    def example_lines(self):
        return [line.strip() for line in self.examples.splitlines() if line.strip()]


class GrammarExercise(models.Model):
    topic = models.ForeignKey(GrammarTopic, related_name='exercises', on_delete=models.CASCADE)
    prompt = models.CharField(max_length=255)
    option_a = models.CharField(max_length=120)
    option_b = models.CharField(max_length=120)
    option_c = models.CharField(max_length=120)
    option_d = models.CharField(max_length=120)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
    )
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.topic.title}: {self.prompt}'

    def options(self):
        return [
            ('A', self.option_a),
            ('B', self.option_b),
            ('C', self.option_c),
            ('D', self.option_d),
        ]


class GrammarPracticeSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(GrammarTopic, related_name='practice_sessions', on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.user} - {self.topic} ({self.correct}/{self.total})'

    def accuracy(self):
        return round((self.correct / self.total) * 100) if self.total else 0


class GrammarExerciseAttempt(models.Model):
    session = models.ForeignKey(GrammarPracticeSession, related_name='attempts', on_delete=models.CASCADE)
    exercise = models.ForeignKey(GrammarExercise, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.exercise_id}: {self.selected_option}'


class GrammarCoachEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sentence = models.TextField()
    corrected_sentence = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    cefr_level = models.CharField(max_length=2, blank=True)
    topic = models.CharField(max_length=120, blank=True)
    explanation = models.TextField(blank=True)
    mistakes = models.JSONField(default=list, blank=True)
    examples = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'grammar coach entries'

    def __str__(self):
        return f'{self.user} - {self.sentence[:40]}'
