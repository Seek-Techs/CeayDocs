from fastapi import APIRouter, UploadFile, File
from services.analyzer import analyze_drawing

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    return analyze_drawing(pdf_bytes)
