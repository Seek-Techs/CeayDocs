from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io

from utils.merge import merge_pdfs

router = APIRouter()


@router.post("/")
async def merge_endpoint(files: list[UploadFile] = File(...)):
    pdf_bytes = await file.read()
    output = merge_pdfs(pdf_bytes)
    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=merged.pdf"}
    )
