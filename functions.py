
import openai
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')



def convert_files_to_txt(source_folder_path, output_base_folder):
    print(f"Converting files from {source_folder_path} to {output_base_folder}")
    
    # Ensure the output base folder exists
    os.makedirs(output_base_folder, exist_ok=True)
    
    # Walking through the source folder and its subfolders
    for root, dirs, files in os.walk(source_folder_path):
        for file in files:
            # Construct the path to the original file
            original_file_path = os.path.join(root, file)
            
            # Construct the relative path of the file from the source folder
            relative_path = os.path.relpath(original_file_path, source_folder_path)
            
            # Define the new file name with .txt extension and construct the new file path
            new_file_name = os.path.splitext(relative_path)[0] + '.txt'
            new_file_path = os.path.join(output_base_folder, new_file_name)
            
            # Ensure the directory for the new file exists
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            
            try:
                # Read the original file
                with open(original_file_path, 'r', encoding='utf-8') as original_file:
                    content = original_file.read()
                    
                # Write the content to a new .txt file
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(content)
                    
                print(f"Converted {original_file_path} to {new_file_path}")
                
            except Exception as e:
                print(f"Error processing file {original_file_path}: {e}")

def convert_file_to_txt(source_file_path, output_base_folder):
    print(f"Converting file from {source_file_path} to {output_base_folder}")
    
    # Ensure the output base folder exists
    os.makedirs(output_base_folder, exist_ok=True)
    
    # Construct the new file name with .txt extension and construct the new file path
    file_name = os.path.basename(source_file_path)
    new_file_name = os.path.splitext(file_name)[0] + '.txt'
    new_file_path = os.path.join(output_base_folder, new_file_name)
    
    content = ""  # Initialize content variable to hold file contents
    
    try:
        # Read the original file
        with open(source_file_path, 'r', encoding='utf-8') as original_file:
            content = original_file.read()
        
        # Write the content to a new .txt file
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(content)
        
        print(f"Converted {source_file_path} to {new_file_path}")
        
    except Exception as e:
        print(f"Error processing file {source_file_path}: {e}")
    
    return content  

def summarize_text(text):
    response = gpt_call(text, system="You are a document agent. You are responsible to answer questions about the document you are given. You can only answer questions or inquiries from the document.")
    return response
def description(text):
    response = gpt_call(text, system="You are a document agent. You are responsible to answer questions about the document you are given. You can only answer questions or inquiries from the document.")
    return response
def gpt_call(prompt, system):
    client = OpenAI()
    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": prompt},
                        ]
                    )
    response = response.choices[0].message.content
    return response
