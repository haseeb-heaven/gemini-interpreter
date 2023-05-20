from os import path
from bard_coder import BardCoder, traceback
import time

# Initialize the bard coder
bard_coder = BardCoder(enable_logs=True)

def measure_accuracy(counter):
    accuracy = 1 / (counter + 1)
    accuracy_percentage = accuracy * 100
    print(f"Output has been fixed {counter} times with accuracy {accuracy_percentage:.0f}%")


def auto_bard_execute_process(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single',rate_limiter_delay=5):
    try:
        # Additional prompt for class clarification.
        prompt += "\n" + "Name the class code_generated for Java and C# languages."
        
        # Additional prompt for no input clarification.
        prompt += "\n" + "Dont ask the input from user.If input values are provided in code just use them. otherwise, you can hardcode the input values in code."
        
        # Setting the prompt.
        bard_coder.set_prompt(prompt)

        # Get the code from the response.
        code = bard_coder.get_code()
        # Save the code to file
        saved_file = bard_coder.save_code(code_file, code)
        if saved_file:
            print("BardCoder: " + f"Code saved to file {saved_file}")
        else:
            print("BardCoder: " + "Code not saved to file")

        print("BardCoder: " + "Executing primary code")
        code_output = bard_coder.execute_code(saved_file)
        if code_output and code_output != None and code_output.__len__() > 0:
            if 'error:' in code_output.lower():
                print("BardCoder: " + f"Error in executing code with exec_type {exec_type}")
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

            print("BardCoder: " + "Executing code choices")
            code_choices_output = bard_coder.execute_code_choices()
            code_choices_output.append(code_output)
            print("BardCoder: " + f"Output: {code_choices_output}")

        # Execute all the code and code choices.
        # bard_coder.execute_code_choices()

        return code_choices_output, saved_file, False

    except Exception as e:
        # printf the stack trace
        stack_trace = traceback.format_exc()
        print("BardCoder: " + stack_trace)
        print("BardCoder: " + str(e))

def auto_bard_setup_process(prompt, code_file='code.txt', code_choices='code_choice', expected_output=None, exec_type='single',rate_limiter_delay=5):
    
    # Append the codes directory to filename
    code_file = path.join("codes",code_file)
    
    # Start the bard coder process
    code_choices_output, saved_file, status = auto_bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
    
    if status:
        print("BardCoder: " + f"Expected output found in file {saved_file}\nOutput: {code_choices_output}")
    else:
        print("BardCoder: " + f"Expected output not found in file {saved_file}\nOutput: {code_choices_output}")
        if code_choices_output:
            code_output = ''.join(code_choices_output)
        if code_output and code_output != None and code_output.__len__() > 0:
            test_cases_output = 0 # Test cases for output.
            # Check for errors like 'error' or 'Error' check case sensitivity and add more error checks.
            code_output = "".join(code_output)
            while 'error' in code_output.lower():
                print("BardCoder: " + f"Error in executing code,Trying to fix the code with error")

                # Re-prompt on error.
                code = bard_coder.get_code()
                prompt = f"I got error while running the code {code_output}.\nPlease fix the code ``\n`{code}\n``` \nand try again.\nHere is error {code_output}\n\n" + \
                "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                # Start the bard coder process again.
                code_output, saved_file, status = auto_bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
                # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                time.sleep(rate_limiter_delay)
                test_cases_output += 1
                
            print("BardCoder: " + f"Code has been fixed for error\nOutput: {code_output}")

            # Check for expected output.
            if code_output and expected_output and code_output.__len__() > 0:
                
                # While expected output does not contain in code output.
                while expected_output not in code_output:
                    print("BardCoder: " + f"Expected output {expected_output} not found in code\nOutput: {code_output}")

                    # Re-prompt on expected output not found.
                    code = bard_coder.get_code()
                    prompt = f"I got output {code_output}.\nPlease fix the code ``\n`{code}\n```  \nand try again.\nHere is expected output: {code_output}\n\n" + \
                    "Note:The output should only be fixed code and nothing else. No explanation or anything else."

                    # start the bard coder process again.
                    code_output, saved_file, status = auto_bard_execute_process(prompt, code_file, code_choices, expected_output, exec_type)
                    
                    # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                    time.sleep(rate_limiter_delay)
                    test_cases_output += 1
                    
                print("BardCoder: " + f"Code has been fixed for expected output\nOutput: {code_output}")
            else:
                print("BardCoder: " + "Not checking for code expected output")
            measure_accuracy(test_cases_output)
        else:
            print("BardCoder: " + "Code output is empty for error")

if __name__ == "__main__":
    try:
        print("Welcome to Bard Coder - Experimental AI Code Generator")

        #prompt = input("Prompt: ")
        prompt = """
        Write a program to print sum of prime numbers between 1 to 100 in C++ using vectors and list and maps.
        Show me different ways to print the output.
        """
        
        # Setting filenames for single/multiple code choices and output.
        code_file = "code_generated" # Filename of code. [Remeber no extension]
        code_choices = "code_choice" # Filename of code choices.
        expected_output = None # Expected output to check in code output.
        exec_type = 'single'  # Execution type = single/multiple. [in Multiple execution type, bard coder will generate multiple code choices]
        rate_limiter_delay = 5 # Delay in seconds to avoid rate limiting.
        
        auto_bard_setup_process(prompt, code_file, code_choices, expected_output, exec_type,rate_limiter_delay)

    except Exception as e:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        print(str(e))