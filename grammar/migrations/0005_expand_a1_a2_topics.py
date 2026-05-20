from django.db import migrations


TOPICS = [
    {
        'title': 'Personal Pronouns',
        'slug': 'personal-pronouns',
        'cefr_level': 'A1',
        'summary': 'Use ich, du, er, sie, es, wir, ihr, and sie/Sie as sentence subjects.',
        'explanation': 'Personal pronouns replace nouns and show who is doing the action. German distinguishes informal du and ihr from formal Sie. The verb ending changes with the subject, so the pronoun and verb must agree.',
        'examples': 'Ich lerne Deutsch. - I am learning German.\nDu kommst aus Berlin. - You come from Berlin.\nSie wohnt in Hamburg. - She lives in Hamburg.',
        'order': 7,
        'exercises': [
            ('___ bin Student.', 'Ich', 'Du', 'Er', 'Wir', 'A', 'Bin is the ich form of sein.'),
            ('___ seid heute sehr frueh.', 'Wir', 'Ihr', 'Sie', 'Ich', 'B', 'Seid is used with ihr.'),
            ('___ kommen aus Deutschland. (formal)', 'du', 'ihr', 'Sie', 'er', 'C', 'Formal you is Sie and takes the plural verb form.'),
        ],
    },
    {
        'title': 'Present Tense Verb Endings',
        'slug': 'present-tense-verb-endings',
        'cefr_level': 'A1',
        'summary': 'Match regular present-tense verbs with the right subject ending.',
        'explanation': 'Most German verbs in the present tense use a stem plus an ending: ich -e, du -st, er/sie/es -t, wir -en, ihr -t, sie/Sie -en. Some common verbs are irregular, but this pattern is the base for many verbs.',
        'examples': 'ich mache - I do\nDu lernst Deutsch. - You learn German.\nWir spielen Fussball. - We play football.',
        'order': 8,
        'exercises': [
            ('Ich ___ Deutsch.', 'lerne', 'lernst', 'lernt', 'lernen', 'A', 'Ich uses the -e ending: lerne.'),
            ('Du ___ Musik.', 'hoere', 'hoerst', 'hoert', 'hoeren', 'B', 'Du usually uses the -st ending: hoerst.'),
            ('Wir ___ im Park.', 'spiele', 'spielst', 'spielt', 'spielen', 'D', 'Wir uses the infinitive-like -en ending: spielen.'),
        ],
    },
    {
        'title': 'Negation: nicht and kein',
        'slug': 'nicht-kein',
        'cefr_level': 'A1',
        'summary': 'Choose nicht for verbs/adjectives and kein for nouns with no article or indefinite article.',
        'explanation': 'Use nicht to negate verbs, adjectives, adverbs, or a whole idea. Use kein to negate nouns that would use ein/eine or no article. Kein changes like an article: kein Mann, keine Frau, kein Buch.',
        'examples': 'Ich komme nicht. - I am not coming.\nDas ist kein Problem. - That is not a problem.\nSie hat keine Zeit. - She has no time.',
        'order': 9,
        'exercises': [
            ('Ich habe ___ Auto.', 'nicht', 'kein', 'keinen', 'keine', 'B', 'Auto is neuter and would be ein Auto, so use kein Auto.'),
            ('Sie ist ___ muede.', 'kein', 'keine', 'nicht', 'keinen', 'C', 'Muede is an adjective, so use nicht.'),
            ('Er trinkt ___ Kaffee.', 'nicht', 'keinen', 'kein', 'keine', 'B', 'Kaffee is masculine accusative here, so kein becomes keinen.'),
        ],
    },
    {
        'title': 'Possessive Articles',
        'slug': 'possessive-articles',
        'cefr_level': 'A2',
        'summary': 'Use mein, dein, sein, ihr, unser, euer, and Ihr to show ownership.',
        'explanation': 'Possessive articles behave like ein-words. Their ending depends on the noun gender, number, and case. In the nominative: mein Vater, meine Mutter, mein Kind, meine Freunde.',
        'examples': 'Das ist mein Bruder. - That is my brother.\nIst das deine Tasche? - Is that your bag?\nUnsere Freunde kommen heute. - Our friends are coming today.',
        'order': 10,
        'exercises': [
            ('Das ist ___ Mutter.', 'mein', 'meine', 'meinen', 'meinem', 'B', 'Mutter is feminine nominative, so use meine.'),
            ('Ich sehe ___ Bruder.', 'dein', 'deine', 'deinen', 'deinem', 'C', 'Bruder is masculine accusative, so dein becomes deinen.'),
            ('___ Freunde wohnen in Koeln.', 'Unser', 'Unsere', 'Unseren', 'Unserem', 'B', 'Freunde is plural nominative, so use unsere.'),
        ],
    },
    {
        'title': 'Perfect Tense',
        'slug': 'perfect-tense',
        'cefr_level': 'A2',
        'summary': 'Talk about the past with haben or sein plus a past participle.',
        'explanation': 'The perfect tense is common in spoken German. Use a conjugated form of haben or sein in second position, and put the past participle at the end. Many movement/change-of-state verbs use sein; most other verbs use haben.',
        'examples': 'Ich habe Kaffee getrunken. - I drank coffee.\nWir sind nach Hause gegangen. - We went home.\nSie hat Deutsch gelernt. - She learned German.',
        'order': 11,
        'exercises': [
            ('Ich ___ gestern Deutsch gelernt.', 'bin', 'habe', 'hat', 'war', 'B', 'Lernen usually forms the perfect with haben.'),
            ('Wir ___ nach Berlin gefahren.', 'haben', 'hat', 'sind', 'seid', 'C', 'Fahren as movement usually forms the perfect with sein.'),
            ('Choose the correct word order.', 'Ich habe gemacht die Hausaufgaben.', 'Ich gemacht habe die Hausaufgaben.', 'Ich habe die Hausaufgaben gemacht.', 'Ich die Hausaufgaben gemacht habe.', 'C', 'The auxiliary is second and the participle goes to the end.'),
        ],
    },
    {
        'title': 'Two-Way Prepositions',
        'slug': 'two-way-prepositions',
        'cefr_level': 'A2',
        'summary': 'Use accusative for direction and dative for location after common two-way prepositions.',
        'explanation': 'Prepositions like in, an, auf, unter, ueber, vor, hinter, neben, and zwischen can take accusative or dative. Use accusative for movement toward a place. Use dative for position in a place.',
        'examples': 'Ich gehe in die Schule. - I go into/to the school.\nIch bin in der Schule. - I am in school.\nDas Buch liegt auf dem Tisch. - The book is on the table.',
        'order': 12,
        'exercises': [
            ('Ich gehe in ___ Park.', 'der', 'den', 'dem', 'des', 'B', 'Movement toward a masculine place uses accusative: den Park.'),
            ('Ich bin in ___ Schule.', 'die', 'der', 'den', 'das', 'B', 'Location uses dative; feminine die becomes der.'),
            ('Das Handy liegt auf ___ Tisch.', 'der', 'den', 'dem', 'die', 'C', 'Location uses dative; masculine der becomes dem.'),
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
        ('grammar', '0004_grammarcoachentry'),
    ]

    operations = [
        migrations.RunPython(seed_topics, unseed_topics),
    ]
