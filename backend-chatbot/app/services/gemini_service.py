from app.config.settings import generation_config, GEMINI_API_KEY
import google.generativeai as genai
import os
from datetime import datetime, timedelta
import threading

data_directory = "./uploads"
history_gemini = []
pending_deletions = {}
conversation_title = None
file_path = ''

def delete_files():
    files_deleted = False 
    if os.path.exists(data_directory):
        if not os.listdir(data_directory): 
            print("DEBUG: Nu sunt fișiere încărcate.")
            return None  
        else:
            for filename in os.listdir(data_directory):
                file_path = os.path.join(data_directory, filename)
                try:
                    os.remove(file_path)
                    files_deleted = True
                    print(f"DEBUG: Fișierul `{filename}` a fost șters.")
                except Exception as e:
                    print(f"Error ștergând fișierul `{filename}`: {e}")
            return files_deleted 
    else:
        print(f"DEBUG: Directorul `{data_directory}` nu există.")
        return False 
def auto_delete_files():
    while True:
        if os.path.exists(data_directory):
            for filename in os.listdir(data_directory):  
                file_path = os.path.join(data_directory, filename) 
                try:
                    last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if datetime.now() - last_modified_time > timedelta(hours=1):
                        os.remove(file_path)
                        print(f"File '{file_path}' has been automatically deleted after one hour.")
                except Exception as e:
                    print(f"Error while trying to delete file '{file_path}': {e}")
            
threading.Thread(target=auto_delete_files, daemon=True).start()

def gemini_chat(user_message: str):
    global conversation_title
    gemini_message = "\n".join([f"{msg['role']}: {msg['parts']}" for msg in history_gemini])

    genai.configure(api_key=GEMINI_API_KEY)
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
    
    history_gemini.append({"role": "user", "parts": user_message})
    
    uploaded_files = [] 

    print(f"Checking directory: {data_directory}")
    if os.path.exists(data_directory):
        print(f"Directory exists: {data_directory}")
        for filename in os.listdir(data_directory):
            print(f"Found file: {filename}")
            if filename.endswith(".txt"):
                print(f"Processing file: {filename}")
                file_path = os.path.join(data_directory, filename)
                try:
                    if not any(file["filename"] == filename for file in uploaded_files):
                        print(f"Uploading file: {filename}")
                        with open(file_path, "r", encoding="utf-8") as file:
                            content = file.read().strip()
                        print(f"Read content for {filename}")
                        uploaded_file = genai.upload_file(file_path)
                        print(f"Uploaded file result: {uploaded_file}")
                        uploaded_files.append({"filename": filename, "content": content})
                        print(f"Uploaded files: {uploaded_files}")
                    else:
                        print(f"File '{filename}' already uploaded.")
                except Exception as e:
                    print(f"Error processing file '{filename}': {e}")
    else:
        print(f"Directory '{data_directory}' does not exist.")
    complete_message = f"{gemini_message}\n"
    
    if uploaded_files:
        files_names = [file["filename"] for file in uploaded_files]
        content_of_file = [file["content"] for file in uploaded_files]
        
        file_info = "\n".join([f"File: {name}\nContent: {content}" for name, content in zip(files_names, content_of_file)])

        complete_message += f"Keep in mind these files:\n{file_info}\n and any information you already know. If the user is asking you about a topic from those file and you got the information from them please do include a footer where you cite the files uploaded and any sources you got the information from, else.. please do not bother or bore the user with the info that it hasn't been requested. ANSWER ALL THE QUESTIONS THAT USER IS ASKING DESPITE THE FACT THEY ARE NOT ABOUT THE FILES. Do not provide the whole content, you can't=)) All the links you provide send them in this form: [text of the link goes here](link goes here)."
    else:
        print("No valid .txt file found or file is empty.")
    
    try:
        chat_session = model.start_chat(history=history_gemini)
        response = chat_session.send_message(f"Respond to this message: '{complete_message}' in the context of it. Stick with the language user is using and be polite. Answer to this message in the context of the user prompt which is: {user_message}. If the user asks about the files uploaded share them to it! If the user asks to change the title please just change it and tell him that the title has been changed put at the end of your message 'title:title_of_the_conversation' without quotes please do not translate the quoted thing in any language let in english. Do not complain about the fact that you didn't actually change the title, roleplay as if you did. Do not request the user to tell you a title for the conversation. If the user requests the title of the conversation put 'title: (title_of_conversation_goes_here)' (without quotes) at the end of your message and everytime user requests that the title to change remember to put title:(title_goes_here) at the end of your message. If the user requests a title do the same thing with 'title:(users_requested_title) at the end of your message. If you ask the user if there is anything that you can do for him and they answer no or something like no, please wave at him and say that they have a nice day or something like that.")
        gemini_model_response = response.text
        history_gemini.append({"role": "model", "parts": gemini_model_response})
            
        if conversation_title is None or user_message.__contains__("Modifica titlul acestei conversatii"):
            if "title:" in gemini_model_response:
                start_index = gemini_model_response.index("title:") + len("title:")
                end_index = gemini_model_response.find("\n", start_index)
                if end_index == -1:
                    end_index = len(gemini_model_response)
                conversation_title = gemini_model_response[start_index:end_index].strip()
                gemini_model_response = (
                    gemini_model_response[:start_index - len("title:")] + gemini_model_response[end_index:]
                ).strip()
                
                print("Title extracted:", conversation_title)
            else:
                print("No 'title:' found in response.")
        
        if "title:" in gemini_model_response:
            start_index = gemini_model_response.index("title:") + len("title:")
            end_index = gemini_model_response.find("\n", start_index)
            if end_index == -1:
                end_index = len(gemini_model_response)
            gemini_model_response = (
                gemini_model_response[:start_index - len("title:")] + gemini_model_response[end_index:]
            ).strip()
            print("Removed 'title:' from the response.")
            # conversation_title = gemini_model_response[:start_index - len("title:")] + gemini_model_response[end_index:]
            
        if "Sterge fisierele incarcate" in user_message:
            call = delete_files()
            if call is True:
                message1 = "Files deleted!"
                chat_session.send_message(f"Please translate in the user's language this: '{message1}' and send ONLY THE TRANSLATED MESSAGE")
            elif call is False:
                message2 = "Directory does not exist."
                chat_session.send_message(f"Please translate in the user's language this: '{message2}' and send ONLY THE TRANSLATED MESSAGE")
            else:
                message3 = "No uploaded files to delete."
                chat_session.send_message(f"Please translate in the user's language this: '{message3}' and send ONLY THE TRANSLATED MESSAGE")
        
        return {"user": user_message, "model": gemini_model_response, "title": conversation_title}
    except Exception as e:
        return {"user": user_message, "model": f"Error with Gemini response: {e}"}
