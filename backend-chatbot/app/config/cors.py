from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:3000/file",
        "http://localhost:3000/file",
        "http://172.105.77.8/file",
        "http://172.105.77.8",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
