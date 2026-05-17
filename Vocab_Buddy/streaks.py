from datetime import timedelta

from django.utils import timezone

from words.models import UserWord


def get_user_streak_days(user):
    if not user or not user.is_authenticated:
        return 0

    added_dates = set(UserWord.objects.filter(user=user).dates('added_at', 'day'))
    streak = 0
    current_day = timezone.localdate()

    while current_day in added_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak