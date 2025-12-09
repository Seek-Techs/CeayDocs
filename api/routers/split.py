from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import StreamingResponse
import io

from utils.split import split_pdf

router = APIRouter()


@router.post("/")
async def split_endpoint(
    file: UploadFile = File(...),
    start: int = 1,
    end: int = 1
):
    pdf_bytes = await file.read()
    output = split_pdf(pdf_bytes, start, end)

    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=split.pdf"}
    )

