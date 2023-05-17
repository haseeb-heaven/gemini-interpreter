import os
import json
from bardapi import Bard
from bardcoder import BardCoder
import traceback

# set your __Secure-1PSID value to key
#os.environ['_BARD_API_KEY']="XXXXXXXXXXXXXXXXXX"

bard = Bard(timeout=10) # Set timeout in seconds

def bard_get_response(prompt:str):
    if not prompt:
        print("Prompt is empty")
        return ""
    
    response = bard.get_answer(prompt)
            
    #get respose formated as json with 4 spaces indent
    return response
    
if __name__ == "__main__":
    try:
        # set your input text
        prompt = input("Prompt: ")
        response = bard_get_response(prompt)
        bard_coder = BardCoder(json.dumps(response, indent=4))
                
        content = ""
        if response:
            content = response['content']
            
        code = bard_coder.get_content(content)
        
        #saving the code to file called code.txt and response to response.txt
        bard_coder.save_code("response.json",json.dumps(response, indent=4))
        bard_coder.save_code("content.txt", content)
        code = code.replace("\\n", "\n").replace("\\t", "\t")
        bard_coder.save_code("code.py", code)
        
        # You can now access the properties of the bard_coder object
        print("Content is : " + bard_coder.content)
        print("Conversation ID is : " + bard_coder.conversation_id)
        print("Response ID is : " + bard_coder.response_id)
        # print("Factuality Queries are : ")
        # for factualityQuery in bard_coder.factualityQueries:
        #     print(str(factualityQuery))
        
        links = bard_coder.get_links(bard_coder.factualityQueries)
        print("Links are : ",str(links))
        
        print("Text Query is : " + str(bard_coder.textQuery))
        
        print("Choices are : ")
        for index, choice in enumerate(bard_coder.choices):
            choice_content = bard_coder.get_choice_content(index)
            bard_coder.save_code("code_choice"+str(index)+".py", choice_content)

    except Exception as e:
        # print the stack trace
        stack_trace = traceback.format_exc()
        print(stack_trace)
        # print the error message
        print(str(e))
