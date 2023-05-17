import json
import logging
import os
import json
from bardapi import Bard
import traceback

# set your __Secure-1PSID value to key
# os.environ['_BARD_API_KEY']="XXXXXXXXXXXXXXXXXX"
# Write Prime numbers from 1 to 50 in C++

class BardCoder:
    global bard
    global logger
    logs_enabled = False
    # define member variables for response_id, conversation_id, content, factualityQueries, textQuery, choices
    response_id, conversation_id, content, factualityQueries, textQuery, choices = None, None, None, None, None, None
    
    def __init__(self, prompt, enable_logs=False):
        try:
            # Setting up Bard from BardAPI.
            self.bard = Bard(timeout=10)  # Set timeout in seconds

            # Enable logs
            if enable_logs:
                self.enable_logs()
            
            # Setups the logging.
            self.logger = self.setup_logger('bardcoder.log')
            self.add_log("Init Starting ...")
            self.add_log("Init: Prompt: " + prompt)
            
            # Get the response from the prompt.
            response = self.get_response(prompt)
            data = json.dumps(response, indent=4)
            json_data = json.loads(data)
            
            # Getting the data from the response.
            self.add_log("Init: Data: " + str(json_data))
            if data:
                self.content = json_data['content']
                
            # Saving the response to file.
            self.add_log("Init: Saving response to file.")
            self.save_file("response/response.json",json.dumps(response, indent=4))
            self.save_file("response/content.txt", self.content)
            
            # Getting the content from the response.
            self.add_log("Init: Content: " + self.content)
            self.conversation_id = json_data['conversation_id']
            
            # Getting the conversation ID from the response.
            self.add_log("Init: Conversation ID: " + self.conversation_id)
            self.response_id = json_data['response_id']
            self.add_log("Init: Response ID: " + self.response_id)
            
            # Get the factuality queries from the response.
            self.factualityQueries = json_data['factualityQueries']
            for factualityQuery in self.factualityQueries:
                self.add_log("Init: Factuality Query: " + str(factualityQuery))
            # Get the links from the response.    
            links = self.get_links(self.factualityQueries)
            self.add_log("Init: Links: " + str(links))

            # Get the text query from the response.
            self.textQuery = json_data['textQuery']
            self.add_log("Init: Text Query: " + str(self.textQuery))
            
            # Getting the choices from the response.
            self.choices = json_data['choices']
            for choice in self.choices:
                self.add_log("Init: Choice: " + str(choice))
        
        except Exception as e:
            # print stack trace
            stack_trace = traceback.format_exc()
            self.add_log(stack_trace)
            self.add_log(str(e))
            

    def get_response(self,prompt: str):
        if not prompt:
            self.add_log("get_response: Prompt is empty.")
            return ""

        response = self.bard.get_answer(prompt)

        # get response from bard
        return response

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

    def setup_logger(self, filename: str, level=logging.INFO):
        # Remove existing handlers from the root logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Set up a file handler to write logs to a file
        file_handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
        file_handler.setFormatter(formatter)
        logging.root.addHandler(file_handler)
        logging.root.setLevel(level)

        return logging.getLogger(__name__)

    def get_code(self):
        start_index = self.content.find('```')
        end_index = self.content.rfind('```')
        if start_index != -1 and end_index != -1:
            return self.content[start_index+3:end_index]
        else:
            return None

    def save_code(self, filename="codes/code.txt"):
        code = self.get_code()
        code = code.replace("\\n", "\n").replace("\\t", "\t")
        if code:
            with open(filename, 'w') as f:
                f.write(code)

    def save_code(self, filename="codes/code.txt", code=None):
        if code:
            code = code.replace("\\n", "\n").replace("\\t", "\t")
            with open(filename, 'w') as f:
                f.write(code)

    def save_code_choices(self, filename):
        self.add_log(f"save_code_choices: Saving code choices with filename: {filename}")
        for index, choice in enumerate(self.choices):
            choice_content = self.get_choice_content(index)
            self.save_code("codes/"+filename+'_'+str(index), choice_content)
    
    def run_code(self):
        code = self.get_code()
        if code:
            exec(code)
    
    def get_links(self, data):
        links = []
        print("Get links '", end='\n')
        print(data, end='\n')
        print("'", end='\n')
        if data is None:
            return links
        try:
            for inner_list in data[0]:
                link = inner_list[2][0]
                if link:
                    links.append(link)
        except Exception as e:
            self.add_log("Exception: " + str(e))
            return links
        return links

    def save_file(self, filename, data):
        with open(filename, 'w') as f:
            f.write(data)

    def read_file(self, filename):
        with open(filename, 'r') as f:
            return f.read()
    
    def add_log(self, log, level=logging.INFO):
        if self.logs_enabled:
            self.logger.log(level, log)
        else:
            self.logger = self.setup_logger('bardcoder.log')
            self.logger.log(level, log)
            
    def enable_logs(self):
        self.logs_enabled = True
