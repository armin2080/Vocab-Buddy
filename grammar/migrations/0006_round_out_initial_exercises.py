from django.db import migrations


EXERCISES = [
    {
        'topic_slug': 'verb-position-main-clauses',
        'prompt': 'Choose the correct sentence with a time phrase first.',
        'option_a': 'Am Montag ich arbeite.',
        'option_b': 'Am Montag arbeite ich.',
        'option_c': 'Am Montag ich arbeite im Buero.',
        'option_d': 'Arbeite am Montag ich.',
        'correct_option': 'B',
        'explanation': 'When a time phrase is first, the conjugated verb still stays in second position.',
        'order': 3,
    },
    {
        'topic_slug': 'definite-articles',
        'prompt': '___ Kinder spielen im Park.',
        'option_a': 'Der',
        'option_b': 'Das',
        'option_c': 'Die',
        'option_d': 'Den',
        'correct_option': 'C',
        'explanation': 'Plural nouns use die in the nominative case.',
        'order': 3,
    },
    {
        'topic_slug': 'nominative-accusative',
        'prompt': 'Sie kauft ___ Tasche.',
        'option_a': 'der',
        'option_b': 'die',
        'option_c': 'den',
        'option_d': 'dem',
        'correct_option': 'B',
        'explanation': 'Tasche is feminine; feminine die stays die in the accusative.',
        'order': 3,
    },
]


def add_exercises(apps, schema_editor):
    GrammarTopic = apps.get_model('grammar', 'GrammarTopic')
    GrammarExercise = apps.get_model('grammar', 'GrammarExercise')

    for item in EXERCISES:
        topic = GrammarTopic.objects.get(slug=item['topic_slug'])
        GrammarExercise.objects.update_or_create(
            topic=topic,
            prompt=item['prompt'],
            defaults={
                'option_a': item['option_a'],
                'option_b': item['option_b'],
                'option_c': item['option_c'],
                'option_d': item['option_d'],
                'correct_option': item['correct_option'],
                'explanation': item['explanation'],
                'order': item['order'],
            },
        )


def remove_exercises(apps, schema_editor):
    GrammarExercise = apps.get_model('grammar', 'GrammarExercise')
    GrammarExercise.objects.filter(prompt__in=[item['prompt'] for item in EXERCISES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('grammar', '0005_expand_a1_a2_topics'),
    ]

    operations = [
        migrations.RunPython(add_exercises, remove_exercises),
    ]
