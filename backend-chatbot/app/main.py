from fastapi import FastAPI
from .config.cors import setup_cors
from .routes.gemini_routes import gemini_router
from .routes.openai_routes import openai_router
from .routes.file_route import file_route

app = FastAPI()

# Configure CORS
setup_cors(app)

app.include_router(gemini_router, prefix="/gemini")
app.include_router(openai_router, prefix="/openai")
app.include_router(file_route, prefix="/file")

if __name__ == "__main__":
    print("Script is running from main.py!")