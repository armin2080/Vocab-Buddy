from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from words.models import UserWord, Word
from .models import PracticeMessage, PracticeSession
from .services import build_system_prompt, select_challenge_words
from .templatetags.practice_lab_format import practice_markdown


class StubPracticeAI:
    calls = []

    def continue_practice_conversation(self, messages):
        self.calls.append(messages)
        return 'Good start. Revise the second sentence.'


class PracticeMessageFormattingTests(SimpleTestCase):
    def test_renders_structured_markdown(self):
        rendered = str(practice_markdown(
            '## Overall Feedback\n'
            'A **strong** paragraph.\n\n'
            '## Improvements\n'
            '- Fix the article.\n'
            '- Use a more natural phrase.\n\n'
            '## Improved Version\n'
            '> Das ist die verbesserte Version.'
        ))

        self.assertIn('<h2>Overall Feedback</h2>', rendered)
        self.assertIn('<strong>strong</strong>', rendered)
        self.assertIn('<ul><li>Fix the article.</li>', rendered)
        self.assertIn('<blockquote>Das ist die verbesserte Version.</blockquote>', rendered)

    def test_escapes_model_html(self):
        rendered = str(practice_markdown(
            '## Feedback\n<script>alert("bad")</script> **safe**'
        ))

        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)
        self.assertIn('<strong>safe</strong>', rendered)

    def test_formats_legacy_colon_headings(self):
        rendered = str(practice_markdown(
            'Sehr gut gemacht!\n\n'
            'Ein paar kleine Vorschläge für Verbesserungen:\n'
            '- Nutze eine natürlichere Formulierung.'
        ))

        self.assertIn(
            '<h3>Ein paar kleine Vorschläge für Verbesserungen:</h3>',
            rendered,
        )
        self.assertIn('<ul><li>Nutze eine natürlichere Formulierung.</li>', rendered)

    def test_prompt_requests_consistent_markdown_sections(self):
        prompt = build_system_prompt([
            {'word': 'laufen', 'level': 'A1', 'translation': 'to run'},
        ])

        self.assertIn('## Overall Feedback', prompt)
        self.assertIn('## Challenge Words', prompt)
        self.assertIn('## Improved Version', prompt)
        self.assertIn('Do not wrap the response in a Markdown code block', prompt)


class PracticeLabTests(TestCase):
    def setUp(self):
        StubPracticeAI.calls = []
        self.user = User.objects.create_user(username='writer', password='test-password')
        self.other_user = User.objects.create_user(username='other', password='test-password')
        self.client.force_login(self.user)

        levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        for index, level in enumerate(levels):
            word = Word.objects.create(
                word=f'word-{level}',
                translation=f'translation-{level}',
                cefr_level=level,
            )
            UserWord.objects.create(
                user=self.user,
                word=word,
                review_count=index,
                correct_count=max(0, index - 2),
            )

    def test_selects_five_challenging_words(self):
        selected = select_challenge_words(self.user)

        self.assertEqual(len(selected), 5)
        self.assertEqual(selected[0]['level'], 'C2')
        self.assertNotIn('A1', [item['level'] for item in selected])

    def test_opening_lab_creates_and_reuses_active_session(self):
        first_response = self.client.get(reverse('practice_lab:lab'))
        practice_session = PracticeSession.objects.get(user=self.user)

        self.assertRedirects(
            first_response,
            reverse('practice_lab:session', kwargs={'pk': practice_session.pk}),
        )
        self.assertEqual(practice_session.messages.count(), 1)
        self.assertEqual(len(practice_session.challenge_words), 5)

        self.client.get(reverse('practice_lab:lab'))
        self.assertEqual(PracticeSession.objects.filter(user=self.user).count(), 1)

    @patch('practice_lab.views.GroqAIService', return_value=StubPracticeAI())
    def test_sends_full_conversation_history_to_groq(self, ai_service):
        self.client.get(reverse('practice_lab:lab'))
        practice_session = PracticeSession.objects.get(user=self.user)

        self.client.post(
            reverse('practice_lab:session', kwargs={'pk': practice_session.pk}),
            {'message': 'Mein erster Absatz.'},
        )
        self.client.post(
            reverse('practice_lab:session', kwargs={'pk': practice_session.pk}),
            {'message': 'Hier ist meine überarbeitete Version.'},
        )

        second_call = StubPracticeAI.calls[1]
        self.assertEqual([message['role'] for message in second_call], [
            'system',
            'assistant',
            'user',
            'assistant',
            'user',
        ])
        self.assertEqual(
            second_call[-2]['content'],
            'Good start. Revise the second sentence.',
        )

    def test_closing_session_deletes_chat_history(self):
        self.client.get(reverse('practice_lab:lab'))
        practice_session = PracticeSession.objects.get(user=self.user)
        message_ids = list(practice_session.messages.values_list('pk', flat=True))

        response = self.client.post(
            reverse('practice_lab:close_session', kwargs={'pk': practice_session.pk}),
        )

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(PracticeSession.objects.filter(pk=practice_session.pk).exists())
        self.assertFalse(PracticeMessage.objects.filter(pk__in=message_ids).exists())

    def test_other_user_cannot_open_or_close_session(self):
        self.client.get(reverse('practice_lab:lab'))
        practice_session = PracticeSession.objects.get(user=self.user)
        self.client.force_login(self.other_user)

        detail_response = self.client.get(
            reverse('practice_lab:session', kwargs={'pk': practice_session.pk}),
        )
        close_response = self.client.post(
            reverse('practice_lab:close_session', kwargs={'pk': practice_session.pk}),
        )

        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(close_response.status_code, 404)

    def test_lab_requires_five_words(self):
        UserWord.objects.filter(user=self.user).delete()

        response = self.client.get(reverse('practice_lab:lab'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practice_lab/not_ready.html')
        self.assertFalse(PracticeSession.objects.filter(user=self.user).exists())
