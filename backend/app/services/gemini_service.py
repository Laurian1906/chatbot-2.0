import google.generativeai as genai
from app.config.settings import generation_config
from app.config.settings import GEMINI_API_KEY

history_gemini = []

# def gemini_chat(user_message: str):
#     """
#     Generare răspuns incremental în streaming și returnare JSON.
#     """
#     genai.configure(api_key=GEMINI_API_KEY)
#     history_gemini.append({"role": "user", "parts": user_message})
    
#     # Configurăm modelul
#     model = genai.GenerativeModel(
#         model_name="gemini-1.5-flash",
#         generation_config=generation_config
#     )
    
#     # Creăm istoricul conversației
#     gemini_full_message = "\n".join([f"{msg['role']}: {msg['parts']}" for msg in history_gemini])
    
#     try:
#         # Începem sesiunea de chat
#         chat_session = model.start_chat(history=history_gemini)
        
#         # Generăm răspunsurile incremental
#         response_stream = chat_session.send_message_stream(
#             f"Respond to this message: '{gemini_full_message}' in the context of it, "
#             "do not send a resume of the conversation to the user. "
#             "Also, if necessary, put categories and emojis (do not overuse). "
#             "STICK WITH THE LANGUAGE THAT USER IS USING. "
#             "Do not explain the responses of the user that much, unless he is requesting something from you."
#         )
        
#         # Returnăm JSON la fiecare chunk de răspuns
#         for chunk in response_stream:
#             # Returnăm user și model în format JSON
#             yield {"user": user_message, "model": chunk.text}
        
#         # Salvăm răspunsul complet în istoric
#         final_response = "".join(chunk.text for chunk in response_stream)
#         history_gemini.append({"role": "model", "parts": final_response})
    
#     except Exception as e:
#         # Gestionăm eventualele erori și returnăm în format JSON
#         yield {"user": user_message, "model": f"Error with Gemini response: {e}"}

def gemini_chat(user_message: str):
    genai.configure(api_key=GEMINI_API_KEY)
    history_gemini.append({"role": "user", "parts": user_message})
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
    
    gemini_full_message = "\n".join([f"{msg['role']}: {msg['parts']}" for msg in history_gemini])
    
    try:
        chat_session = model.start_chat(history=history_gemini)
        response = chat_session.send_message(f"Respond to this message: '{gemini_full_message}' in the context of it, do not sent resume to the user about the conversation you are having with it. Also, if neccessary put categories and emojies (do not overuse). STICK WITH THE LANGUAGE THAT USER IS USING. Do not explain the responses of the user that much, unless he is requesting something from you")
        gemini_model_response = response.text
        history_gemini.append({"role": "model", "parts": gemini_model_response})
        
        return {"user": user_message, "model": gemini_model_response}
    except Exception as e:
        return {"user": user_message, "model": f"Error with Gemini response: {e}"}
    