
import os
import sys
import time
import subprocess
import traceback
from dotenv import load_dotenv
from libs.bardcoder_lib import BardCoder
from libs.makrdown_code import display_markdown_message,display_code
from libs.package_installer import PackageInstaller

bard_coder = None
pip_installer = None

def setup_bard_coder():
    # load the environment variables from .env file
    load_dotenv()

    # Initialize the bard coder
    api_key = os.getenv("PALMAI_API_KEY")  # get value of Palm API key.
    # Define guidelines as a list of strings
    guidelines = ["only_code","script_only", "exception_handling", "error_handling"]

    # Initialize the bard coder with the defined guidelines
    bard_coder = BardCoder(api_key=api_key, model="text-bison-001", temperature=0.1, max_output_tokens=2048, mode='precise', guidelines=guidelines)
    return bard_coder

def generate_code(bard_coder, prompt):
    try:
        # Generate the code.
        code = bard_coder.generate_code(prompt, 'python')  # Generate code using BardCoder
        if not code:
            display_markdown_message(f"Error no data was recieved from Server")
            return None
        else:
            display_code(code)
        return code
    except Exception as e:
        display_markdown_message(f"Error in generating code: {str(e)}")
        return None

def execute_code(bard_coder, code):
    max_tries = 5
    delay = 5  # delay in seconds
    code_output = ""
    code_error = ""
    global pip_installer
    
    # Execute the code.
    code_output, code_error = bard_coder.execute_code(code)
    if code_output and code_output != None and code_output.__len__() > 0:
        display_markdown_message(f"Output: {code_output}")
        return code_output, code_error
    
    code_fixed = code
    # We will try to execute the code for a maximum number of times defined by max_tries
    for index in range(max_tries):
        try:
            # If there was an error in the previous execution of the code
            if code_error:
                # Display a message indicating that the code execution failed and we are attempting to fix the code
                display_markdown_message(f"Code execution **failed**. **Fixing code.**")
                # Attempt to fix the code using the bard_coder's fix_code method
                code_fixed = bard_coder.fix_code(code_fixed,code_error)
                
                # If the code could not be fixed, display a message and continue to the next iteration
                if code_fixed is None:
                    code_fixed = code # Reset the code back to try-again.
                    display_markdown_message(f"Code **fixing** failed.- Retring")
                    continue
                
                # Execute the fixed code
                code_output, code_error = bard_coder.execute_code(code_fixed)
                
                # If the execution of the fixed code was successful, display the output and return it
                if code_output and code_output != None and code_output.__len__() > 0:
                    display_markdown_message(f"Output: {code_output}")
                    return code_output, code_error
                else:
                    # If the execution of the fixed code was not successful, display the error
                    display_markdown_message(f"Code Error is {code_error}")
                
                # Install the missing package on error.
                if "ModuleNotFoundError" in code_error or "No module named" in code_error:
                    package_name = pip_installer.extract_package_name(code_error)
                    display_markdown_message(f"Trying to install missing package **'{package_name}'** on error")
                    pip_installer.install_package(package_name)
                    display_markdown_message(f"Successfully installed package **'{package_name}'**")
                
                
        except Exception as exception:
            display_markdown_message(f"Error in executing code: {str(exception)}")
            if index < max_tries - 1:  # it's not the final try
                time.sleep(delay)  # delay before next try
            else:  # it's the final try
                return None
            
def clean_responses():
    files_to_remove = ['graph.png', 'chart.png', 'table.md']
    for file in files_to_remove:
        try:
            if os.path.isfile(file):
                os.remove(file)
                print(f"{file} removed successfully")
        except Exception as e:
            print(f"Error in removing {file}: {str(e)}")

import argparse

def bard_main(args) -> None:
    try:
        display_markdown_message("Welcome to **PALM - Interpreter**")
        bard_coder = setup_bard_coder()
        global pip_installer
        pip_installer = PackageInstaller()

        display_markdown_message("Enter prompt (or type '**qui**t' or '**exit**' to terminate): ")
        while True:
            prompt = input("> ")
            
            # Check for termination commands
            if prompt.lower() in ['quit', 'exit']:
                display_markdown_message("Terminating the program...")
                break
                
            # clean responses
            clean_responses()
            
            # Check if prompt is empty.
            if not prompt and prompt.__len__() == 0:
                display_markdown_message(f"Prompt is empty")
                continue
            
            # If graph were requested.
            if 'graph' in prompt.lower():
                prompt += "\n" + "using Python use Matplotlib save the graph in file called 'graph.png'"

            # if Chart were requested
            if 'chart' in prompt.lower() or 'plot' in prompt.lower():
                prompt += "\n" + "using Python use Plotly save the chart in file called 'chart.png'"

            # if Table were requested
            if 'table' in prompt.lower():
                prompt += "\n" + "using Python use Pandas save the table in file called 'table.md'"
            
            # More guidings for Prompt.
            prompt += "\n" + "Make sure the code has no comments and it should not be modular code it should be sequential line by line and should not ask any kind of input from the user whatsoever"
            prompt += "\n" + "Make sure the code doesnt add any logs or documents to it and make the code short and simple and code should not have any main method there should be no methods in the code"
            
            # Generate the code using PALM 2.
            code = generate_code(bard_coder, prompt)
            
            if code is not None:
                if args.save_code:
                    with open('generated_code.py', 'w') as file:
                        file.write(code)
                if not args.exec:
                    if input("Do you want to execute the code? (y/n): ").lower() == 'y':
                        execute_code(bard_coder, code)
                else:
                    execute_code(bard_coder, code)
                
            try:
                # Check if graph.png exists and open it using subprocess
                if os.path.isfile('graph.png'):
                    subprocess.call(['open', 'graph.png'])
                    print("graph.png exists and opened successfully")
                
                # Check if chart.png exists and open it using subprocess
                if os.path.isfile('chart.png'):
                    subprocess.call(['open', 'chart.png'])
                    print("chart.png exists and opened successfully")
                
                # Check if table.md exists and open it using subprocess
                if os.path.isfile('table.md'):
                    subprocess.call(['open', 'table.md'])
                    print("table.md exists and opened successfully")
            except Exception as exception:
                display_markdown_message(f"Error in opening files: {str(exception)}")
        
    except Exception as exception:
        stack_trace = traceback.format_exc()
        display_markdown_message(stack_trace)
        display_markdown_message(str(exception))

# App main entry point.
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='PALM - Interpreter')
        parser.add_argument('--exec', '-e', action='store_true', help='Execute the code')
        parser.add_argument('--save_code', '-s', action='store_true', help='Save the generated code')
        parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')
        args = parser.parse_args()
        
        # Check if only the application name is passed
        if len(sys.argv) == 0 and sys.argv[0] == parser.prog:
            display_markdown_message("**Usage: python interpreter.py [options]**")
            display_markdown_message("**Options:**")
            display_markdown_message("**--exec, -e: Execute the code**")
            display_markdown_message("**--save_code: Save the generated code**")
            display_markdown_message("**--version: Show the version of the program**")
            sys.exit(1)
        
        bard_main(args)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
