
import os
import time
import subprocess
import traceback
from dotenv import load_dotenv
from libs.bardcoder_lib import BardCoder
from libs.makrdown_code import display_markdown_message,display_code

bard_coder = None

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
    
    # Execute the code.
    code_output, code_error = bard_coder.execute_code(code)
    if code_output and code_output != None and code_output.__len__() > 0:
        display_markdown_message(f"Output: {code_output}")
        return code_output, code_error
    
    code_fixed = code
    for index in range(max_tries):
        try:
            if code_error:
                display_markdown_message(f"Code execution **failed**. **Fixing code.**")
                code_fixed = bard_coder.fix_code(code_fixed,code_error)
                if code_fixed is None:
                    display_markdown_message(f"Code **fixing** failed.- Retring")
                    continue
                code_output, code_error = bard_coder.execute_code(code_fixed)
                
                if code_output and code_output != None and code_output.__len__() > 0:
                    display_markdown_message(f"Output: {code_output}")
                    return code_output, code_error
        except Exception as exception:
            display_markdown_message(f"Error in executing code: {str(exception)}")
            if index < max_tries - 1:  # it's not the final try
                time.sleep(delay)  # delay before next try
            else:  # it's the final try
                return None
            
def remove_files():
    files_to_remove = ['graph.png', 'chart.png', 'table.md']
    for file in files_to_remove:
        try:
            if os.path.isfile(file):
                os.remove(file)
                print(f"{file} removed successfully")
        except Exception as e:
            print(f"Error in removing {file}: {str(e)}")

def bard_main() -> None:
    try:
        display_markdown_message("Welcome to **PALM - Interpreter**")
        bard_coder = setup_bard_coder()
        display_markdown_message("Enter prompt (or type '**qui**t' or '**exit**' to terminate): ")
        
        while True:
            prompt = input("> ")
            
            # Check for termination commands
            if prompt.lower() in ['quit', 'exit']:
                display_markdown_message("Terminating the program...")
                break
             
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
                    
            code = generate_code(bard_coder, prompt)
            if code is not None:
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
    bard_main()