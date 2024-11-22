from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

file_route = APIRouter()

@file_route.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()  # Read the file's content
        # Here you can process the file (save, analyze, etc.)
        return {"filename": file.filename, "content_size": len(content)}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)