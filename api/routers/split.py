import io

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from utils.split import split_pdf

router = APIRouter()

FILE_REQUIRED = File(...)



@router.post("/")
async def split_endpoint(
    file: UploadFile = FILE_REQUIRED,
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

