from django.db import migrations


TOPICS = [
    {
        'title': 'Definite Articles: der, die, das',
        'slug': 'definite-articles',
        'cefr_level': 'A1',
        'summary': 'Learn how German nouns use grammatical gender with der, die, and das.',
        'explanation': 'Every German noun has a grammatical gender. Masculine nouns use der, feminine nouns use die, and neuter nouns use das in the nominative case. Plural nouns also use die. It is best to learn every noun together with its article.',
        'examples': 'der Tisch - the table\ndie Tasche - the bag\ndas Buch - the book\ndie Buecher - the books',
        'order': 1,
        'exercises': [
            ('___ Buch ist neu.', 'Der', 'Die', 'Das', 'Den', 'C', 'Buch is neuter, so the article is das.'),
            ('___ Frau kommt aus Berlin.', 'Der', 'Die', 'Das', 'Dem', 'B', 'Frau is feminine, so the article is die.'),
        ],
    },
    {
        'title': 'Nominative and Accusative',
        'slug': 'nominative-accusative',
        'cefr_level': 'A1',
        'summary': 'Understand the subject of a sentence and the direct object.',
        'explanation': 'The nominative case marks the subject: the person or thing doing the action. The accusative case marks the direct object: the person or thing receiving the action. Masculine der changes to den in the accusative. Feminine die, neuter das, and plural die stay the same.',
        'examples': 'Der Mann sieht den Hund.\nIch kaufe das Buch.\nSie hat die Tasche.',
        'order': 2,
        'exercises': [
            ('Ich sehe ___ Mann.', 'der', 'den', 'dem', 'das', 'B', 'Mann is masculine and the direct object, so der becomes den.'),
            ('___ Hund spielt im Garten.', 'Den', 'Dem', 'Der', 'Das', 'C', 'Hund is the subject, so it stays nominative: der.'),
        ],
    },
    {
        'title': 'Verb Position in Main Clauses',
        'slug': 'verb-position-main-clauses',
        'cefr_level': 'A1',
        'summary': 'German main clauses usually place the conjugated verb in second position.',
        'explanation': 'In a normal German main clause, the conjugated verb appears in position two. The first position can be the subject, a time phrase, or another sentence element. The subject often comes right after the verb when something else is first.',
        'examples': 'Ich lerne Deutsch.\nHeute lerne ich Deutsch.\nAm Abend liest sie ein Buch.',
        'order': 3,
        'exercises': [
            ('Choose the correct sentence.', 'Heute ich lerne Deutsch.', 'Heute lerne ich Deutsch.', 'Heute Deutsch ich lerne.', 'Lerne heute Deutsch ich.', 'B', 'Heute is first, so the conjugated verb lerne comes second.'),
            ('Choose the correct sentence.', 'Ich morgen gehe ins Kino.', 'Morgen ich gehe ins Kino.', 'Morgen gehe ich ins Kino.', 'Gehe ich morgen ins Kino.', 'C', 'Morgen is first, so gehe must be second.'),
        ],
    },
    {
        'title': 'Modal Verbs',
        'slug': 'modal-verbs',
        'cefr_level': 'A2',
        'summary': 'Use koennen, muessen, wollen, sollen, duerfen, and moegen with an infinitive.',
        'explanation': 'Modal verbs change the meaning of another verb. In a main clause, the modal verb is conjugated in second position and the main verb goes to the end in the infinitive form.',
        'examples': 'Ich kann Deutsch sprechen.\nWir muessen heute lernen.\nSie will ein Buch lesen.',
        'order': 4,
        'exercises': [
            ('Ich ___ morgen arbeiten.', 'kann', 'koennen', 'kannst', 'koennt', 'A', 'With ich, the modal verb is kann.'),
            ('Choose the correct word order.', 'Ich muss lernen heute.', 'Ich lernen muss heute.', 'Ich muss heute lernen.', 'Muss ich lernen heute.', 'C', 'The modal verb is second and the infinitive goes to the end.'),
        ],
    },
    {
        'title': 'Dative Case',
        'slug': 'dative-case',
        'cefr_level': 'A2',
        'summary': 'Use the dative for indirect objects and after common dative prepositions.',
        'explanation': 'The dative often marks the indirect object: the person receiving or benefiting from something. It is also used after prepositions like mit, nach, bei, seit, von, and zu. Articles change: der becomes dem, die becomes der, das becomes dem, and plural die becomes den.',
        'examples': 'Ich gebe dem Mann ein Buch.\nSie spricht mit der Lehrerin.\nWir fahren zu den Freunden.',
        'order': 5,
        'exercises': [
            ('Ich helfe ___ Frau.', 'die', 'der', 'den', 'das', 'B', 'Helfen takes the dative; feminine die becomes der.'),
            ('Wir fahren mit ___ Zug.', 'der', 'den', 'dem', 'das', 'C', 'Mit takes the dative; masculine der becomes dem.'),
        ],
    },
    {
        'title': 'Separable Verbs',
        'slug': 'separable-verbs',
        'cefr_level': 'A2',
        'summary': 'Learn verbs whose prefix moves to the end in main clauses.',
        'explanation': 'Some German verbs have separable prefixes, such as aufstehen, einkaufen, and anrufen. In a main clause, the conjugated verb stem goes in second position and the prefix moves to the end.',
        'examples': 'Ich stehe um sieben Uhr auf.\nWir kaufen heute ein.\nEr ruft seine Mutter an.',
        'order': 6,
        'exercises': [
            ('Ich ___ um 7 Uhr ___.', 'stehe / auf', 'auf / stehe', 'stehen / auf', 'stehe / an', 'A', 'Aufstehen separates: ich stehe ... auf.'),
            ('Choose the correct sentence.', 'Sie ruft ihre Freundin an.', 'Sie anruft ihre Freundin.', 'Sie ruft an ihre Freundin.', 'An ruft sie ihre Freundin.', 'A', 'Anrufen separates, and the prefix an goes to the end.'),
        ],
    },
]


def seed_topics(apps, schema_editor):
    GrammarTopic = apps.get_model('grammar', 'GrammarTopic')
    GrammarExercise = apps.get_model('grammar', 'GrammarExercise')

    for topic_data in TOPICS:
        exercises = topic_data['exercises']
        defaults = {key: value for key, value in topic_data.items() if key != 'exercises'}
        topic, _ = GrammarTopic.objects.update_or_create(
            slug=topic_data['slug'],
            defaults=defaults,
        )
        for order, exercise in enumerate(exercises, start=1):
            prompt, option_a, option_b, option_c, option_d, correct_option, explanation = exercise
            GrammarExercise.objects.update_or_create(
                topic=topic,
                prompt=prompt,
                defaults={
                    'option_a': option_a,
                    'option_b': option_b,
                    'option_c': option_c,
                    'option_d': option_d,
                    'correct_option': correct_option,
                    'explanation': explanation,
                    'order': order,
                },
            )


def unseed_topics(apps, schema_editor):
    GrammarTopic = apps.get_model('grammar', 'GrammarTopic')
    GrammarTopic.objects.filter(slug__in=[topic['slug'] for topic in TOPICS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('grammar', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_topics, unseed_topics),
    ]
