import os
import openai

openai.organization = "org-epKTu2qzLA0v2BTC1IOufKNt"
openai.api_key = os.getenv("OPENAI_API_KEY")

filename = "ChatHistory.txt"


class ChatBot:
    def __init__(self):
        self.currentPrompt = ""

    def write_to_file(self, filename, chatHistory):
        mode = 'a' if os.path.exists(filename) else 'w'
        with open(filename, mode) as file:
            file.write("\nChat History: "+ chatHistory)

    def read_from_file(self, filename):
        if not os.path.exists(filename):
            return ""
        with open(filename, 'r') as file:
            return file.read()

    def execute_prompt(self, input_prompt, history=""):
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt= history + input_prompt,
            temperature=0,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["--", ";", "/*", "*/"]
        )

        answer = response.choices[0].text.strip()
        return answer

    def get_entity_and_columns(self, headers):

        return a

