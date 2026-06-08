from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import AddWordForm
from .models import UserWord, Word


NOUN_RESPONSE = """WORD: die Lehrerin
TRANSLATION: teacher
CEFR: A1
EXAMPLES:
1. Die Lehrerin erklärt die Aufgabe. - The teacher explains the task.
2. Ich spreche mit der Lehrerin. - I speak with the teacher.
VERB_FORMS:
not a verb
NOUN_FORMS:
SINGULAR: die Lehrerin
PLURAL: die Lehrerinnen
MASCULINE: der Lehrer
FEMININE: die Lehrerin
"""


class StubAIService:
    def get_word_info(self, word):
        return NOUN_RESPONSE

    def get_verb_info(self, word):
        return 'not a verb'


class AddWordFormTests(TestCase):
    @patch('words.forms.GroqAIService', return_value=StubAIService())
    def test_parses_noun_forms(self, ai_service):
        form = AddWordForm({'word': 'Lehrerin'})

        self.assertTrue(form.is_valid(), form.errors)
        self.assertTrue(form.cleaned_data['parsed_is_noun'])
        self.assertFalse(form.cleaned_data['parsed_is_verb'])
        self.assertEqual(form.cleaned_data['parsed_singular_form'], 'die Lehrerin')
        self.assertEqual(form.cleaned_data['parsed_plural_form'], 'die Lehrerinnen')
        self.assertEqual(form.cleaned_data['parsed_masculine_form'], 'der Lehrer')
        self.assertEqual(form.cleaned_data['parsed_feminine_form'], 'die Lehrerin')


class NounFormsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='learner', password='test-password')
        self.client.force_login(self.user)

    @patch('words.forms.GroqAIService', return_value=StubAIService())
    def test_add_word_persists_and_displays_noun_forms(self, ai_service):
        response = self.client.post(reverse('words:add_word'), {'word': 'Lehrerin'})

        self.assertEqual(response.status_code, 302)
        word = Word.objects.get(word='die Lehrerin')
        self.assertTrue(word.is_noun)
        self.assertEqual(word.plural_form, 'die Lehrerinnen')
        self.assertEqual(word.masculine_form, 'der Lehrer')

        list_response = self.client.get(reverse('words:word_list'))
        self.assertContains(list_response, 'die Lehrerinnen')
        self.assertContains(list_response, 'der Lehrer')

    def test_review_payload_contains_noun_forms(self):
        word = Word.objects.create(
            word='das Haus',
            translation='house',
            cefr_level='A1',
            is_noun=True,
            singular_form='das Haus',
            plural_form='die Häuser',
        )
        UserWord.objects.create(user=self.user, word=word)

        response = self.client.get(reverse('learning:review_start'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['cards'][0]['is_noun'])
        self.assertEqual(
            response.context['cards'][0]['noun_forms_data']['plural'],
            'die Häuser',
        )


class WordManagementViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='editor', password='test-password')
        self.other_user = User.objects.create_user(username='other', password='test-password')
        self.word = Word.objects.create(
            word='Lehrerin',
            translation='old translation',
            cefr_level='A2',
        )
        self.user_word = UserWord.objects.create(user=self.user, word=self.word)
        self.client.force_login(self.user)

    def test_vocabulary_tile_links_to_detail_page(self):
        response = self.client.get(reverse('words:word_list'))

        self.assertContains(
            response,
            reverse('words:word_detail', kwargs={'pk': self.user_word.pk}),
        )

    def test_edit_word_updates_fields(self):
        response = self.client.post(
            reverse('words:edit_word', kwargs={'pk': self.user_word.pk}),
            {
                'word': 'die Lehrerin',
                'translation': 'teacher',
                'cefr_level': 'A1',
                'example_sentences': 'Die Lehrerin hilft. - The teacher helps.',
                'context_paragraph': '',
                'is_noun': 'on',
                'singular_form': 'die Lehrerin',
                'plural_form': 'die Lehrerinnen',
                'masculine_form': 'der Lehrer',
                'feminine_form': 'die Lehrerin',
                'verb_forms': '',
            },
        )

        self.assertRedirects(
            response,
            reverse('words:word_detail', kwargs={'pk': self.user_word.pk}),
        )
        self.word.refresh_from_db()
        self.assertEqual(self.word.word, 'die Lehrerin')
        self.assertEqual(self.word.translation, 'teacher')
        self.assertEqual(self.word.plural_form, 'die Lehrerinnen')

    @patch('words.forms.GroqAIService', return_value=StubAIService())
    def test_refresh_word_replaces_missing_metadata(self, ai_service):
        response = self.client.post(
            reverse('words:refresh_word', kwargs={'pk': self.user_word.pk}),
        )

        self.assertRedirects(
            response,
            reverse('words:word_detail', kwargs={'pk': self.user_word.pk}),
        )
        self.word.refresh_from_db()
        self.assertTrue(self.word.is_noun)
        self.assertEqual(self.word.translation, 'teacher')
        self.assertEqual(self.word.plural_form, 'die Lehrerinnen')

    def test_refresh_requires_post(self):
        response = self.client.get(
            reverse('words:refresh_word', kwargs={'pk': self.user_word.pk}),
        )

        self.assertEqual(response.status_code, 405)

    def test_other_users_cannot_manage_word(self):
        other_user_word = UserWord.objects.create(user=self.other_user, word=self.word)

        for route in ('word_detail', 'edit_word', 'refresh_word', 'delete_word'):
            url = reverse(f'words:{route}', kwargs={'pk': other_user_word.pk})
            response = self.client.post(url) if route in {'refresh_word', 'delete_word'} else self.client.get(url)
            self.assertEqual(response.status_code, 404)

    def test_delete_removes_word_from_users_vocabulary(self):
        response = self.client.post(
            reverse('words:delete_word', kwargs={'pk': self.user_word.pk}),
        )

        self.assertRedirects(response, reverse('words:word_list') + f'?refresh={response.url.split("=")[-1]}')
        self.assertFalse(UserWord.objects.filter(pk=self.user_word.pk).exists())
