from datetime import datetime, timedelta
from django.db import models
from words.models import UserWord


class SpacedRepetitionScheduler:
    """
    Scheduler for spaced-repetition review sessions.
    Selects words based on compute_score() and due dates.
    """
    
    @staticmethod
    def get_due_words(user, limit=20, min_days_since_review=1):
        """
        Get words due for review, sorted by spaced-repetition score.
        
        Args:
            user: User instance
            limit: max words to return
            min_days_since_review: min days since last review to be "due"
        
        Returns:
            List of UserWord instances sorted by review priority
        """
        now = datetime.now()
        cutoff = now - timedelta(days=min_days_since_review)
        
        # Never reviewed OR last review is old enough
        due_words = UserWord.objects.filter(
            user=user
        ).filter(
            models.Q(last_reviewed__isnull=True) | models.Q(last_reviewed__lte=cutoff)
        )[:limit * 2]  # fetch extra to sort by score
        
        # Sort by compute_score (higher = more urgent)
        sorted_words = sorted(due_words, key=lambda uw: uw.compute_score(), reverse=True)
        return sorted_words[:limit]
    
    @staticmethod
    def get_review_batch(user, batch_size=20):
        """
        Get a batch of words for a review session.
        Defaults to words never reviewed, then oldest reviews.
        """
        return SpacedRepetitionScheduler.get_due_words(user, limit=batch_size)
