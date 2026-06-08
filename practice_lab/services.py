from words.models import UserWord


CEFR_WEIGHT = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6}


def select_challenge_words(user, limit=5):
    """Select difficult words using level, mistakes, and review history."""
    user_words = list(UserWord.objects.filter(user=user).select_related('word'))

    def priority(user_word):
        reviews = user_word.review_count or 0
        mistakes = max(0, reviews - (user_word.correct_count or 0))
        accuracy_penalty = 1 - ((user_word.correct_count or 0) / reviews) if reviews else 0.5
        return (
            CEFR_WEIGHT.get(user_word.word.cefr_level, 0) * 10
            + mistakes * 4
            + accuracy_penalty * 5
            + user_word.compute_score()
        )

    selected = sorted(user_words, key=priority, reverse=True)[:limit]
    return [
        {
            'word': item.word.word,
            'translation': item.word.translation,
            'level': item.word.cefr_level,
        }
        for item in selected
    ]


def build_system_prompt(challenge_words):
    words = '\n'.join(
        f'- {item["word"]} ({item["level"]}): {item["translation"]}'
        for item in challenge_words
    )
    return f"""You are the Practice Lab writing coach for a German learner.

The learner must write a German paragraph using all five challenge words:
{words}

Remember and use the full conversation context. Be encouraging, concise, and accurate.
When the learner submits a paragraph:
1. Check whether every challenge word was used and used appropriately.
2. Explain important grammar, spelling, and word-choice issues.
3. Suggest more natural phrasing.
4. Provide an improved German version.
5. End with one clear next step or invitation to revise.

Always format paragraph feedback using this exact Markdown structure:
## Overall Feedback
<a short assessment>

## Challenge Words
- **<word>:** <how it was used>

## Improvements
- <specific correction or natural phrasing suggestion>

## Improved Version
> <the improved German paragraph>

## Next Step
<one clear next step or invitation to revise>

Use Markdown headings, bold labels, and bullet lists. Keep sections concise.
Do not wrap the response in a Markdown code block.
For follow-up questions or revisions, respond in context and continue coaching.
Do not invent a new set of challenge words during this session."""
