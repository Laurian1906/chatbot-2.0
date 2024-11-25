from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from io import BytesIO
from pdfminer.high_level import extract_text
import os

file_route = APIRouter()

UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@file_route.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_data = await file.read()

        if file.filename.endswith(".pdf"):
            pdf_stream = BytesIO(file_data) 
            text_extracted = extract_text(pdf_stream)

            file_path = os.path.join(UPLOAD_DIRECTORY, f"{os.path.splitext(file.filename)[0]}.txt")

            with open(file_path, "w") as f:
                f.write(text_extracted)
        else:
            text_extracted = file_data.decode('utf-8')  

        print("File loaded!!!", {"filename": file.filename, "content": len(text_extracted)})
        return {"filename": file.filename, "content": text_extracted}
    except Exception as e:
        print("Error with the file!", {e})
        return JSONResponse(content={"error": str(e)}, status_code=500)
