from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import os
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_id = str(uuid.uuid4())
    temp_file_path = f"temp_{file_id}.pdf"

    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text from PDF
    text = ""
    with fitz.open(temp_file_path) as doc:
        for page in doc:
            text += page.get_text()

    # Clean up temp file
    os.remove(temp_file_path)

    return JSONResponse(content={
        "filename": file.filename,
        "extracted_text": text[:1000]  # Just return first 1000 chars for now
    })
