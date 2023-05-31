"""
Details : BardCoder Library is code genrator for bard. It is used to generate code from bard response.
its using Bard API to interact with bard and refine the results for coding purpose.
The main purpose of this is to integrate bard with any projects and make code generation easy.
Language : Python
Author : HeavenHM.
License : MIT
Date : 21-05-2023
"""

# import libraries
import json
import logging
import os
import json
from bardapi import Bard
import traceback
import subprocess
import time
from os import path
import lib.extensions_map as extensions_map
from lib.extensions_map import get_file_extesion
import inspect

class BardCoder:
    global bard
    global logger
    bard_init = False
    logs_enabled = False
    logs_file = "bardcoder.log"
    response_id, conversation_id, content, factuality_queries, text_query, code_choices, code_extension = None, None, None, None, None, None, None
    
    # Initial setup
    def __init__(self,api_key=None,timeout=10,enable_logs=False):
        try:
            BardCoder.write_log("Starting to initialize BardCoder.")
            # Dont initialize if api key is None.
            if api_key is None or api_key == "" or '.' not in api_key:
                BardCoder.write_log("BardCoder API key is missing or is invalid Skipping init")
                self.bard = None
                BardCoder.bard_init = False
                return None
            
            # Setting up the api key.
            BardCoder.write_log("Setting up the api key")
            if api_key and '.' in api_key:
                self.set_api_key(api_key)
            
            BardCoder.write_log("Setting up the prompt")
            # Setting up Bard from BardAPI.
            self.bard = Bard(timeout=timeout)  # Set timeout in seconds
            
            if not self.bard:
                BardCoder.write_log("BardCoder not initialized...Skipping init.")
                self.bard = None
                BardCoder.bard_init = False
                return None

            # Enable logs
            if enable_logs:
                self.enable_logs()
            
            BardCoder.write_log("Setting up the logger")
            # Setups the logging.
            self.logger = self.setup_logger(self.logs_file)
            
            BardCoder.bard_init = True
            BardCoder.write_log("BardCoder initialized successfully.")
            
        except Exception as e:
            self.add_log(str(e))
            stack_trace = traceback.format_exc()
            self.add_log(stack_trace)
            self.bard = None
    
    def write_log(data:str=None):
        if data is None:
            raise ValueError("Data cannot be None")
        with open("bardcoder.log",'a') as f:
            # Get the name of the calling function
            caller_name = inspect.stack()[1][3]            
            f.write(f"{time.strftime('%d-%m-%Y %H:%M:%S')} {caller_name}: {data}\n")

    # Set the api key
    def set_api_key(self, api_key):
        if api_key:
            os.environ['_BARD_API_KEY'] = api_key
    
    # Set the prompt for bard
    def set_prompt(self, prompt):
        try:
            # Get the response from the prompt.
            response = self.get_response(prompt)
            if response:
                data = json.dumps(response, indent=4)

                if data:
                    # Getting the data from the response.
                    json_data = json.loads(data)
                    if json_data:
                        self.content = json_data['content']
                        self.add_log("Content: " + self.content)

                        # Saving the response to file.
                        self.add_log("Saving response to file.")
                        self.save_file("response/response.json",json.dumps(response, indent=4))
                        self.save_file("response/content.md", self.content)

                        # Getting the content from the response.
                        self.conversation_id = json_data['conversation_id']
                        if self.conversation_id:
                            self.add_log(f"Conversation ID: {self.conversation_id}")

                        # Getting the conversation ID from the response.
                        self.response_id = json_data['response_id']
                        if self.response_id:
                            self.add_log(f"Response ID: {self.response_id}")

                        # Get the factuality queries from the response.
                        self.factuality_queries = json_data['factualityQueries']
                        if self.factuality_queries:
                            for factualityQuery in self.factuality_queries:
                                self.add_log(f"Factuality Query: {factualityQuery}")
                            # Get the links from the response.
                            links = self.get_links()
                            self.add_log(f"Links: {links}")

                        # Get the text query from the response.
                        self.text_query = json_data['textQuery']
                        if self.text_query:
                            self.add_log(f"Text Query: {self.text_query}")

                        # Getting the code choices from the response.
                        self.code_choices = json_data['choices']
                        self.add_log(f"Code Choices: {self.code_choices}")
                        if self.code_choices:
                            for code_choice in self.code_choices:
                                self.add_log(f"Code Choice: {code_choice}")

                        # Mark end of init. - Success
                        self.add_log("Success.")
                        return True,"Success."
                    else:
                        self.add_log("Json data is empty.")
                        return False,"Json data is empty."
                else:
                    self.add_log("Data is empty.")
                    return False,"Data is empty."
            else:
                self.add_log("Response is empty.\nCheck if the API key is valid.")
                return False,"Response is empty.\nCheck if the API key is valid."

        except Exception as e:
            # show stack trace
            stack_trace = traceback.format_exc()
            self.add_log(stack_trace)
            return False,str(e)

    # get the response from bard
    def get_response(self, prompt: str):
        if not prompt:
            self.add_log("Prompt is empty.")
            return ""
        if self.bard:
            self.add_log("Getting response from bard.")
            response = self.bard.get_answer(prompt)
        else:
            self.add_log("Bard is not initialized.")
            return None

        # get response from bard
        return response

    # get multiple responses from bard
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

    # setting the logger
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

    # get the code from bard response
    def get_code(self):
        try:
            if self.content:
                self.add_log("Getting code from content.")
                
                data = self.content
                start_index = data.find("```")
                if start_index == -1:
                    return None
                start_index += 3
                end_index = data.find("```", start_index)
                if end_index == -1:
                    return None
                extracted_data = data[start_index:end_index]
                result = extracted_data.strip()
                
                # Remove the code language identifier
                result = result[result.find('\n') + 1:]
                self.add_log(f"Code: {result}")
                return result
        except Exception as e:
            self.add_log(str(e))
            stack_trace = traceback.format_exc()
            self.add_log(stack_trace)
            
    def save_code(self, filename="code.txt"):
        code = self.get_code()
        self.code_extenstion = '.' + self.get_code_extension()
        if code:
            code = code.replace("\\n", "\n").replace("\\t", "\t")
            self.add_log(f"Saving code with filename: {filename} and extension: {self.code_extenstion} and code: {code}")

            # Add extension to filename
            extension = extensions_map.get_file_extesion(self.code_extenstion) or self.code_extenstion
            filename = filename + extension

            with open(filename, 'w') as f:
                f.write(code)
                self.add_log(f"{filename} saved.")
            return filename

    def save_code(self, filename="code.txt", code='self.add_log("Hello World")'):
        self.add_log(f"Saving code with filename: {filename}")
        extension = self.get_code_extension()
        if extension:
            self.code_extenstion = '.' + extension
            #code = self.get_code()
            if code:
                code = code.replace("\\n", "\n").replace("\\t", "\t")
                self.add_log(f"Saving code with filename: {filename} and extension: {self.code_extenstion} and code: {code}")

                # Add extension to filename
                extension = extensions_map.get_file_extesion(self.code_extenstion) or self.code_extenstion
                filename = filename + extension

                with open(filename, 'w') as f:
                    f.write(code)
                    self.add_log(f"{filename} saved.")
                return filename

    # save multiple codes from bard response
    def save_code_choices(self, filename):
        self.add_log(f"Saving code choices with filename: {filename}")
        extension = self.get_code_extension()
        if extension:
            self.code_extension = '.' + extension
            self.code_extension = extensions_map.get_file_extesion(self.code_extenstion) or self.code_extenstion

            for index, choice in enumerate(self.code_choices):
                choice_content = self.get_code_choice(index)
                self.add_log(f"Enumurated Choice content: {choice}")
                self.save_file("codes/"+filename+'_'+str(index+1) +
                               self.code_extension, choice_content)
                
    # execute code from bard response using locally installed compilers.
    # a support for online compilers will be added soon.
    def execute_code(self, filename):
        if filename:
            self.add_log(f"Running {filename}")
            output = self.run_code_exec(filename)
            self.add_log(f"Output: {output}")
            return output
        return None
    
    # execute code from bard response using locally installed compilers.
    def run_code_exec(self, filename: str, debug: bool = False, cpp_version: str = "c++17"):
        compiler_map = {
            ".c": ("gcc", "c"),
            ".cpp": ("g++", "c++"),
            ".java": ("java", "java"),
            ".go": ("go run", "go"),
            ".cs": ("csc", "csharp"),
            ".swift": ("swift", "swift"),
            ".py": ("python3", "python"),
            ".js": ("node", "javascript"),
            ".rs": ("rustc", "rust")
        }

        _, extension = os.path.splitext(filename)
        self.add_log(f"Extension: {extension}")
        if extension not in compiler_map:
            self.add_log(f"Extension {extension} not supported.")
            return

        compiler, language = compiler_map[extension]
        self.add_log(f"Compiler: {compiler}")

        if language == "c++" and cpp_version.startswith("c++"):
            version = cpp_version[3:]
            if version in ["17", "14", "11", "0x"]:
                cpp_version = f"c++{version}"
                self.add_log(f":C++ Version: {cpp_version}")

        if debug:
            if language == "c++":
                 self.add_log(f"Compiling {filename} with {compiler} (C++ {cpp_version})...")
            else:
                 self.add_log(f"Compiling {filename} with {compiler}...")

        output = ""
        try:
            if language == "c":
                output = subprocess.check_output([compiler, filename, "-o", f"{filename[:-len(extension)]}"], stderr=subprocess.STDOUT).decode('utf-8')
            elif language == "c++":
                output = subprocess.check_output([compiler, filename, f"-std={cpp_version}", "-o", f"{filename[:-len(extension)]}"], stderr=subprocess.STDOUT).decode('utf-8')
            elif language == "java":
                output = subprocess.check_output([compiler, filename], stderr=subprocess.STDOUT).decode('utf-8')
            elif language in ["go", "swift", "python", "javascript","java"]:
                output = subprocess.check_output([compiler, filename], stderr=subprocess.STDOUT).decode('utf-8')
            elif language == "csharp":
                output = subprocess.check_output([compiler, f"/out:{filename[:-len(extension)]}.exe", filename], stderr=subprocess.STDOUT).decode('utf-8')
            elif language == "rust":
                output = subprocess.check_output([compiler, filename], stderr=subprocess.STDOUT).decode('utf-8')
            else:
                self.add_log("Error: Unsupported file type")
                return
            self.add_log(f"Output: {output}")
        except subprocess.CalledProcessError as e:
            output += e.output.decode('utf-8')
            self.add_log(f"Error: {output}")

        if debug:
            self.add_log(f"Running {filename[:-len(extension)]}...")

        # Checking further output for syntax ./path/filename to run the executable
        try:
            # run C# with mono command. like this mono ./path/filename.exe
            if language == "csharp":
                output_file_exec = f"{filename[:-len(extension)]}.exe"
                output += subprocess.check_output(['mono',output_file_exec], stderr=subprocess.STDOUT).decode('utf-8')
            
            else:
                output_file_exec = f"./{filename[:-len(extension)]}"
                # checking if file exists output_file_exec
                if os.path.isfile(output_file_exec):
                    output += subprocess.check_output([output_file_exec], stderr=subprocess.STDOUT).decode('utf-8')
        except (subprocess.CalledProcessError, Exception) as e:
            if isinstance(e, subprocess.CalledProcessError):
                output += '\n' + e.output.decode('utf-8')
            else:
                output += '\n' + str(e)
            self.add_log(f"Error: {output}")
        

        if debug:
            self.add_log(f"Finished running {filename[:-len(extension)]}")

        self.add_log(f"Output: {output}")
        return output

    # execute all the code choices from bard response using locally installed compilers.
    def execute_code_choices(self):
        self.add_log("Running codes")
        codes_choices_output = list()
        for filename in os.listdir('codes'):
            filepath = path.join('codes', filename)
            self.add_log(f"Running {filepath}")
            output = self.execute_code(filepath)
            if output:
                codes_choices_output.append(output)
            time.sleep(5)
        return codes_choices_output

    # get the code extension from bard response - automatically detects the language from bard response.
    def get_code_extension(self):
        try:
            code_content = self.content
            if code_content and not code_content in "can't help":
                self.code_extension = code_content.split('```')[1].split('\n')[0]
                self.add_log(f"Code extension: {self.code_extension}")
                return self.code_extension
        except Exception as e:
            stack_trace = traceback.format_exc()
            self.add_log(stack_trace)
        return None

    # get the links from bard response
    def get_links(self):
        data = self.factuality_queries
        links = []
        self.add_log("Data: " + str(data))
        if data is None or len(data) == 0:
            self.add_log("Data is None.")
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
        self.add_log("Links: " + str(links))
        return links

    def save_file(self, filename, data):
        with open(filename, 'w') as f:
            f.write(data)

    def read_file(self, filename):
        with open(filename, 'r') as f:
            return f.read()

    def add_log(self, log, level=logging.INFO):
        log_msg = inspect.stack()[1][3] + ": " + log
        if self.logs_enabled:
            self.logger.log(level, log_msg)
        else:
            self.logger = self.setup_logger(self.logs_file)
            self.logger.log(level, log_msg)

    def enable_logs(self):
        self.logs_enabled = True
