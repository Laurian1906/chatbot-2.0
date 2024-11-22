import google.generativeai as genai
from app.config.settings import generation_config
from app.config.settings import GEMINI_API_KEY
from app.routes.file_route import upload_file

history_gemini = []

def gemini_chat(user_message: str):
    genai.configure(api_key=GEMINI_API_KEY)
    history_gemini.append({"role": "user", "parts": user_message})
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
    
    gemini_full_message = "\n".join([f"{msg['role']}: {msg['parts']}" for msg in history_gemini])
    print("File content: ", upload_file)
    try:
        chat_session = model.start_chat(history=history_gemini)
        response = chat_session.send_message(f"Respond to this message: '{gemini_full_message}' in the context of it, do not sent resume to the user about the conversation you are having with it. Also, if neccessary put categories and emojies (do not overuse). STICK WITH THE LANGUAGE THAT USER IS USING. Do not explain the responses of the user that much, unless he is requesting something from you")
        gemini_model_response = response.text
        history_gemini.append({"role": "model", "parts": gemini_model_response})
        
        return {"user": user_message, "model": gemini_model_response}
    except Exception as e:
        return {"user": user_message, "model": f"Error with Gemini response: {e}"}
    