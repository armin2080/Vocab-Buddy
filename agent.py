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
                    Hi. I'm gonna send you a german word and you will tell me its complete notation(only if it's a name, also include the article, otherwise just write the verb itself), its translation, and on which CEFR level it is(make sure you choose correct level for it, not simpler or more complex than its actual level). 
                    just give me these three. your answer should be in this structure, nothing else; <complete word> - <english translation> - <CEFR level> 
                    Here is the word:
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







if __name__ == "__main__":
    groq_client = GroqClient()
    word = ['Haus', 'Auto', 'Baum', 'Hund', 'Katze']
    # info = groq_client.get_word_info(word[0])
    examples = groq_client.write_example(word)
    par = groq_client.write_paragraph(word)
    print(par)