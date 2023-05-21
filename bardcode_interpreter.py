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
import streamlit as st
from os import path
import time
import traceback
from lib.bardcoder_lib import BardCoder
from lib.extensions_map import get_streamlit_code_lang
import subprocess
from io import StringIO

# Initialize the bard coder
bard_coder = BardCoder(enable_logs=True)

# Function to measure the accuracy of the code
def measure_accuracy(counter):
    accuracy = 1 / (counter + 1)
    accuracy_percentage = accuracy * 100
    st.code(f"Output has been fixed {counter} times with accuracy {accuracy_percentage:.0f}%", language="python")

def show_content(content):
    # Open the file and read its contents
    with open(content, "r") as f:
        markdown_text = f.read()

    # Display the Markdown text in the app
    st.markdown(markdown_text)

# Initialize an empty string to hold the messages
global log_container
messages = ""

def show_output(message):
    global messages
    messages += message + "\n"
    log_container.code(messages, language="python")

# method to execute the bard coder process
def auto_bard_execute_process(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single',rate_limiter_delay=5):
    try:
        # Additional prompt for class clarification.
        prompt += "\n" + f"Note: The Name the class should be {code_file} if Java and C# languages is selected"
        
        # Additional prompt for no input clarification.
        prompt += "\n" + "Dont ask the input from user.If input values are provided in code just use them. otherwise, you can hardcode the input values in code."
        
        # Setting the prompt.
        bard_coder.set_prompt(prompt)

        # Get the code from the response.
        code = bard_coder.get_code()
        # Save the code to file
        saved_file = bard_coder.save_code(code_file, code)
        if saved_file:
            show_output(f"Code saved to file {saved_file}")
        else:
            show_output("Code not saved to file")

        show_output("Executing primary code")
        code_output = bard_coder.execute_code(saved_file)
        if code_output and code_output != None and code_output.__len__() > 0:
            if 'error' in code_output.lower() or 'exception' in code_output.lower():
                show_output(f"Error in executing code with exec_type {exec_type}")
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
            bard_coder.save_code_choices(code_choices)

            show_output("Executing code choices")
            code_choices_output = bard_coder.execute_code_choices()
            code_choices_output.append(code_output)
            show_output(f"Output: {code_choices_output}")

        # Execute all the code and code choices.
        # bard_coder.execute_code_choices()

        return code_choices_output, saved_file, False

    except Exception as e:
        # show_outputf the stack trace
        stack_trace = traceback.format_exc()
        show_output(stack_trace)
        show_output(str(e))

# method to execute the bard coder process
def auto_bard_setup_process(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single',rate_limiter_delay=5):
    
    # Append the codes directory to filename
    code_file = path.join("codes",code_file)
    test_cases_output = 0 # Test cases for output.
        
    # Start the bard coder process
    code_choices_output, saved_file, status = auto_bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
    code_output = None
    
    if status:
        show_output(f"Expected output found in file {saved_file}\nOutput: {code_choices_output}")
    else:
        show_output(f"Expected output not found in file {saved_file}\nOutput: {code_choices_output}")
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
                    show_output(f"Error in executing code,Trying to fix the code with error")

                    # Re-prompt on error.
                    code = bard_coder.get_code()
                    prompt = f"I got error while running the code {code_output}.\nPlease fix the code ``\n`{code}\n``` \nand try again.\nHere is error {code_output}\n\n" + \
                    "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                    # Start the bard coder process again.
                    code_output, saved_file, status = auto_bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
                    # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                    time.sleep(rate_limiter_delay)
                    test_cases_output += 1
                
            show_output(f"Code has been fixed for error")
            st.code(code_output, language="python")

            # Check for expected output.
            if code_output and expected_output and code_output.__len__() > 0:
                
                # While expected output does not contain in code output.
                while expected_output not in code_output:
                    show_output(f"Expected output {expected_output} not found in code\nOutput: {code_output}")

                    # Re-prompt on expected output not found.
                    code = bard_coder.get_code()
                    prompt = f"I got output {code_output}.\nPlease fix the code ``\n`{code}\n```  \nand try again.\nHere is expected output: {code_output}\n\n" + \
                    "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                    # start the bard coder process again.
                    code_output, saved_file, status = auto_bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
                    
                    # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                    time.sleep(rate_limiter_delay)
                    test_cases_output += 1
                    
                show_output(f"Code has been fixed for expected output")
                st.code(code_output, language="python")
            else:
                show_output("Not checking for code expected output")            
        else:
            show_output("Code output is empty for error")
        
    # Print output and information.
    measure_accuracy(test_cases_output)            
    content_file = "response/content.md"
    show_content(content_file)


if __name__ == "__main__":
    # Set the page title and description
    st.title("AutoBard - Code Interpreter")
    prompt = st.text_area("Enter your prompt here:")
    bard_api_key = ""
    
    # Setting options for the application
    with st.expander("Options"):
        code_file = st.text_input("Filename for the generated code (without extension):", value="generated_code")
        code_choices = st.text_input("Filename for code choices:", value="code_choices")
        expected_output = st.text_input("Expected output (leave blank if none):")
        exec_type = st.selectbox("Execution type:", ["single", "multiple"], index=0)
        rate_limiter_delay = st.number_input("Rate limiter delay (in seconds):", value=5)

    # Setting the settings for the application    
    with st.expander("Settings"):
        bard_api_key = st.text_input("Bard API key:", type="password")
        if bard_api_key:
            bard_coder.set_api_key(bard_api_key)

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        upload_data = stringio.read()

        # Display a success message
        st.success("File uploaded successfully.")
        
        # Run the auto bard setup process.
        log_container = st.empty()
        prompt = "I want you to anaylze the file and show its basic data visualization.\n" + \
        "Here is the file data.\n" + \
        f"```\n{upload_data}\n```"
        auto_bard_setup_process(prompt, code_file, code_choices, expected_output, exec_type, rate_limiter_delay)

            
    # Seting application to run
    if st.button("Run"):
        # Clear the previous cache.
        st.code("Running the code generator", language="python")
        subprocess.call(['bash', 'bash_src/clear_cache.sh'])
        
        # Run the auto bard setup process.
        log_container = st.empty()
        auto_bard_setup_process(prompt, code_file, code_choices, expected_output, exec_type, rate_limiter_delay)

