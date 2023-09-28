"""
Details : AutoBard-Coder is code genrator for bard. It is used to generate code from bard response.
its using Bard API to interact with bard and refine the results for coding purpose.
The main purpose of this is for research and educational purpose.
This is using official PALM API to generate code now.
This can generate the code from prompt and fix itself unless the code is fixed.
Language : Python
Dependencies : streamlit, bard-coder
Author : HeavenHM.
License : MIT
Date : 21-05-2023
Updated Date : 28-09-2023
"""

# Import the required libraries
import logging
import streamlit as st
import time
import traceback
from libs.bardcoder_lib import BardCoder
from libs.logger import logger
import subprocess
from io import StringIO
from libs.sharegpt_api import sharegpt_get_url
from libs.blacklist_commands import harmful_commands_python, harmful_commands_cpp, harmful_prompts
from PIL import Image
import tokenize
from stat import S_IREAD, S_IRGRP, S_IROTH
import re
import io
import os
from os import path

# The input limit of Bard is 4,000 character (As per the Bard API documentation)
# But you can give more input upto 10,000 characters. so we are gonna stick to that.
BARD_FILE_SIZE_LIMIT = 10000

# Function to measure the accuracy of the code
def measure_accuracy(counter):
    accuracy = 1 / (counter + 1)
    accuracy_percentage = accuracy * 100
    st.info(f"Output has been fixed {counter} times with accuracy {accuracy_percentage:.0f}%")


def show_content(content):
    try:
        # Open the file and read its contents
        with open(content, "r") as f:
            markdown_text = f.read()

        # Display the Markdown text in the app
        st.markdown(markdown_text)
    except Exception as e:
        logger.info(f"Error in showing content {e}")


def init_session_state():
  # Initialize the session state variables
    if "bard_coder" not in st.session_state:
        st.session_state.bard_coder = None
    
    if "api_key_initialized" not in st.session_state:
        st.session_state.api_key_initialized = False

    if "code_output" not in st.session_state:
        st.session_state.code_output = ""

    if "messages" not in st.session_state:
        st.session_state.messages = ""

    if "text_area" not in st.session_state:
        st.session_state.text_area = ""

    if "file_size" not in st.session_state:
        st.session_state.file_size = 0

    if "file_char_count" not in st.session_state:
        st.session_state.file_char_count = 0

    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.1

    if "mode" not in st.session_state:
        st.session_state.mode = "precise"

    if "max_output_tokens" not in st.session_state:
        st.session_state.max_output_tokens = 2048
        
    if "safe_system" not in st.session_state:
        st.session_state.safe_system = False
        
    if "save_file" not in st.session_state:
        st.session_state.save_file = False

def init_bard_coder_session(api_key=None, temperature=0.1, max_output_tokens=2048, mode='precise'):
    # Initialize the bard coder session
    try:
        bard_coder = BardCoder(api_key=api_key, model="text-bison-001", temperature=temperature, max_output_tokens=max_output_tokens, mode=mode, guidelines=["exception_handling", "error_handling","code_only"])
    except Exception as e:
        logger.error(f"Error initializing BardCoder session: {e}")
        raise
    return bard_coder


def make_code_interpreter_read_only(files=[],folders:str="libs"):
    for filename in files:
        logger.info(f"Making {filename} read-only")
        os.chmod(filename, S_IREAD|S_IRGRP|S_IROTH)

    # Make all files in lib folder read-only
    logger.info(f"Making all files in {folders} folder read-only")
    folder = folders
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        os.chmod(filepath, S_IREAD|S_IRGRP|S_IROTH)

def create_dirs_on_startup():
    # Create the uploads directory if it does not exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    if not os.path.exists("codes"):
        os.makedirs("codes")
    if not os.path.exists("response"):
        os.makedirs("response")

def read_file(file_path):
    try:
        logger.info(f"Reading file: {file_path}")
        with open(file_path, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error occurred while reading file: {file_path}. Error: {str(e)}")
        return None


# method to execute the bard coder process
def auto_bard_execute(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single', rate_limiter_delay=5):
    logger.info("Starting auto_bard_execute method")
    try:
        # Additional prompt for class clarification.
        # prompt += "\n" + f"Note: The Name the class should be {code_file} if Java language is requested"
        logger.info("Adding additional prompts")

        # Additional prompt for no input clarification.
        prompt += "\n" + "Dont ask the input from user.If input values are provided in code just use them. otherwise, you can hardcode the input values in code."

        # Generate the code from the prompt
        logger.info("Generating code from prompt")
        code = st.session_state.bard_coder.generate_code(prompt, 'python')  # Generate code using BardCoder
        
        # print the code in output.
        if code:
            st.code(code, language='python')
            
        # Save the code to file
        if st.session_state.save_file and code and len(code) > 0:
            logger.info("Saving generated code to file")
            saved_file = st.session_state.bard_coder.save_code(code_file)
            if saved_file:
                logger.info(f"Code saved to file {saved_file}")
                st.info(f"Code saved to file {saved_file}")
            else:
                logger.info("Code not saved to file")
                st.info("Code not saved to file")
                return None, None, False

        logger.info("Executing primary code")
        st.info("Executing primary code")
        # check for safe code to run.
        safe_code = not st.session_state.safe_system
        code_snippet = None
        code_command = None
        safe_code_dict = []

        if code and st.session_state.safe_system:
            logger.info("Checking if code is safe")
            safe_code_dict = is_code_safe(code)
            # Get tuple from list of tuples code_safe_dict
            safe_code = safe_code_dict[0][0]
            code_command = safe_code_dict[0][1]
            code_snippet = safe_code_dict[0][2]

        if safe_code:
            saved_file = ""
            logger.info("Code is safe, executing code")
            if st.session_state.bard_coder is not None:
                code_output = st.session_state.bard_coder.execute_code(code)
            
            if code_output and code_output != None and code_output.__len__() > 0:
                if 'error' in code_output.lower() or 'exception' in code_output.lower():
                    logger.info(f"Error in executing code with type {exec_type}")
                    st.info(f"Error in executing code with type {exec_type}")
                    return code_output, saved_file, False

                # Check if expected output is in code output.
                if expected_output and expected_output in code_output:
                    logger.info("Expected output found in code output")
                    code_choices_output = [code_output]
                    return code_output, saved_file, True
                else:
                    logger.info("Expected output not found in code output")
                    if exec_type == 'single':
                        logger.info("Sleeping for rate limiter delay")
                        time.sleep(rate_limiter_delay)
                        return code_output, saved_file, False
                    else:
                        logger.info("Sleeping for rate limiter delay")
                        time.sleep(rate_limiter_delay)
            else:
                logger.info("Code output is empty")
                return code_output, saved_file, False

            # Save all the code choices to file
            if exec_type == 'multiple':
                logger.info("Saving code choices to file")
                st.session_state.bard_coder.save_code_choices(code_choices)

                logger.info("Executing code choices")
                st.info("Executing code choices")
                code_choices_output = st.session_state.bard_coder.execute_code_choices()
                code_choices_output.append(code_output)
                logger.info(f"Code choices output: {code_choices_output}")
                st.info(f"Output: {code_choices_output}")

            return code_choices_output, saved_file, False
        else:
            logger.info("Code is not safe")
            for safe_codes in safe_code_dict:
                if safe_codes[0]:  # Skip if code is safe
                    continue

                safe_code = safe_codes[0]
                code_command = safe_codes[1]
                code_snippet = safe_codes[2]
                logger.error(f"Error: Cannot execute the code because of illegal command found '{code_command}' in code snippet '{code_snippet}'")
                st.error(f"Error: Cannot execute the code because of illegal command found '{code_command}' in code snippet '{code_snippet}'")
                logger.info(f"Cannot run the code:\n'{code}'\nbecause of illegal command found '{code_command}' in code snippet '{code_snippet}'")
            st.stop()
            return None, None, False

    except Exception as exception:
        # show_outputf the stack trace
        stack_trace = traceback.format_exc()
        st.info(str(exception))
        logger.error(f"Exception {exception} occurred while executing the code {stack_trace}")


# method to execute the bard coder process
def auto_bard_setup(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single', rate_limiter_delay=5):
    logger.info("Starting auto_bard_setup method")

    # Append the codes directory to filename
    code_file = path.join("codes", code_file)
    test_cases_output = 0  # Test cases for output.

    # Start the bard coder process
    logger.info("Starting bard coder process")
    code_choices_output, saved_file, status = auto_bard_execute(prompt, code_file, code_choices, expected_output, exec_type)
    code_output = None

    # Check if file is saved.
    if not saved_file:
        logger.info("File not saved")
        return code_choices_output, saved_file, status

    if status:
        logger.info(f"Expected output found in file {saved_file}\nOutput: {code_choices_output}")
        st.info(f"Expected output found in file {saved_file}\nOutput: {code_choices_output}")
    else:
        logger.info(f"Expected output not found in file {saved_file}\nOutput: {code_choices_output}")
        st.info(f"Expected output not found in file {saved_file}\nOutput: {code_choices_output}")
        if code_choices_output:
            code_output = ''.join(code_choices_output)
        if code_output and code_output != None and code_output.__len__() > 0:

            # Check for errors like 'error' or 'Error' check case sensitivity and add more error checks.
            if code_output is not None:
                code_output = "".join(code_output)
            else:
                code_output = ""

            if code_output:
                logger.info("Checking for errors in code output")
                while 'error' in code_output.lower() or 'exception' in code_output.lower():
                    logger.info(
                        "Error in executing code, trying to fix the code with error")
                    st.info(
                        "Error in executing code,Trying to fix the code with error")

                    # Re-prompt on error.
                    code = st.session_state.bard_coder.get_code()
                    prompt = f"I got error while running the code {code_output}.\nPlease fix the code ``\n`{code}\n``` \nand try again.\nHere is error {code_output}\n\n" + \
                        "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                    # Start the bard coder process again.
                    logger.info("Starting bard coder process again")
                    code_output, saved_file, status = auto_bard_execute(prompt, code_file, code_choices, expected_output, exec_type)
                    # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                    logger.info("Sleeping for rate limiter delay")
                    time.sleep(rate_limiter_delay)
                    test_cases_output += 1

            logger.info("Code has been fixed for errors")
            st.info("Code has been fixed for errors")
            st.code(code_output, language="python")

            # Check for expected output.
            if code_output and expected_output and code_output.__len__() > 0:

                # While expected output does not contain in code output.
                logger.info("Checking for expected output in code output")
                while expected_output not in code_output:
                    logger.info(
                        f"Expected output {expected_output} not found in code\nOutput: {code_output}")
                    st.info(
                        f"Expected output {expected_output} not found in code\nOutput: {code_output}")

                    # Re-prompt on expected output not found.
                    code = st.session_state.bard_coder.get_code()
                    prompt = f"I got output {code_output}.\nPlease fix the code ``\n`{code}\n```  \nand try again.\nHere is expected output: {code_output}\n\n" + \
                        "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                    # start the bard coder process again.
                    logger.info("Starting bard coder process again")
                    code_output, saved_file, status = auto_bard_execute(prompt, code_file, code_choices, expected_output, exec_type)

                    # Sleep for N seconds before re-prompting. Dont get Rate limited.
                    logger.info("Sleeping for rate limiter delay")
                    time.sleep(rate_limiter_delay)
                    test_cases_output += 1

                logger.info("Code has been fixed for expected output")
                st.info("Code has been fixed for expected output")
                st.info(code_output)
            else:
                logger.info("Not checking for code expected output")
                st.info("Not checking for code expected output")
        else:
            logger.info("Code output is empty for error")
            st.info("Code output is empty for error")

    # Print output and information.
    measure_accuracy(test_cases_output)
    content_file = "response/content.md"
    show_content(content_file)
    return code_output, saved_file, status


def find_image_files(file_path):
    logger.info("Starting find_image_files method")
    try:
        # Create a regular expression for image files
        image_regex = re.compile(r"\b\w+\.(png|jpg|jpeg|gif|bmp)", re.IGNORECASE)

        # Open the code file
        logger.info("Opening code file")
        with open(file_path) as f:
            # Read the lines
            lines = f.readlines()
            # Loop through the lines
            for line in lines:
                # Search for image files in the line
                match = image_regex.search(line)
                # If there is a match
                if match:
                    # Get the image file name
                    image_file = match.group()
                    # Print the image file name
                    logger.info(f"Image file found: {image_file}")
                    return image_file
    except Exception as e:
        logger.error(f"Error in finding image files: {e}")
    return None


def is_prompt_safe(prompt):
    logger.info("Starting is_prompt_safe method")
    if prompt is None:
        logger.info("Prompt is Empty")
        return False
    
    logger.info("Checking prompt for safety")

    # Extra care for prompt input.
    prompt_list = [re.sub(r'[^\w\s]', '', re.sub(r'(\*\*|__)(.*?)(\*\*|__)', r'\2', re.sub(
        r'^\W+|\W+$', '', item))).strip() for item in re.split('\n| ', prompt.lower()) if item.strip() != '']
    prompt_list = [re.sub(r'\d+', '', i) for i in prompt_list]
    logger.info(f"Prompt list is {prompt_list}")

    # Convert the code to lowercase and split it into a list of words

    # Check if any harmful command is in the list of words
    for command in harmful_prompts:
        if command in prompt_list:
            logger.info(f"Prompt is not safe because of illegal command found '{command}'")
            return False, command
    logger.info(f"Input Prompt is safe")
    return True, None


def tokenize_source_code(source_code):
    logger.info("Starting tokenize_source_code method")
    tokens = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(source_code).readline):
            if token.type not in [tokenize.ENCODING, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT]:
                if any(char in token.string for char in ['::', '.', '->', '_']) or token.string.isalnum():
                    token_str = re.sub(r'\'|\"', '', token.string)
                    tokens.append(token_str)
    except tokenize.TokenError:
        if st.session_state.bard_coder:
          logger.error("Error parsing the tokens")
    if tokens:
        tokens = list(([token.lower() for token in tokens]))
    if st.session_state.bard_coder:
      logger.info(f"Tokenise was called and Tokens length is {tokens.__len__()}")
    return tokens


def is_code_safe(code):
    logger.info("Starting is_code_safe method")
    if st.session_state.bard_coder:
      logger.info("Checking code for safety")

    # Combine both lists
    harmful_code_commands = harmful_commands_python + harmful_commands_cpp

    # Tokenize the code
    tokens_list = tokenize_source_code(code)

    # Initialize the output dictionary
    output_dict = []

    # Check if any harmful command is in the list of words
    for command in harmful_code_commands:
        for token in tokens_list:
            if command == token:
                output_dict.append((False, command, token))

    if output_dict is None or output_dict.__len__() == 0:
        output_dict = [(True, None, None)]
    if st.session_state.bard_coder:
      logger.info(f"Output dict is {output_dict}")
    return output_dict


def load_css(file_name):
    try:
        # Open the file and read the content
        with open(file_name) as fp:
            css = fp.read()
        # Use st.components.v1.html to load the CSS file
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except Exception as e:
        logger.info(f"Error in loading css {e}")              


def display_logo(logo_file: str, title: str):
    # create two columns
    col1, col2 = st.columns(2, gap='large')

    # use the first column for the image
    col1.image(logo_file, width=370)

    # use the second column for the title
    col2.title(title)


def dsiplay_buttons(is_prompt_valid: bool):
    col1, col2, col3 = st.columns(3, gap='large')

    with col1:  # use the first column
        run_button = st.button("Run", key="run-button", use_container_width=True,
                               disabled=not is_prompt_valid)  # place the run button as a regular button

    with col2:  # use the second column
        share_button = st.button("Share", key="share-button", use_container_width=True,
                                 disabled=not is_prompt_valid)  # place the share button as a regular button

    with col3:
        # place the help button as a regular button
        help_button = st.button(
            "Help", key="help-button", use_container_width=True)

    return run_button, share_button, help_button



if __name__ == "__main__":
    try:
        logger.info("Starting the streamlit App")
        # Create directories on startup
        create_dirs_on_startup()
        
        # Make the code interpreter read-only
        file = __file__
        filenames = [file,file.replace("bardcode_interpreter", "bardcoder")]
        #make_code_interpreter_read_only(filenames,"libs")
        
        # Load the CSS file named style.css
        load_css("styles/style.css")

        # Upload file data variables
        upload_prompt_data, upload_data, uploaded_file = None, None, None

        # Initialize the session state variables
        logger.info("Initializing the session state variables")
        init_session_state()
        logger.info("Session state variables initialized")

        # Set the logo and title
        logo_file = "resources/logo.png"
        title = "Code Interpreter"
        display_logo(logo_file, title)
        logger.info("Logo and title set")

        # Use the text_area variable from the session state for input
        prompt = st.text_area(placeholder="Enter your prompt here", label="Prompt",label_visibility="hidden", height=300, key="text_area_input")

        # check if prompt is changed.
        if prompt != st.session_state.text_area:
            logger.info(f"Prompt changed from '{st.session_state.text_area}' to '{prompt}'")
            st.session_state.text_area = prompt

        character_count: int = len(st.session_state.text_area)

        # Status info message. (Char count and file size)
        status_info_msg = f"Characters:{character_count}/{BARD_FILE_SIZE_LIMIT}"

        if st.session_state.file_size > 0:
            logger.info(f"File Char count is {st.session_state.file_char_count}")
            character_count += st.session_state.file_char_count
            # Update the character count for file size.
            status_info_msg = f"Characters:{character_count}/{BARD_FILE_SIZE_LIMIT}"
            status_info_msg += " | " + f"File Size is {st.session_state.file_size/1024:.2f}Kb | {st.session_state.file_size/1024/1024:.2f}Mb"

        st.info(status_info_msg)

        # check the Prompt for safety and file size exceeding 4,000 characters.
        prompt_safe = True
        if st.session_state.bard_coder and st.session_state.safe_system:
            prompt_safe, command = is_prompt_safe(prompt)
            if not prompt_safe:
                logger.info(f"Error in prompt because of unsafe command found '{command}'")
                st.error(f"Error in prompt because of illegal command found '{command}'")

        if character_count > BARD_FILE_SIZE_LIMIT or st.session_state.file_char_count > BARD_FILE_SIZE_LIMIT:
            st.error(f"Error in prompt The file size limit exceeded {BARD_FILE_SIZE_LIMIT} characters")

        # Setting options for the application
        with st.sidebar.expander("Options"):
            try:
                code_file = st.text_input("Filename for the generated code (without extension):", value="interpreter")
                code_choices = st.text_input("Filename for code choices:", value="interpreter_choices")
                expected_output = st.text_input("Expected output (leave blank if none):")
                exec_type = st.selectbox("Execution type:", ["single", "multiple"], index=0)
                timeout_delay = st.number_input("Timeout (in seconds):", value=10)
                st.session_state.safe_system = st.checkbox("Safe System", value=True)
                st.session_state.save_file = st.checkbox("Save file", value=False)
                
                # Adding the upload file option
                uploaded_file = st.file_uploader("Choose a file")
                if uploaded_file is not None:

                    # To read file as bytes:
                    bytes_data = uploaded_file.getvalue()
                    # get the file size
                    st.session_state.file_size = uploaded_file.size

                    # To convert to a string based IO:
                    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    # To read file as string:
                    upload_data = stringio.read()

                    # Count the number of characters in the file
                    st.session_state.file_char_count = len(upload_data)

                    # write the file to uploads directory
                    with open("uploads/" + uploaded_file.name, "w") as f:
                        f.write(upload_data)

                    # Display a success message
                    st.success("File uploaded successfully.")
            except Exception as exception:
                logger.info(f"Error in options {exception}")

        # Adding settings for the application
        with st.sidebar.expander("Settings"):
            bard_key_help_text = """
            How to obtain Google Palm API key.
            1. Visit https://makersuite.google.com/app/apikey
            2. Click Create API Key.
            3. This is your API key paste it below.
            """
            st.info(bard_key_help_text)
            palm_api_key = st.text_input(label="API Key", label_visibility="hidden", type="password", placeholder="Enter your PALM API key.")
            st.session_state.temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.1)
            st.session_state.max_output_tokens = st.slider("Max Output Tokens", min_value=64, max_value=8000, value=2048, step=64)
            st.session_state.mode = st.selectbox("Mode", options=["precise", "balanced", "creative"], index=0)
            
            if palm_api_key and not st.session_state.api_key_initialized:
                # how to call write_file static method from BardCoder class
                logger.info("Starting init API Key")
                
                st.session_state.bard_coder = init_bard_coder_session(palm_api_key, st.session_state.temperature, st.session_state.max_output_tokens, st.session_state.mode)
                if st.session_state.bard_coder:
                    st.session_state.api_key_initialized = True
                    logger.info("Bard Coder initialized successfully")
                    st.info("Bard Coder initialized successfully")
                else:
                    st.session_state.api_key_initialized = False
                    logger.info("Error initializing Bard Coder")
                    st.error("Error initializing Bard Coder")
                  

        # Setting advanced options for the application
        with st.sidebar.expander("Advanced"):
            try:
                # button to show logs.
                show_logs = st.button("Show Logs", key="show-logs-button", use_container_width=True)
                if show_logs:
                    if st.session_state.bard_coder:
                        logs_data = read_file('bardcoder.log')
                        st.code(logs_data, language="python")
            except Exception as exception:
                st.error(f"Error in showing logs {exception}")
                    
            # button to show content.
            try:
                show_content_button = st.button("Show Content", key="show-content-button", use_container_width=True)
                if show_content_button:
                    if st.session_state.bard_coder:
                        content_data = read_file("response/response.md")
                        st.code(content_data, language="python")
            except Exception as exception:
                st.error(f"Error in showing content {exception}")
            
            # button to show response.
            try:
                show_response_button = st.button("Show Response", key="show-response-button", use_container_width=True)
                if show_response_button:
                    if st.session_state.bard_coder:
                        response_data = read_file("response/response.json")
                        st.code(response_data, language="json")
            except Exception as exception:
                st.error(f"Error in showing response {exception}")
                        
        # Setting the buttons for the application
        run_button, share_button, help_button = dsiplay_buttons(prompt_safe and st.session_state.file_char_count < BARD_FILE_SIZE_LIMIT)

        # Setting application to run
        if run_button:
            saved_file = None
            # Check if API Key is empty
            if palm_api_key is None or palm_api_key == "" or palm_api_key.__len__() == 0:
                st.error("Error executing code the API key is missing from settings.\nPlease go to settings and add your API key.")
                logger.info("Error executing code the API key is missing from settings.Please go to settings and add your API key.")
                st.stop()

            # Clear the previous cache.
            st.info("Running the code interpreter...")
            subprocess.call(['bash', 'bash_src/clear_cache.sh'])

            # Append the uploaded file data to prompt
            if upload_data:
                prompt += "\n" + f"Here is the file called {uploaded_file.name} at location {'uploads/' + uploaded_file.name} data.\n" + \
                    f"```\n{upload_data}\n```"

            # If graph were requested.
            if 'graph' in prompt.lower():
                prompt += "\n" + "using Python use Matplotlib save the graph in file called 'graph.png'"

            # if Chart were requested
            if 'chart' in prompt.lower() or 'plot' in prompt.lower():
                prompt += "\n" + "using Python use Plotly save the chart in file called 'chart.png'"

            # if Table were requested
            if 'table' in prompt.lower():
                prompt += "\n" + "using Python use Pandas save the table in file called 'table.md'"

            # Refine the prompt for harmful commands.
            try:
                if prompt_safe:
                    # Run the auto bard setup process.
                    log_container = st.empty()
                    st.session_state.code_output, saved_file, status = auto_bard_setup(prompt, code_file, code_choices,expected_output, exec_type,timeout_delay)
                    if st.session_state.code_output:
                        st.code(st.session_state.code_output,language='python')
                else:
                    st.error(f"Cannot execute the prompt because of illegal command found '{command}'")
                    logger.info(f"Cannot execute the prompt: '{prompt}' because of illegal command found '{command}'")
                    st.stop()
            except Exception as exception:
                logger.info(f"Error in auto bard setup {exception}")
                
            # Check if output is Graph,Chart request.
            if 'graph' in prompt.lower() or 'chart' in prompt.lower():
                image_file_graph = find_image_files(saved_file)
                if image_file_graph:
                    logger.info(f"Graph image file is {image_file_graph} and code file is {saved_file}")
                    image = Image.open(image_file_graph)
                    st.image(image, caption='Graph Output')

            # Check if output in Table request.
            if 'table' in prompt.lower():
                table_file = "table.md"
                table_file_data = read_file(table_file)
                if table_file_data:
                    st.markdown(table_file_data)

        # Adding Share button
        if share_button:
            if st.session_state.code_output is None or st.session_state.messages is None:
                logger.info("ShareGPT: Error Please run the code generator first")
                st.error("Error: Please run the code generator first")
            else:
                gpt_data = prompt
                human_data = ""

                if st.session_state.messages:
                    human_data = "Bard Logs: \n" + st.session_state.messages
                if st.session_state.code_output:
                    human_data += "\nOutput:\n" + st.session_state.code_output
                human_data += "\n\n[AutoBard-Coder: Repo](https:#github.com/haseeb-heaven/AutoBard-Coder)"

                if gpt_data.__len__() > 0 and human_data.__len__() > 0:
                    sharegpt_url = sharegpt_get_url(gpt_data, human_data)
                    st.info(f"ShareGPT Url: {sharegpt_url}")
                else:
                    logger.info("ShareGPT: Error Please run the code generator first")
                    st.error("Error: Please run the code generator first")

        # Adding Help button
        if help_button:
            content_file = "README.md"
            if st.session_state.bard_coder:
                content_data = read_file(content_file)
                st.markdown(content_data, unsafe_allow_html=True)
            else:
                st.error("API key is missing from settings.\nPlease go to settings and add your API key.")
                logger.info("Help: Error API key is missing from settings.")

    except Exception as exception:
        # show_outputf the stack trace
        stack_trace = traceback.format_exc()
        st.error("Error: " + str(exception))
        logger.error(f"Error: {exception}\n{stack_trace}")