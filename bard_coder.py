import json
import os

class BardCoder:
    def __init__(self, json_data):
        data = json.loads(json_data)
        self.content = data['content']
        self.conversation_id = data['conversation_id']
        self.response_id = data['response_id']
        self.factualityQueries = data['factualityQueries']
        self.textQuery = data['textQuery']
        self.choices = data['choices']

    def get_content(self):
        start_index = self.content.find('```')
        end_index = self.content.rfind('```')
        if start_index != -1 and end_index != -1:
            return self.content[start_index+3:end_index]
        else:
            return None

    def save_code(self, filename):
        code = self.get_content()
        if code:
            with open(filename, 'w') as f:
                f.write(code)

    def run_code(self):
        code = self.get_content()
        if code:
            exec(code)
