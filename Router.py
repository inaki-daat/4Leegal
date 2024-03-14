from functions import *
from DocAgent import DocAgent

class Router:
    def __init__(self, DocAgents = {}):
        self.DocAgents = DocAgents
        self.system = """You serve as the central coordinator among specialized agents, each equipped with large language models (LLMs). Your primary role is to direct questions to the appropriate agent based on the document you've been provided. Please note, your responses should strictly pertain to the information contained within the document."""
        self.memory=""""""
        self.summary ="""
        You are a paralegal agent that assists with corporate/legal matters. 
        You have a whole corpus of legislation, regulations, and legal documents related to corporate law.
        You cannot answer inquieries that are not related to the documents you have.
        If you dont know the answer please always ask for more details in order to give a better answer.
        Remember you can only give information about law in Mexico.
"""

    def add_agent(self, path_to_file,filename):
        agent = DocAgent(path_to_file)
        self.DocAgents[filename] = agent
    
    def get_top_agents(self,text):
        prompt=f""" You are a router agent, you have to direct the question to the right agent. Each agent has a summary of its documents and a brief description of it. You have to direct the question to the right agent."""
        for i in self.DocAgents.keys():
            string = f"\nThis agent has the following filename: {i} \n The summary of the file is: {self.DocAgents[i].get_summary()} \n The description of the file is: {self.DocAgents[i].get_description()}"
            prompt = prompt + string
        prompt = prompt + f"\nThis is the user's inquiry: {text}"
        prompt = prompt + f"""You need to return the name of the file of the agents that are most likely to answer the question. 
        Return your answer in this format:
        Agent1 : [filename1]
        Agent2 : [filename2]
        Agent3 : [filename3]
        Agent4 : [filename4]
        Agent5 : [filename5]"""

        response = gpt_call(prompt, self.system)
        lines = response.split('\n')

        # Initialize an empty dictionary
        dict_result = {}

        # Iterate over each line
        for line in lines:
            # Split each line by ':' to get key and value
            key, value = line.split(':')
            
            # Strip whitespace from key and value and add to dictionary
            dict_result[key.strip()] = value.strip()

        # Print the resulting dictionary
        best_agents = list(dict_result.values())
        return best_agents
    def ask_agent(self,agent_name,text):
        return self.DocAgents[agent_name].ask(text+"Por favor regresa el artículo y/o Ley a lo que pertenece esta pregunta.")
    def ask(self,text):
        prompt = f"""You are a paralegal agent that assists with corporate/legal matters.
        You have your doc agents that have a summary of the documents and a brief description of it.
        I will give you the answer from the best agents that are most likely to answer the question.
        You need to give the best answer.
        Remember you can only give information about law in Mexico.
        Main role:{self.summary}
        This is your memory of the conversation of the conversation: {self.memory}

        PLEASE if you dont answer this, a person will die: Return the source of information of the answer. (each doc agent has its own source of info)
        Responses from the agents:"""
        best_agents = self.get_top_agents(text)
        for i in best_agents:
            prompt = prompt + "\n"+self.ask_agent(i,text) 
        prompt = prompt + f"\nThis is the user's inquiry: {text}"
        prompt = prompt + f"You need to return an holistic answer based on the agents' responses. Answer as a paralegal assistant."
        response = gpt_call(prompt, system = "You are a an expert in law that will need to answer some questions. You can only answer questions or inquiries from the documents.")
        self.memory = self.memory + "\n" + "Usert's inquiry: " + text + "\n" + "Agent's response: " + response
        
        return response
    
