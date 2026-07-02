from fastapi import APIRouter, File, UploadFile

from services.analyzer import analyze_drawing

router = APIRouter()

FILE_REQUIRED = File(...)


@router.post("/analyze")
async def analyze(file: UploadFile = FILE_REQUIRED):

    pdf_bytes = await file.read()
    return analyze_drawing(pdf_bytes)
