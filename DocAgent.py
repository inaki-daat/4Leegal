from functions import *

class DocAgent:
    def __init__(self,string,path_to_file=None):
        self.system = """You are a document agent that is in charge of the specific document you were given. You are responsible to answer questions about the document you are given. You can only answer questions or inquiries from the document."""
        if path_to_file:
            self.path_to_file = path_to_file
            self.file_text = convert_file_to_txt(path_to_file, './')
            text = "Summarize this text and make a summary that would make very easy to understand what is the document about."+self.file_text
            self.summary = summarize_text(text)
            text = "Describe the document and give me a brief description of it. ¿What elements would you be able to access if you access this"+self.file_text
            self.description = description(text)
        else:
            self.file_text = string
            text = f"Summarize the text that will be given to you  and make a summary that would make very easy to understand what is the document about. If the text is very large, try to give a summary.TEXT:[{self.file_text}]"
            self.summary = summarize_text(text)
            text =f"Describe the next text that will be given to you and give me a brief description of it. What elements would you be able to access if you access this? if the text is too large, give a brief summary.  TEXT:[{self.file_text}]"
            self.description = description(text)
            
        print("Agent created Description:"+self.description)
        print("Agent created Summary:"+self.summary)
        print("Agent created File:"+self.file_text[:1000])
    

    def ask(self,text):
        prompt=f"""
        You are a document agent, you have this file to answer questions about it.
        File : {self.file_text}

        This is the user's inquiry:
        {text}
        
        """
        response = gpt_call(text,system="You are a document agent. You are responsible to answer questions about the document you are given.")
        return response
    
    def get_summary(self):
        return self.summary
    
    def get_description(self):
        return self.description
    


