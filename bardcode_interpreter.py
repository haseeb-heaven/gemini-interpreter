"""
Details : AutoBard-Coder is code genrator for bard. It is used to generate code from bard response.
its using Bard API to interact with bard and refine the results for coding purpose.
The main purpose of this is for research and educational purpose.
This is using unofficial bard api and not affiliated with bard in any way - So use it at your own risk.
This can generate the code from prompt and fix itself unless the code is fixed.
Language : Python
Dependencies : streamlit, bard-coder
Author : HeavenHM.
License : MIT
Date : 21-05-2023
"""

# Import the required libraries
import logging
import sys
import streamlit as st
from os import path
import time
import traceback
from lib.bardcoder_lib import BardCoder
import subprocess
from io import StringIO
import re
from lib.sharegpt_api import sharegpt_get_url
from lib.blacklist_commands import harmful_commands_python, harmful_commands_cpp, harmful_prompts
from PIL import Image
import tokenize
import io

# The input limit of Bard is 4,000 character (As per the Bard API documentation)
# But you can give more input upto 10,000 characters. so we are gonna stick to that.
BARD_FILE_SIZE_LIMIT = 10000

# Function to measure the accuracy of the code


def measure_accuracy(counter):
    accuracy = 1 / (counter + 1)
    accuracy_percentage = accuracy * 100
    st.info(
        f"Output has been fixed {counter} times with accuracy {accuracy_percentage:.0f}%")


def show_content(content):
    # Open the file and read its contents
    with open(content, "r") as f:
        markdown_text = f.read()

    # Display the Markdown text in the app
    st.markdown(markdown_text)


# method to execute the bard coder process
def auto_bard_execute(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single', rate_limiter_delay=5):
    try:
        # Additional prompt for class clarification.
        # prompt += "\n" + f"Note: The Name the class should be {code_file} if Java language is requested"

        # Additional prompt for no input clarification.
        prompt += "\n" + "Dont ask the input from user.If input values are provided in code just use them. otherwise, you can hardcode the input values in code."

        # Setting the prompt.
        prompt_status, error_reason = st.session_state.bard_coder.set_prompt(
            prompt)
        if not prompt_status:
            st.error(
                f"Error no data was recieved from Server, Reason {error_reason}")
            st.stop()

        # Get the code from the response.
        code = st.session_state.bard_coder.get_code()
        # Save the code to file
        saved_file = st.session_state.bard_coder.save_code(code_file, code)
        if saved_file:
            st.info(f"Code saved to file {saved_file}")
        else:
            st.info("Code not saved to file")
            return None, None, False

        st.info("Executing primary code")
        # check for safe code to run.
        code = st.session_state.bard_coder.read_file(saved_file)
        safe_code = False
        code_snippet = None
        code_command = None
        safe_code_dict = []

        if code:
            safe_code_dict = is_code_safe(code)
            # Get tuple from list of tuples code_safe_dict
            safe_code = safe_code_dict[0][0]
            code_command = safe_code_dict[0][1]
            code_snippet = safe_code_dict[0][2]

        if safe_code:
            code_output = st.session_state.bard_coder.execute_code(saved_file)
            if code_output and code_output != None and code_output.__len__() > 0:
                if 'error' in code_output.lower() or 'exception' in code_output.lower():
                    st.info(f"Error in executing code with type {exec_type}")
                    return code_output, saved_file, False

                # Check if expected output is in code output.
                if expected_output and expected_output in code_output:
                    code_choices_output = [code_output]
                    return code_output, saved_file, True
                else:
                    if exec_type == 'single':
                        time.sleep(rate_limiter_delay)
                        return code_output, saved_file, False
                    else:
                        time.sleep(rate_limiter_delay)
            else:
                return code_output, saved_file, False

            # Save all the code choices to file
            if exec_type == 'multiple':
                st.session_state.bard_coder.save_code_choices(code_choices)

                st.info("Executing code choices")
                code_choices_output = st.session_state.bard_coder.execute_code_choices()
                code_choices_output.append(code_output)
                st.info(f"Output: {code_choices_output}")

            return code_choices_output, saved_file, False
        else:
            for safe_codes in safe_code_dict:
                if safe_codes[0]:  # Skip if code is safe
                    continue

                safe_code = safe_codes[0]
                code_command = safe_codes[1]
                code_snippet = safe_codes[2]
                st.error(f"Error: Cannot execute the code because of illegal command found '{code_command}' in code snippet '{code_snippet}'")
                if st.session_state.bard_coder:
                  st.session_state.bard_coder.add_log(f"Cannot run the code:\n'{code}'\nbecause of illegal command found '{code_command}' in code snippet '{code_snippet}'", logging.ERROR)
            st.stop()
            return None, None, False

    except Exception as e:
        # show_outputf the stack trace
        stack_trace = traceback.format_exc()
        st.info(stack_trace)
        st.info(str(e))


# method to execute the bard coder process
def auto_bard_setup(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single', rate_limiter_delay=5):

    # Append the codes directory to filename
    code_file = path.join("codes", code_file)
    test_cases_output = 0  # Test cases for output.

    # Start the bard coder process
    code_choices_output, saved_file, status = auto_bard_execute(
        prompt, code_file, code_choices, expected_output, exec_type)
    code_output = None

    # Check if file is saved.
    if not saved_file:
        return code_choices_output, saved_file, status

    if status:
        st.info(
            f"Expected output found in file {saved_file}\nOutput: {code_choices_output}")
    else:
        st.info(
            f"Expected output not found in file {saved_file}\nOutput: {code_choices_output}")
        if code_choices_output:
            code_output = ''.join(code_choices_output)
        if code_output and code_output != None and code_output.__len__() > 0:

            # Check for errors like 'error' or 'Error' check case sensitivity and add more error checks.
            if code_output is not None:
                code_output = "".join(code_output)
            else:
                code_output = ""

            if code_output:
                while 'error' in code_output.lower() or 'exception' in code_output.lower():
                    st.info(
                        "Error in executing code,Trying to fix the code with error")

                    # Re-prompt on error.
                    code = st.session_state.bard_coder.get_code()
                    prompt = f"I got error while running the code {code_output}.\nPlease fix the code ``\n`{code}\n``` \nand try again.\nHere is error {code_output}\n\n" + \
                        "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                    # Start the bard coder process again.
                    code_output, saved_file, status = auto_bard_execute(
                        prompt, code_file, code_choices, expected_output, exec_type)
                    # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                    time.sleep(rate_limiter_delay)
                    test_cases_output += 1

            st.info("Code has been fixed for errors")
            st.code(code_output, language="python")

            # Check for expected output.
            if code_output and expected_output and code_output.__len__() > 0:

                # While expected output does not contain in code output.
                while expected_output not in code_output:
                    st.info(
                        f"Expected output {expected_output} not found in code\nOutput: {code_output}")

                    # Re-prompt on expected output not found.
                    code = st.session_state.bard_coder.get_code()
                    prompt = f"I got output {code_output}.\nPlease fix the code ``\n`{code}\n```  \nand try again.\nHere is expected output: {code_output}\n\n" + \
                        "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                    # start the bard coder process again.
                    code_output, saved_file, status = auto_bard_execute(
                        prompt, code_file, code_choices, expected_output, exec_type)

                    # Sleep for N seconds before re-prompting. Dont get Rate limited.
                    time.sleep(rate_limiter_delay)
                    test_cases_output += 1

                st.info("Code has been fixed for expected output")
                st.info(code_output)
            else:
                st.info("Not checking for code expected output")
        else:
            st.info("Code output is empty for error")

    # Print output and information.
    measure_accuracy(test_cases_output)
    content_file = "response/content.md"
    show_content(content_file)
    return code_output, saved_file, status


def find_image_files(file_path):
    # Create a regular expression for image files
    image_regex = re.compile(r"\b\w+\.(png|jpg|jpeg|gif|bmp)", re.IGNORECASE)

    # Open the code file
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
                return image_file
    return None


def is_prompt_safe(prompt):
    if st.session_state.bard_coder:
        st.session_state.bard_coder.add_log("Checking prompt for safety")

    # Extra care for prompt input.
    prompt_list = [re.sub(r'[^\w\s]', '', re.sub(r'(\*\*|__)(.*?)(\*\*|__)', r'\2', re.sub(
        r'^\W+|\W+$', '', item))).strip() for item in re.split('\n| ', prompt.lower()) if item.strip() != '']
    prompt_list = [re.sub(r'\d+', '', i) for i in prompt_list]
    if st.session_state.bard_coder:
        st.session_state.bard_coder.add_log(f"Prompt list is {prompt_list}")

    # Convert the code to lowercase and split it into a list of words

    # Check if any harmful command is in the list of words
    for command in harmful_prompts:
        if command in prompt_list:
            if st.session_state.bard_coder:
                st.session_state.bard_coder.add_log(f"Prompt is not safe because of illegal command found '{command}'")
            return False, command
    if st.session_state.bard_coder:
        st.session_state.bard_coder.add_log(f"Input Prompt is safe")
    return True, None


def tokenize_source_code(source_code):
    tokens = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(source_code).readline):
            if token.type not in [tokenize.ENCODING, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT]:
                if any(char in token.string for char in ['::', '.', '->', '_']) or token.string.isalnum():
                    token_str = re.sub(r'\'|\"', '', token.string)
                    tokens.append(token_str)
    except tokenize.TokenError:
        if st.session_state.bard_coder:
          st.session_state.bard_coder.add_log("Error parsing the tokens")
    if tokens:
        tokens = list(([token.lower() for token in tokens]))
    if st.session_state.bard_coder:
      st.session_state.bard_coder.add_log(f"Tokenise was called and Tokens length is {tokens.__len__()}")
    return tokens


def is_code_safe(code):
    if st.session_state.bard_coder:
      st.session_state.bard_coder.add_log("Checking code for safety")

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
      st.session_state.bard_coder.add_log(f"Output dict is {output_dict}")
    return output_dict


def load_css(file_name):
    # Open the file and read the content
    with open(file_name) as fp:
        css = fp.read()
    # Use st.components.v1.html to load the CSS file
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


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


def init_bard_coder_session(api_key=None, timeout=10):
    # Initialize the bard coder session
    bard_coder = BardCoder(api_key=api_key, enable_logs=True, timeout=timeout)
    return bard_coder


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


if __name__ == "__main__":
    try:
        # Load the CSS file named style.css
        load_css("styles/style.css")

        # Upload file data variables
        upload_prompt_data, upload_data, uploaded_file = None, None, None

        # Initialize the session state variables
        init_session_state()

        # Set the logo and title
        logo_file = "resources/logo.png"
        title = "Code Interpreter"
        display_logo(logo_file, title)

        # Use the text_area variable from the session state for input
        prompt = st.text_area(placeholder="Enter your prompt here", label="Prompt",
                              label_visibility="hidden", height=300, key="text_area_input")

        # check if prompt is changed.
        if prompt != st.session_state.text_area:
            if st.session_state.bard_coder:
              st.session_state.bard_coder.add_log(f"Prompt changed from '{st.session_state.text_area}' to '{prompt}'")
            st.session_state.text_area = prompt

        character_count: int = len(st.session_state.text_area)

        # Status info message. (Char count and file size)
        status_info_msg = f"Characters:{character_count}/{BARD_FILE_SIZE_LIMIT}"

        if st.session_state.file_size > 0:
            if st.session_state.bard_coder:
              st.session_state.bard_coder.add_log(f"File Char count is {st.session_state.file_char_count}")
            character_count += st.session_state.file_char_count
            # Update the character count for file size.
            status_info_msg = f"Characters:{character_count}/{BARD_FILE_SIZE_LIMIT}"
            status_info_msg += " | " + f"File Size is {st.session_state.file_size/1024:.2f}Kb | {st.session_state.file_size/1024/1024:.2f}Mb"

        st.info(status_info_msg)

        # check the Prompt for safety and file size exceeding 4,000 characters.
        prompt_safe, command = is_prompt_safe(prompt)
        if not prompt_safe:
            st.error(
                f"Error in prompt because of illegal command found '{command}'")

        if character_count > BARD_FILE_SIZE_LIMIT or st.session_state.file_char_count > BARD_FILE_SIZE_LIMIT:
            st.error(
                f"Error in prompt The file size limit exceeded {BARD_FILE_SIZE_LIMIT} characters")

        # Setting options for the application
        with st.expander("Options"):
            code_file = st.text_input(
                "Filename for the generated code (without extension):", value="generated_code")
            code_choices = st.text_input(
                "Filename for code choices:", value="code_choices")
            expected_output = st.text_input(
                "Expected output (leave blank if none):")
            exec_type = st.selectbox(
                "Execution type:", ["single", "multiple"], index=0)
            rate_limiter_delay = st.number_input(
                "Rate limiter delay (in seconds):", value=5)

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

        with st.expander("Settings"):
            bard_key_help_text = """
      How to obtain Google Bard API key.
      1. Visit bard.google.com and open the console with F12
      2. Go to Application → Cookies and copy the __Secure-1PSID value
      3. This is your API key paste it below.
      """
            st.info(bard_key_help_text)
            bard_api_key = st.text_input(label="API Key", label_visibility="hidden", type="password", placeholder="Enter your bard API key.")
            
            if bard_api_key and not st.session_state.api_key_initialized:
                st.session_state.bard_coder = init_bard_coder_session(bard_api_key)
                if st.session_state.bard_coder:
                    st.session_state.api_key_initialized = True
                    st.info("Bard Coder initialized successfully")
                else:
                    st.session_state.api_key_initialized = False
                    st.error("Error initializing Bard Coder")
                  

        # Setting the buttons for the application
        run_button, share_button, help_button = dsiplay_buttons(
            prompt_safe and st.session_state.file_char_count < BARD_FILE_SIZE_LIMIT)

        # Seting application to run
        if run_button:
            # Code to execute when the "Run" button is clicked

            # Check if API Key is empty
            if bard_api_key is None or bard_api_key == "" or bard_api_key.__len__() == 0:
                st.error(
                    "Error executing code the API key is missing from settings.\nPlease go to settings and add your API key.")
                if st.session_state.bard_coder:
                  st.session_state.bard_coder.add_log("Error executing code the API key is missing from settings.\nPlease go to settings and add your API key.")
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
            if prompt_safe:
                # Run the auto bard setup process.
                log_container = st.empty()
                st.session_state.code_output, saved_file, status = auto_bard_setup(prompt, code_file, code_choices, 
                                                                                   expected_output, exec_type,rate_limiter_delay)
            else:
                st.error(f"Cannot execute the prompt because of illegal command found '{command}'")
                if st.session_state.bard_coder:
                  st.session_state.bard_coder.add_log(f"Cannot execute the prompt: '{prompt}' because of illegal command found '{command}'", logging.ERROR)
                st.stop()

            # Check if output is Graph,Chart request.
            if 'graph' in prompt.lower() or 'chart' in prompt.lower():
                image_file_graph = find_image_files(saved_file)
                if image_file_graph:
                    if st.session_state.bard_coder:
                      st.session_state.bard_coder.add_log(f"Graph image file is {image_file_graph} and code file is {saved_file}")
                    image = Image.open(image_file_graph)
                    st.image(image, caption='Graph Output')

            # Check if output in Table request.
            if 'table' in prompt.lower():
                table_file = "table.md"
                table_file_data = st.session_state.bard_coder.read_file(
                    table_file)
                if table_file_data:
                    st.markdown(table_file_data)

        # Adding Share button
        if share_button:
            if st.session_state.code_output is None or st.session_state.messages is None:
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
                    st.error("Error: Please run the code generator first")

        # Adding Help button
        if help_button:
            content_file = "README.md"
            if st.session_state.bard_coder:
                content_data = st.session_state.bard_coder.read_file(content_file)
                st.markdown(content_data, unsafe_allow_html=True)

    except Exception as e:
        # show_outputf the stack trace
        stack_trace = traceback.format_exc()
        st.error("Error: " + str(e))
        st.error(stack_trace)
