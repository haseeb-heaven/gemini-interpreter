
from os import path
from bard_coder import BardCoder, traceback, json
import time

# Initialize the bard coder
bard_coder = BardCoder(enable_logs=True)
rate_limiter_delay = 5

# #%%
# saved_file = "code_generated.java"
# code_output = bard_coder.execute_code(saved_file)

def bard_execute_process(prompt, filename='code.txt', code_choices='code_choice', expected_output=None, exec_type='single'):
    try:
        bard_coder.set_prompt(prompt)

        # Get the code from the response.
        code = bard_coder.get_code()
        filename = path.join("codes", "code_generated")
        # Save the code to file
        saved_file = bard_coder.save_code(filename, code)
        if saved_file:
            print(f"Code saved to file {saved_file}")
        else:
            print("Code not saved to file")

        print("Executing primary code")
        code_output = bard_coder.execute_code(saved_file)
        if code_output:
            if 'error:' in code_output.lower():
                print(f"Error in executing code with exec_type {exec_type}")
                return code_output, saved_file, False

            # Check if expected output is in code output.
            if expected_output in code_output:
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
            bard_coder.save_code_choices("code_choice")

            print("Executing code choices")
            code_choices_output = bard_coder.execute_code_choices()
            code_choices_output.append(code_output)
            print(f"Output: {code_choices_output}")

        # Execute all the code and code choices.
        # bard_coder.execute_code_choices()

        return code_choices_output, saved_file, False

    except Exception as e:
        # print the stack trace
        stack_trace = traceback.format_exc()
        print(stack_trace)
        print(str(e))


if __name__ == "__main__":
    try:
        # Set the prompt
        print("Welcome to Bard Coder - Experimental AI Code Generator")

        # prompt = input("Prompt: ")
        prompt = """
2. Implementing the Levenshtein distance algorithm: .  Give me full source code in Java with main method included and dont explain anything in output.
- Description: Write a program to implement the Levenshtein distance algorithm for computing the edit distance between two strings.
- Input: Strings "kitten" and "sitting".
- Expected output: The Levenshtein distance between the two strings is 3.
        """
        
        # Additional prompt for class clarification.
        prompt += "\n" + "Name the class code_generated for Java and C# languages."
        
        # Additional prompt for no input clarification.
        prompt += "\n" + "Dont ask the input from user.If input values are provided in code just use them. otherwise, you can hardcode the input values in code."
        
        # Setting filenames for single/multiple code choices and output.
        filename = path.join("codes", "code_generated")
        code_choices = "code_choice"
        expected_output = '3'
        exec_type = 'single'  # single/multiple
        # biggest prime number from 1 to 1000 is 997

        # Start the bard coder process
        code_choices_output, saved_file, status = bard_execute_process(prompt, filename, code_choices, expected_output, exec_type)
        if status:
            print(f"Expected output found in file {saved_file}\nOutput: {code_choices_output}")
        else:
            print(f"Expected output not found in file {saved_file}\nOutput: {code_choices_output}")
            code_output = ''.join(code_choices_output)
            if code_output and code_output != None and code_output.__len__() > 0:
                # Check for errors like 'error' or 'Error' check case sensitivity and add more error checks.
                while 'error' in code_output.lower():
                    print(f"Error in executing code\nTrying to fix the code with error")

                    # Re-prompt on error.
                    code = bard_coder.get_code()
                    prompt = f"I got error while running the code {code_output}.\nPlease fix the code ``\n`{code}\n``` \nand try again.\nHere is error {code_output}\n\nNote:Only give me fixed and updated code in output and nothing else."

                    # Start the bard coder process again.
                    code_output, saved_file, status = bard_execute_process(prompt, filename, code_choices, expected_output, exec_type)
                    # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                    time.sleep(rate_limiter_delay)
                print("Code has been fixed for error")

                # Check for expected output.
                if code_output and code_output != None and code_output.__len__() > 0:
                    # While expected output does not contain in code output.
                    while expected_output not in code_output:
                        print(f"Expected output {expected_output} not found in code\nOutput: {code_output}")

                        # Re-prompt on expected output not found.
                        code = bard_coder.get_code()
                        prompt = f"I got output {code_output}.\nPlease fix the code ``\n`{code}\n```  \nand try again.\nHere is expected output: {code_output}\n\nNote:Only give me fixed and updated code in output and nothing else."

                        # start the bard coder process again.
                        code_output, saved_file, status = bard_execute_process(
                            prompt, filename, code_choices, expected_output, exec_type)
                        # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
                        time.sleep(rate_limiter_delay)
                    print("Code has been fixed for expected output")
                else:
                    print("Code output is empty for expected output")
            else:
                print("Code output is empty for error")

    except Exception as e:
        # print the stack trace
        stack_trace = traceback.format_exc()
        print(stack_trace)
        print(str(e))

# %%
