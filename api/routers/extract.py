from fastapi import APIRouter, UploadFile, File

from utils.extract import extract_text_from_pdf

router = APIRouter()


@router.post("/")
async def extract_text_endpoint(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    return {
        "text": text
    }
