"""
AI Service wrapper for Groq integration
"""
import os
from groq import Groq
from django.conf import settings


class GroqAIService:
    """Groq AI service for German language learning"""
    
    def __init__(self):
        api_key = os.environ.get('GROQ_API_KEY') or getattr(settings, 'GROQ_API_KEY', None)
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment or settings")
        self.client = Groq(api_key=api_key)
    
    def get_word_info(self, word):
        """
        Get word information from Groq AI
        Returns: structured word info or "not german"
        """
        prompt = """You are a German language expert. I will give you a word/phrase and you must first determine if it's German, then provide information.

CRITICAL RULES:
1. FIRST: Check if the input is actually a German word or phrase
2. If the input is NOT German (English, French, Spanish, gibberish, etc.), respond with EXACTLY: "not german"
3. If it IS German, normalize it to the correct vocabulary storage form along with translation and CEFR level
4. For German nouns: WORD must include the nominative article and noun, e.g. "der Tisch", "die Zeitung", "das Haus". If the user typed only "Haus", return "das Haus". If the user typed a plural noun, use "die" with the plural form.
5. For German verbs: WORD must be the infinitive/lemma, even if the user typed a conjugated, past tense, or participle form. If the user typed "ging", "gegangen", or "geht", return "gehen".
6. For adjectives: return the base adjective form (do NOT convert to noun form)
7. For adverbs and phrases: return the natural dictionary/storage form
8. Do NOT change the part of speech. Do not turn verbs into nouns, nouns into verbs, etc.
9. Provide accurate English translation for the normalized word type
10. Assign correct CEFR level (A1, A2, B1, B2, C1, C2)

FORMAT for German words:
WORD: <normalized vocabulary form>
TRANSLATION: <English translation>
CEFR: <A1/A2/B1/B2/C1/C2>
EXAMPLES:
1. <German example sentence> - <English translation>
2. <German example sentence> - <English translation>
VERB_FORMS:
If the word is not a verb, write exactly "not a verb" under this heading, then continue to NOUN_FORMS
If the word is a verb, respond with:
VERB: <infinitive form>
MEANING: <English translation>
TYPE: <regular/irregular/modal/separable>
PRESENT TENSE:
ich <form>
du <form>
er/sie/es <form>
wir <form>
ihr <form>
sie/Sie <form>
PAST TENSE (Präteritum):
ich <form>
du <form>
er/sie/es <form>
wir <form>
ihr <form>
sie/Sie <form>
PERFECT TENSE:
Past Participle: <ge- form>
Auxiliary: <haben/sein>
NOUN_FORMS:
If the word is not a noun, write exactly "not a noun" under this heading
If the word is a noun, respond with:
SINGULAR: <nominative singular with article, or none if no singular exists>
PLURAL: <nominative plural with article, or none if no plural exists>
MASCULINE: <masculine counterpart with article, or none if it does not exist>
FEMININE: <feminine counterpart with article, or none if it does not exist>

Here is the word/phrase to analyze:
"""
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt + word,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    
    def write_example(self, words):
        """Generate example sentences for words"""
        prompt = """Hi. I'm gonna send you a list of german words and you will give me exactly 2 short example sentences for each one of them, in german,
and then its translation in english. The format should be:
<german word>: <german example> - <english translation>
<german word>: <german example> - <english translation>
Keep each example on its own line.
Here is the list of words:
"""
        words_str = ' - '.join(words)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt + words_str,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    
    def write_paragraph(self, words):
        """Generate a paragraph using the words"""
        prompt = """Hi. I'm gonna send you a list of german words and you will write a paragraph using all of them, in german, 
and then its translation in english. the format should be like this:
<german paragraph> \n <english translation> 
Here is the list of words:
"""
        words_str = ' - '.join(words)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt + words_str,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    
    def get_verb_info(self, word):
        """Get verb conjugation information"""
        prompt = """You are a German language expert specializing in verb conjugation. I will give you a word and you must:

CRITICAL RULES:
1. FIRST: Check if the input is actually a German VERB
2. If the input is NOT a German verb (noun, adjective, English word, etc.), respond with EXACTLY: "not a verb"
3. If it IS a German verb, provide comprehensive conjugation information
4. The input may be infinitive, conjugated present, Präteritum, or past participle. Always identify the infinitive/lemma and use that in VERB.
5. Examples: "ging", "gegangen", and "geht" are verb forms of "gehen", so VERB must be "gehen".

FORMAT for non-verbs: not a verb
FORMAT for German verbs:
VERB: <infinitive form>
MEANING: <English translation>
TYPE: <regular/irregular/modal/separable>
PRESENT TENSE:
ich <form>
du <form>
er/sie/es <form>
wir <form>
ihr <form>
sie/Sie <form>
PAST TENSE (Präteritum):
ich <form>
du <form>
er/sie/es <form>
wir <form>
ihr <form>
sie/Sie <form>
PERFECT TENSE:
Past Participle: <ge- form>
Auxiliary: <haben/sein>

Examples:
- "Haus" → "not a verb" (noun)
- "schnell" → "not a verb" (adjective)
- "hello" → "not a verb" (English word)

For a verb like "gehen":
VERB: gehen
MEANING: to go
TYPE: irregular
PRESENT TENSE:
ich gehe
du gehst
er/sie/es geht
wir gehen
ihr geht
sie/Sie gehen
PAST TENSE (Präteritum):
ich ging
du gingst
er/sie/es ging
wir gingen
ihr gingt
sie/Sie gingen
PERFECT TENSE:
Past Participle: gegangen
Auxiliary: sein

Here is the word to analyze:
"""
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt + word,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
