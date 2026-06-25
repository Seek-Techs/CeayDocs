import io

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from core.file_naming import generate_converted_filename
from utils.convert import pdf_to_word

router = APIRouter()


@router.post("/pdf-to-word")
async def pdf_to_word_api(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    output_bytes = pdf_to_word(pdf_bytes)

    file_name = generate_converted_filename(
        file.filename,
        src_ext=".pdf",
        target_ext=".docx",
    )

    return StreamingResponse(
        io.BytesIO(output_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
