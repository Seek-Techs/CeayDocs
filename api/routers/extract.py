from fastapi import APIRouter, File, UploadFile

from utils.extract import extract_text_from_pdf

router = APIRouter()

FILE_REQUIRED = File(...)



@router.post("/")
async def extract_text_endpoint(file: UploadFile = FILE_REQUIRED):

    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    return {
        "text": text
    }
