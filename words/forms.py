from django import forms
from django.core.exceptions import ValidationError
from ai_service import GroqAIService
from .models import Word


class EditWordForm(forms.ModelForm):
    """Edit stored vocabulary metadata."""

    class Meta:
        model = Word
        fields = [
            'word',
            'translation',
            'cefr_level',
            'example_sentences',
            'context_paragraph',
            'is_noun',
            'singular_form',
            'plural_form',
            'masculine_form',
            'feminine_form',
            'is_verb',
            'verb_forms',
        ]
        widgets = {
            'translation': forms.Textarea(attrs={'rows': 2}),
            'example_sentences': forms.Textarea(attrs={'rows': 4}),
            'context_paragraph': forms.Textarea(attrs={'rows': 5}),
            'verb_forms': forms.Textarea(attrs={'rows': 12}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                'w-full rounded-md border border-gray-300 px-3 py-2 '
                'focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500'
            )
        for name in ('is_noun', 'is_verb'):
            self.fields[name].widget.attrs['class'] = 'h-4 w-4 rounded border-gray-300'


class AddWordForm(forms.Form):
    """Form to add a new German word"""
    
    word = forms.CharField(
        label='German Word',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a German word or phrase',
            'autofocus': True,
        })
    )
    
    def clean_word(self):
        word_input = self.cleaned_data['word'].strip()

        def parse_word_response(ai_response):
            lines = [line.rstrip() for line in ai_response.splitlines()]
            word = ''
            translation = ''
            cefr_level = ''
            examples = []
            verb_forms_lines = []
            noun_forms = {}
            section = None

            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    continue
                if line.startswith('WORD:'):
                    word = line.split(':', 1)[1].strip()
                    section = None
                    continue
                if line.startswith('TRANSLATION:'):
                    translation = line.split(':', 1)[1].strip()
                    section = None
                    continue
                if line.startswith('CEFR:'):
                    cefr_level = line.split(':', 1)[1].strip()
                    section = None
                    continue
                if line.startswith('EXAMPLES:'):
                    section = 'examples'
                    continue
                if line.startswith('VERB_FORMS:'):
                    section = 'verb_forms'
                    continue
                if line.startswith('NOUN_FORMS:'):
                    section = 'noun_forms'
                    continue

                if section == 'examples':
                    examples.append(line.lstrip('0123456789. ').strip())
                elif section == 'verb_forms':
                    verb_forms_lines.append(raw_line.rstrip())
                elif section == 'noun_forms' and ':' in line:
                    key, value = line.split(':', 1)
                    noun_forms[key.strip().lower()] = value.strip()

            valid_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
            if not word or not translation or cefr_level not in valid_levels:
                raise ValueError('Invalid response format')

            verb_forms_text = '\n'.join([line for line in verb_forms_lines if line]).strip()
            parsed_verb_forms = '' if verb_forms_text.lower() == 'not a verb' else verb_forms_text
            verb_lemma, verb_meaning = extract_verb_metadata(parsed_verb_forms)
            clean_noun_form = lambda value: '' if value.lower() in {'', 'none', 'n/a', 'not applicable'} else value
            singular_form = clean_noun_form(noun_forms.get('singular', ''))
            plural_form = clean_noun_form(noun_forms.get('plural', ''))
            masculine_form = clean_noun_form(noun_forms.get('masculine', ''))
            feminine_form = clean_noun_form(noun_forms.get('feminine', ''))

            return {
                'parsed_word': verb_lemma or word,
                'parsed_translation': verb_meaning or translation,
                'parsed_cefr_level': cefr_level,
                'parsed_example_sentences': '\n'.join([line for line in examples if line][:2]),
                'parsed_verb_forms': parsed_verb_forms,
                'parsed_is_verb': bool(parsed_verb_forms),
                'parsed_is_noun': bool(singular_form or plural_form),
                'parsed_singular_form': singular_form,
                'parsed_plural_form': plural_form,
                'parsed_masculine_form': masculine_form,
                'parsed_feminine_form': feminine_form,
            }

        def extract_verb_metadata(verb_forms_text):
            verb = ''
            meaning = ''
            for raw_line in (verb_forms_text or '').splitlines():
                line = raw_line.strip()
                if line.startswith('VERB:'):
                    verb = line.split(':', 1)[1].strip()
                elif line.startswith('MEANING:'):
                    meaning = line.split(':', 1)[1].strip()
            return verb, meaning

        def parse_verb_response(ai_response):
            lines = [line.rstrip() for line in ai_response.splitlines()]
            verb_forms_lines = []
            section = None

            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    continue
                if line.startswith('VERB:'):
                    section = 'verb_forms'
                elif line.startswith('MEANING:'):
                    section = 'verb_forms'
                elif line.startswith('TYPE:'):
                    section = 'verb_forms'
                elif line.startswith('PRESENT TENSE:'):
                    section = 'verb_forms'
                elif line.startswith('PAST TENSE'):
                    section = 'verb_forms'
                elif line.startswith('PERFECT TENSE:'):
                    section = 'verb_forms'

                if section == 'verb_forms':
                    verb_forms_lines.append(raw_line.rstrip())

            verb_forms_text = '\n'.join([line for line in verb_forms_lines if line]).strip()
            if not verb_forms_text or verb_forms_text.lower() == 'not a verb':
                return ''
            return verb_forms_text
        
        if not word_input:
            raise ValidationError('Please enter a German word.')
        
        # Validate with Groq AI
        try:
            ai_service = GroqAIService()
            ai_response = ai_service.get_word_info(word_input)
            
            if ai_response.strip().lower() == 'not german':
                raise ValidationError(
                    f'"{word_input}" does not appear to be a German word. '
                    'Please enter a valid German word or phrase.'
                )
            try:
                parsed = parse_word_response(ai_response)
                self.cleaned_data.update(parsed)

                if not self.cleaned_data['parsed_is_verb']:
                    verb_info_response = ai_service.get_verb_info(word_input)
                    parsed_verb_forms = parse_verb_response(verb_info_response)
                    if parsed_verb_forms:
                        verb_lemma, verb_meaning = extract_verb_metadata(parsed_verb_forms)
                        if verb_lemma:
                            self.cleaned_data['parsed_word'] = verb_lemma
                        if verb_meaning:
                            self.cleaned_data['parsed_translation'] = verb_meaning
                        self.cleaned_data['parsed_verb_forms'] = parsed_verb_forms
                        self.cleaned_data['parsed_is_verb'] = True

            except (ValueError, AttributeError):
                raise ValidationError(
                    'Could not parse word information. Please try another word.'
                )
        except Exception as e:
            raise ValidationError(
                f'Error validating word: {str(e)} Please try again.'
            )
        
        return word_input
