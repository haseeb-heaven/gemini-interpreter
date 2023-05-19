from os import path
from bard_coder import BardCoder,traceback,json
import time

# Initialize the bard coder
bard_coder = BardCoder(enable_logs=True)

def bard_execute_process(prompt,filename='code.txt',code_choices='code_choice',output=None):
    try:
        bard_coder.set_prompt(prompt)

        # Get the code from the response.
        code = bard_coder.get_code()
        filename = path.join("codes","code_generated")
        # Save the code to file
        saved_file = bard_coder.save_code(filename,code)
        print(f"Code saved to file {saved_file}")

        # Save all the code choices to file
        #bard_coder.save_code_choices("code_choice")

        # Print the links
        #links = bard_coder.get_links()
        #print(f"Links: {links}")
            
        code_output = bard_coder.execute_code(saved_file)
        
        # Execute all the code and code choices.
        #bard_coder.execute_code_choices()
        
        return code_output

    except Exception as e:
        # print the stack trace
        stack_trace = traceback.format_exc()
        print(stack_trace)
        print(str(e))

if __name__ == "__main__":
    try:
        # Set the prompt
        print("Welcome to Bard Coder - Experimental AI Code Generator")
        
        #prompt = input("Prompt: ")
        prompt = """
        Problem: Write a program in C++ to find the first non-repeating character in a string.  Give me full source code with main method included.
        Input: Given a string s = “leetcode” 
        """
        # Setting filenames for single/multiple code choices and output.
        filename = path.join("codes","code_generated")
        code_choices = "code_choice"
        
        # Start the bard coder process
        code_output = bard_execute_process(prompt,filename,code_choices)
        
        if code_output:
            # Check for errors like 'error' or 'Error' check case sensitivity and add more error checks.
            while 'error' in code_output or 'Error' in code_output:
                print(f"Error in executing code\n,Trying to fix the code with error {code_output}")
                
                # Re-prompt on error.
                code = bard_coder.get_code()
                prompt = f"I got error while running the code {code_output}.\nPlease fix the code {code} \nand try again.\nHere is error {code_output}"
                
                # Start the bard coder process again.
                code_output = bard_execute_process(prompt,filename,code_choices)
                time.sleep(5) # Sleep for 5 seconds before re-prompting. Dont get Rate limited.
            print(f"Code has been fixed Output: {code_output}")
        
        
    except Exception as e:
        # print the stack trace
        stack_trace = traceback.format_exc()
        print(stack_trace)
        print(str(e))


