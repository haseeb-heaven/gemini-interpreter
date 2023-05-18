from os import path
from bardcoder import BardCoder,traceback,json


if __name__ == "__main__":
    try:
        # Initialize the bard coder
        bard_coder = BardCoder(enable_logs=True)
        
        # Set the prompt
        print("Welcome to Bard Coder - Experimental AI Code Generator")
        prompt = input("Prompt: ")
        bard_coder.set_prompt(prompt)
        
        # Get the code from the response.
        code = bard_coder.get_code()
        filename = path.join("codes","code_generated")
        # Save the code to file
        filename = bard_coder.save_code(filename,code)
        print(f"Code saved to file {filename}")
        
        # Save all the code choices to file
        #bard_coder.save_code_choices("code_choice")
        
        # Print the links
        links = bard_coder.get_links()
        print(f"Links: {links}")
         
        code_output = bard_coder.execute_code(filename)
        
        # Execute all the code and code choices.
        #bard_coder.execute_code_choices()
        
    except Exception as e:
        # print the stack trace
        stack_trace = traceback.format_exc()
        print(stack_trace)
        print(str(e))
