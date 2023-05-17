from bardcoder import BardCoder,traceback,json

if __name__ == "__main__":
    try:
        # set your input text
        prompt = input("Prompt: ")
        bard_coder = BardCoder(prompt,enable_logs=True)
        
        # You can now access the properties of the bard_coder object
        print("Text Query is : " + str(bard_coder.textQuery))
        print("Content is : " + bard_coder.content)
        print("Conversation ID is : " + bard_coder.conversation_id)
        print("Response ID is : " + bard_coder.response_id)
        links = bard_coder.get_links(bard_coder.factualityQueries)
        print("Links are : ", str(links))
        
        # Save the code to file
        bard_coder.save_code()

    except Exception as e:
        # print the stack trace
        stack_trace = traceback.format_exc()
        print(stack_trace)
        print(str(e))
