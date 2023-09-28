from os import path
import os
import time
import subprocess
from dotenv import load_dotenv
from libs.bardcoder_lib import BardCoder, traceback
from libs.sharegpt_api import sharegpt_get_url

bard_coder = None

messages = ""

def measure_accuracy(counter):
    accuracy = 1 / (counter + 1)
    accuracy_percentage = accuracy * 100
    show_output(f"Output has been fixed {counter} times with accuracy {accuracy_percentage:.0f}%")

def show_output(message):
    global messages
    messages += message + "\n"
    print(message)

def bard_execute_process(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single',rate_limiter_delay=5):
    try:
        # Additional prompt for class clarification.
        #prompt += "\n" + "Name the class code_generated for Java language."
        
        # Additional prompt for no input clarification.
        prompt += "\n" + "Dont ask the input from user.If input values are provided in code just use them. otherwise, you can hardcode the input values in code."
        
        # Setting the prompt.
        code = bard_coder.generate_code(prompt, 'python')  # Generate code using BardCoder
        if not code:
            print(f"Error no data was recieved from Server")
            return None, None, False

        # Save the code to file
        print(f"Saving code {code[:100]} to file {code_file}")
        saved_file = bard_coder.save_code(code_file)
        if saved_file:
            show_output("BardCoder: " + f"Code saved to file {saved_file}")
        else:
            show_output("BardCoder: " + "Code not saved to file")

        show_output("BardCoder: " + "Executing primary code")
        code_extension = bard_coder.get_code_extension()
        code_output = bard_coder.execute_code('offline', code,code_extension)
        
        if code_output and code_output != None and code_output.__len__() > 0:
            if 'error:' in code_output.lower():
                show_output("BardCoder: " + f"Error in executing code with exec_type {exec_type}")
                return code_output, saved_file, False

            # Check if expected output is in code output.
            if expected_output:
                if  expected_output in code_output:
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

            show_output("BardCoder: " + "Executing code choices")
            code_choices_output = bard_coder.execute_code_choices()
            code_choices_output.append(code_output)
            show_output("BardCoder: " + f"Output: {code_choices_output}")

        # Execute all the code and code choices.
        # bard_coder.execute_code_choices()

        return code_choices_output, saved_file, False

    except Exception as e:
        # show_outputf the stack trace
        stack_trace = traceback.format_exc()
        show_output("BardCoder: " + stack_trace)
        show_output("BardCoder: " + str(e))

def bard_setup_process(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single',rate_limiter_delay=5):
    
    # Append the codes directory to filename
    code_file = path.join("codes",code_file)
    
    # Start the bard coder process
    code_choices_output, saved_file, status = bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
    code_output = ""
    
    if status:
        show_output("BardCoder: " + f"Expected output found in file {saved_file}\nOutput: {code_choices_output}")
    else:
        show_output("BardCoder: " + f"Expected output not found in file {saved_file}\nOutput: {code_choices_output}")
        if code_choices_output:
            code_output = ''.join(code_choices_output)
        if code_output and code_output != None and code_output.__len__() > 0:
            test_cases_output = 0 # Test cases for output.
            # Check for errors like 'error' or 'Error' check case sensitivity and add more error checks.
            code_output = "".join(code_output)
            while 'error' in code_output.lower():
                show_output("BardCoder: " + f"Error in executing code,Trying to fix the code with error")

                # Re-prompt on error.
                code = bard_coder.fix_code(code_output, 'python')  # Fix code using BardCoder
                prompt = f"I got error while running the code {code_output}.\nPlease fix the code ``\n`{code}\n``` \nand try again.\nHere is error {code_output}\n\n" + \
                "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                # Start the bard coder process again.
                code_output, saved_file, status = bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
                # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                time.sleep(rate_limiter_delay)
                test_cases_output += 1
                
            show_output("BardCoder: " + f"Code has been fixed for error\nOutput: {code_output}")

            # Check for expected output.
            if code_output and expected_output and code_output.__len__() > 0:
                
                # While expected output does not contain in code output.
                while expected_output not in code_output:
                    show_output("BardCoder: " + f"Expected output {expected_output} not found in code\nOutput: {code_output}")

                    # Re-prompt on expected output not found.
                    code = bard_coder.fix_code(code_output, 'python')  # Fix code using BardCoder
                    prompt = f"I got output {code_output}.\nPlease fix the code ``\n`{code}\n```  \nand try again.\nHere is expected output: {code_output}\n\n" + \
                    "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                    # start the bard coder process again.
                    code_output, saved_file, status = bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
                    
                    # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                    time.sleep(rate_limiter_delay)
                    test_cases_output += 1
                    
                show_output("BardCoder: " + f"Code has been fixed for expected output\nOutput: {code_output}")
            else:
                show_output("BardCoder: " + "Not checking for code expected output")
            measure_accuracy(test_cases_output)
        else:
            show_output("BardCoder: " + "Code output is empty for error")
        return code_output

def read_prompt_from_file(prompt_file = "prompt.txt") -> str:
    prompt = ""
    with open(prompt_file, 'r') as file:
        prompt = file.read()
    return prompt

# Main method to run the bard coder.
def bard_main() -> None:
    try:
        show_output("Welcome to Bard Coder - Experimental AI Code Generator")
                
        # Clear the previous cache.
        subprocess.call(['bash', 'bash_src/clear_cache.sh'])
        
        prompt_file = str(input("Enter prompt file name [default: prompt.txt]: "))
        
        if not prompt_file or prompt_file.__len__() == 0:
            prompt_file = "prompt.txt"
            # sleep for 2 seconds.
            time.sleep(2)
            print(f"Reading prompt from file {prompt_file}")
        
        # Read the prompt from file.
        prompt = read_prompt_from_file(prompt_file)
        
        print(f"Trying to generate code for input prompt: \n{prompt}")
        time.sleep(2)
                
        # Check if prompt is empty.
        if not prompt and prompt.__len__() == 0:
            print(f"Prompt is empty in file prompt.txt")
            return None
            
        # Setting filenames for single/multiple code choices and output.
        code_file = "code_generated" # Filename of code. [Remeber no extension]
        code_choices = "code_choice" # Filename of code choices.
        expected_output = None # Expected output to check in code output.
        exec_type = 'single'  # Execution type = single/multiple. [in Multiple execution type, bard coder will generate multiple code choices]
        rate_limiter_delay = 5 # Delay in seconds to avoid rate limiting.
        share_gpt = False # Share the code on sharegpt.com
        
        # Execute the bard coder process.
        code_output = bard_setup_process(prompt, code_file, code_choices, expected_output, exec_type,rate_limiter_delay)
        sharegpt_url = ""
        
        # Adding Share button
        if share_gpt:
            if code_output is None and messages is None:
                show_output("Please run the code generator first")
            else:
                gpt_data = prompt
                human_data = ""
                if messages:
                    human_data = "Bard Logs: \n" + messages
                if code_output and len(code_output) > 0:
                    human_data += "\nOutput:\n" + code_output
                if gpt_data and human_data:
                    sharegpt_url = sharegpt_get_url(gpt_data, human_data)
                
                human_data += "\n\n[AutoBard-Coder: Repo](https://github.com/haseeb-heaven/AutoBard-Coder)"
                if len(sharegpt_url) > 0:
                    show_output(f"ShareGPT Url: {sharegpt_url}")
        
    except Exception as e:
        stack_trace = traceback.format_exc()
        show_output(stack_trace)
        show_output(str(e))

# App main entry point.
if __name__ == "__main__":
    # load the environment variables from .env file
    load_dotenv()

    # Initialize the bard coder
    api_key = os.getenv("PALMAI_API_KEY")  # get value of Secure-1PSID from .env file
    # Define guidelines as a list of strings
    guidelines = ["modular_code", "exception_handling", "error_handling", "efficient_code"]

    # Initialize the bard coder with the defined guidelines
    bard_coder = BardCoder(api_key=api_key, model="text-bison-001", temperature=0.1, max_output_tokens=2048, mode='precise', guidelines=guidelines)

    bard_main()