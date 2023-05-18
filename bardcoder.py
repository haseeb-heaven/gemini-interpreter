import json
import logging
import os
import json
from bardapi import Bard
import traceback

# set your __Secure-1PSID value to key
# os.environ['_BARD_API_KEY']="XXXXXXXXXXXXXXXXXX"

"""
Factorial of number using recursion in C++  only code no explanations.
Sum of all numbers from 1 to 100  only code no explanations. in Java  only code no explanations.
Prime numbers from 10 to 20  only code no explanations. in Go lang  only code no explanations.
Floyds triangle using for loop only code no explanations. in Swift  only code no explanations.
Sum of all even numbers only code no explanations. in Python  only code no explanations.
Find string or int is palindrome in Rust  only code no explanations.
Write Fibonacci series from 1 to 100 in C++  only code no explanations.
Calculate the power of a number using recursion in Python only code no explanations.
Find the maximum and minimum element in an array using C++ only code no explanations.
"""


class BardCoder:
    global bard
    global logger
    logs_enabled = False
    # define member variables for response_id, conversation_id, content, factualityQueries, textQuery, choices
    response_id, conversation_id, content, factuality_queries, text_query, code_choices = None, None, None, None, None, None

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
            self.add_log(f"Init: Prompt: {prompt}")

            # Get the response from the prompt.
            response = self.get_response(prompt)
            if response:
                # self.add_log(f"Init: Response: {response}")
                data = json.dumps(response, indent=4)

                if data:
                    # self.add_log(f"Init: Data: {data}")

                    # Getting the data from the response.
                    json_data = json.loads(data)
                    if json_data:
                        self.content = json_data['content']
                        self.add_log("Init: Content: " + self.content)

                        # Saving the response to file.
                        self.add_log("Init: Saving response to file.")
                        self.save_file("response/response.json",
                                       json.dumps(response, indent=4))
                        self.save_file("response/content.md", self.content)

                        # Getting the content from the response.
                        self.conversation_id = json_data['conversation_id']
                        if self.conversation_id:
                            self.add_log(
                                f"Init: Conversation ID: {self.conversation_id}")

                        # Getting the conversation ID from the response.
                        self.response_id = json_data['response_id']
                        if self.response_id:
                            self.add_log(
                                f"Init: Response ID: {self.response_id}")

                        # Get the factuality queries from the response.
                        self.factuality_queries = json_data['factualityQueries']
                        if self.factuality_queries:
                            for factualityQuery in self.factuality_queries:
                                self.add_log(
                                    f"Init: Factuality Query: {factualityQuery}")
                            # Get the links from the response.
                            links = self.get_links()
                            self.add_log(f"Init: Links: {links}")

                        # Get the text query from the response.
                        self.text_query = json_data['textQuery']
                        if self.text_query:
                            self.add_log(
                                f"Init: Text Query: {self.text_query}")

                        # Getting the code choices from the response.
                        self.code_choices = json_data['choices']
                        self.add_log(
                            f"Init: Code Choices: {self.code_choices}")
                        if self.code_choices:
                            for code_choice in self.code_choices:
                                self.add_log(
                                    f"Init: Code Choice: {code_choice}")

                        # Mark end of init. - Success
                        self.add_log("Init: Success.")
                    else:
                        self.add_log("Init: Json data is empty.")
                else:
                    self.add_log("Init: Data is empty.")

        except Exception as e:
            # print stack trace
            stack_trace = traceback.format_exc()
            self.add_log(stack_trace)
            self.add_log(str(e))

    def get_response(self, prompt: str):
        if not prompt:
            self.add_log("get_response: Prompt is empty.")
            return ""

        response = self.bard.get_answer(prompt)

        # get response from bard
        return response

    def get_code_choice(self, index):
        if index < len(self.code_choices):
            choice_content = self.code_choices[index]['content'][0]
            start_index = choice_content.find('```') + 3
            end_index = choice_content.find('```', start_index)
            if start_index != -1 and end_index != -1:
                extracted_data = choice_content[start_index:end_index]
                result = extracted_data.strip()
                # Remove the code language identifier
                result = result[result.find('\n') + 1:]
                return result
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
        formatter = logging.Formatter(
            '%(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
        file_handler.setFormatter(formatter)
        logging.root.addHandler(file_handler)
        logging.root.setLevel(level)

        return logging.getLogger(__name__)

    def get_code(self):
        if self.content:
            self.add_log("get_code: Getting code from content.")
            data = self.content
            start_index = data.find("```") + 3
            end_index = data.find("```", start_index)
            extracted_data = data[start_index:end_index]
            result = extracted_data.strip()
            # Remove the code language identifier
            result = result[result.find('\n') + 1:]
            self.add_log(f"get_code: Code: {result}")
            return result

    def get_codey(self):
        if self.content:
            self.add_log("get_code: Getting code from content.")
            data = self.content
            start_index = data.find("```") + 3
            end_index = data.find("```", start_index)
            extracted_data = data[start_index:end_index]
            result = extracted_data.strip()
            self.add_log(f"get_code: Code: {result}")
            return result

    def save_code(self, filename="code.txt"):
        code = self.get_code()
        code_extenstion = '.' + self.get_code_extension()
        if code:
            code = code.replace("\\n", "\n").replace("\\t", "\t")
            self.add_log(
                f"save_code: Saving code with filename: {filename} and extension: {code_extenstion} and code: {code}")

            # Add extension to filename
            filename = filename + code_extenstion

            with open(filename, 'w') as f:
                f.write(code)
                self.add_log(f"save_code {filename} saved.")

    def save_code(self, filename="code.txt", code='print("Hello World")'):
        self.add_log(f"save_code: Saving code with filename: {filename}")

        code_extenstion = '.' + self.get_code_extension()
        code = self.get_code()
        if code:
            code = code.replace("\\n", "\n").replace("\\t", "\t")
            self.add_log(
                f"save_code: Saving code with filename: {filename} and extension: {code_extenstion} and code: {code}")

            # Add extension to filename
            filename = filename + code_extenstion

            with open(filename, 'w') as f:
                f.write(code)
                self.add_log(f"save_code {filename} saved.")

    def save_code_choices(self, filename):
        self.add_log(
            f"save_code_choices: Saving code choices with filename: {filename}")
        code_extension = '.' + self.get_code_extension()

        for index, choice in enumerate(self.code_choices):
            choice_content = self.get_code_choice(index)
            self.add_log(
                f"save_code_choices: Enumurated Choice content: {choice}")
            self.save_file("codes/"+filename+'_'+str(index+1) +
                           code_extension, choice_content)

    def run_code(self):
        code = self.get_code()
        if code:
            exec(code)

    def get_code_extension(self):
        code_content = self.content
        code_extension = ""
        if code_content:
            code_extension = code_content.split('```')[1].split('\n')[0]
            self.add_log(
                f"get_code_extension: Code extension: {code_extension}")
            return code_extension
        return None

    def get_links(self):
        data = self.factuality_queries
        links = []
        self.add_log("get_links: Data: " + str(data))
        if data is None or len(data) == 0:
            self.add_log("get_links: Data is None.")
            return links
        try:
            for inner_list in data[0]:
                link = inner_list[2][0]
                if link:
                    links.append(link)
        except Exception as e:
            stack_trace = traceback.format_exc()
            self.add_log(stack_trace)
            return links
        self.add_log("get_links: Links: " + str(links))
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
