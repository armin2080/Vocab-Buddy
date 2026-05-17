from .streaks import get_user_streak_days


def study_streak(request):
    streak_days = get_user_streak_days(request.user)
    return {
        'study_streak_days': streak_days,
        'study_streak_label': f'🔥 {streak_days} day streak' if streak_days else '🔥 Start your streak',
    }