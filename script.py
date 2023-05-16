import os
import json
from bardapi import Bard

# set your __Secure-1PSID value to key
#os.environ['_BARD_API_KEY']="XXXXXXXXXXXXXXXXXX"

bard = Bard(timeout=10) # Set timeout in seconds

def bard_write_to_file(file_name:str, content:str,mode:str="w"):
    if not file_name:
        print("File name is empty")
        return
    
    if not content:
        print("Content is empty")
        return
    
    with open(file_name, mode) as f:
        f.write(content)
        f.write("\n")
        
def bard_read_from_file(file_name:str):
    if not file_name:
        print("File name is empty")
        return
    
    content = ""
    with open(file_name, "r") as f:
        content = f.read()
        
    return content

def bard_get_response(prompt:str):
    if not prompt:
        print("Prompt is empty")
        return ""
    
    response = bard.get_answer(prompt)
            
    #get respose formated as json with 4 spaces indent
    return response

def bard_get_code(response:str):
    if not response:
        print("Response is empty")
        return ""
    
    # get code from response find in response for this ``` and ``` whatever is in between is code so extract it from response and after ``` is language code so skip it will be 3 to 6 characters
    code = ""
    start = response.find("```")
    end = response.find("```", start+3)
    if start != -1 and end != -1:
        code = response[start+3:end]
    return code
    
if __name__ == "__main__":
    try:
        # set your input text
        prompt = input("Enter your prompt: ")
        response = bard_get_response(prompt)
        
        content = ""
        if response:
            content = response['content']
            
        code = bard_get_code(content)
        
        #saving the code to file called code.txt and response to response.txt
        bard_write_to_file("response.json",json.dumps(response, indent=4))
        bard_write_to_file("content.txt", content)
        code = code.replace("\\n", "\n").replace("\\t", "\t")
        bard_write_to_file("code.cpp", code)

    except Exception as e:
        print(e)
