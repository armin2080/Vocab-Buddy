from groq import Groq
import json, os


class GroqClient:
    def __init__(self):
        with open("config.json", "r") as f:
            config = json.load(f)
        self.api_key = config["AI_TOKEN"]
        
        self.client = Groq(api_key=self.api_key)
        self.text = ""
    
    
    def get_word_info(self, word):
        self.text = """
                    You are a German language expert. I will give you a word/phrase and you must first determine if it's German, then provide information.

                    CRITICAL RULES:
                    1. FIRST: Check if the input is actually a German word or phrase
                    2. If the input is NOT German (English, French, Spanish, gibberish, etc.), respond with EXACTLY: "not german"
                    3. If it IS German, return the word in its EXACT original form along with translation and CEFR level
                    4. For German words: Return the word in its EXACT original form - do NOT change it from adjective to noun, verb to noun, etc.
                    5. If it's a noun, include the article (der/die/das)
                    6. If it's a verb, return it in infinitive form as given
                    7. If it's an adjective, return it exactly as the adjective (do NOT convert to noun form)
                    8. If it's an adverb, return it exactly as the adverb
                    9. Provide accurate English translation for the word type given
                    10. Assign correct CEFR level (A1, A2, B1, B2, C1, C2)

                    FORMAT for German words: <exact word as given> - <English translation> - <CEFR level>
                    FORMAT for non-German: not german

                    Examples:
                    - "hello" → "not german" (English word)
                    - "bonjour" → "not german" (French word)
                    - "xyz123" → "not german" (gibberish)
                    - "schnell" → "schnell - fast/quick - A2" (German adjective)
                    - "Haus" → "das Haus - the house - A1" (German noun with article - if it does not have an article, make sure to add it)
                    - "laufen" → "laufen - to run - A2" (German verb in infinitive)
                    
                    Here is the word/phrase to analyze:
                    """
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.text + word,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    
    def write_example(self,words=[]):
        self.text = """
                    Hi. I'm gonna send you a list of german words and you will give me an example sentence for each one of them, in german, 
                    and then its translation in english. the format should be like this:
                    <german word>: <german example> - <english translation> (each word should be on a new line) 
                    Here is the list of words:
                    """
        words = ' - '.join(words)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.text + words,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    
    def write_paragraph(self, words=[]):
        self.text = """
                    Hi. I'm gonna send you a list of german words and you will write a paragraph using all of them, in german, 
                    and then its translation in english. the format should be like this:
                    <german paragraph> \n <english translation> 
                    Here is the list of words:
                    """
        words = ' - '.join(words)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.text + words,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    

    def get_verb_info(self, word):
        self.text = """
                    You are a German language expert specializing in verb conjugation. I will give you a word and you must:

                    CRITICAL RULES:
                    1. FIRST: Check if the input is actually a German VERB
                    2. If the input is NOT a German verb (noun, adjective, English word, etc.), respond with EXACTLY: "not a verb"
                    3. If it IS a German verb, provide comprehensive conjugation information

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
                    "content": self.text + word,
                },
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content









if __name__ == "__main__":
    groq_client = GroqClient()
    word = ['Haus', 'Auto', 'Baum', 'Hund', 'Katze']
    
    # Test verb analysis
    test_verbs = ['gehen', 'haben', 'Haus', 'schnell', 'lernen']
    
    print("=== VERB ANALYSIS TESTS ===")
    for test_word in test_verbs:
        print(f"\nTesting: {test_word}")
        print("-" * 40)
        verb_info = groq_client.get_verb_info(test_word)
        print(verb_info)
        print("-" * 40)
    
    # Original examples and paragraph generation
    # info = groq_client.get_word_info(word[0])
    examples = groq_client.write_example(word)
    par = groq_client.write_paragraph(word)
    print(par)