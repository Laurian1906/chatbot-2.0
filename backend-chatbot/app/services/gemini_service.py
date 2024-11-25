import google.generativeai as genai
from app.config.settings import generation_config, GEMINI_API_KEY
import os
from datetime import datetime, timedelta
import threading
import time

data_directory = "uploads"
history_gemini = []
pending_deletions = {}

def delete_old_files():
    while True:
        if os.path.exists(data_directory):
            for filename in os.listdir(data_directory):
                file_path = os.path.join(data_directory, filename)
                if os.path.isfile(file_path):
                    try:
                        last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if datetime.now() - last_modified_time > timedelta(hours=1):
                            os.remove(file_path)
                            print(f"File '{file_path}' has been automatically deleted after one hour.")
                    except Exception as e:
                        print(f"Error while trying to delete file '{file_path}': {e}")
        time.sleep(3600)

threading.Thread(target=delete_old_files, daemon=True).start()

def gemini_chat(user_message: str):
    gemini_message = "\n".join([f"{msg['role']}: {msg['parts']}" for msg in history_gemini])

    genai.configure(api_key=GEMINI_API_KEY)
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
    
    history_gemini.append({"role": "user", "parts": user_message})
    
    uploaded_files = []  # This will store file names or identifiers of the uploaded files

    if os.path.exists(data_directory):
        for filename in os.listdir(data_directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(data_directory, filename)
                try:
                    # Only upload file if not already uploaded
                    if filename not in uploaded_files:
                        # Open the file and read its content
                        with open(file_path, "r", encoding="utf-8") as file:
                            content = file.read().strip()  # Read the content of the file

                        # Upload the file to the Gemini model
                        #uploaded_file = genai.upload_file(file_path)
                        
                        # Store the filename and content in the uploaded_files list
                        uploaded_files.append({"filename": filename, "content": content})

                except Exception as e:
                    print(f"Error reading file '{filename}': {e}")

    # Build the message to be sent to Gemini
    complete_message = f"{gemini_message}\n"
    
    if uploaded_files:
        # Extrage numele fișierelor și conținutul lor
        files_names = [file["filename"] for file in uploaded_files]
        content_of_file = [file["content"] for file in uploaded_files]
        
        # Crează un mesaj cu numele fișierului și conținutul acestuia
        file_info = "\n".join([f"File: {name}\nContent: {content}" for name, content in zip(files_names, content_of_file)])

        complete_message += f"Keep in mind these files:\n{file_info}\n and any information you already know. Please reference them when asked about them. Do not provide the whole content, you can't=)) All the links you provide send them in this form: [text of the link goes here](link goes here)"
    else:
        print("No valid .txt file found or file is empty.")
    
    try:
        chat_session = model.start_chat(history=history_gemini)
        response = chat_session.send_message(f"Respond to this message: '{complete_message}' in the context of it. Stick with the language user is using and be polite. Answer to this message in the context of the user prompt which is: {user_message}. If the user asks about the files uploaded share them to it!")
        gemini_model_response = response.text
        history_gemini.append({"role": "model", "parts": gemini_model_response})
        
        return {"user": user_message, "model": gemini_model_response}
    except Exception as e:
        return {"user": user_message, "model": f"Error with Gemini response: {e}"}
