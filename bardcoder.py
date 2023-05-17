import json
import os
import logging

class BardCoder:    
    logger = None
    def __init__(self, json_data):
        logger = self.setup_logger('bardcoder.log')
        logger.info("Init Starting ...")
        data = json.loads(json_data)
        logger.info("Init: Data: " + json_data)
        self.content = data['content']
        logger.info("Init: Content: " + self.content)
        self.conversation_id = data['conversation_id']
        logger.info("Init: Conversation ID: " + self.conversation_id)
        self.response_id = data['response_id']
        logger.info("Init: Response ID: " + self.response_id)
        self.factualityQueries = data['factualityQueries']
        for factualityQuery in self.factualityQueries:
            logger.info("Init: Factuality Query: " + str(factualityQuery))
        
        self.textQuery = data['textQuery']
        logger.info("Init: Text Query: " + str(self.textQuery))
        self.choices = data['choices']
        for choice in self.choices:
            logger.info("Init: Choice: " + str(choice))

    def get_choice_content(self, index):
        if index < len(self.choices):
            choice_content = self.choices[index]['content'][0]
            start_index = choice_content.find('```')
            end_index = choice_content.rfind('```')
            if start_index != -1 and end_index != -1:
                return choice_content[start_index+3:end_index]
            else:
                return None
        else:
            return None

        
    def setup_logger(self, filename:str, level=logging.INFO):
        # Remove existing handlers from the root logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Set up a file handler to write logs to a file
        file_handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        file_handler.setFormatter(formatter)
        logging.root.addHandler(file_handler)
        logging.root.setLevel(level)

        return logging.getLogger(__name__)
        
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
    
    def save_code(self, filename, code):
        if code:
            with open(filename, 'w') as f:
                f.write(code)

    def run_code(self):
        code = self.get_content()
        if code:
            exec(code)
