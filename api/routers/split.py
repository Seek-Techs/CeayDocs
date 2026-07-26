import io

from CeayDocs.api.core.errors import bad_request
from CeayDocs.services.operations.split_ops import split_pdf_op
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

router = APIRouter()

FILE_REQUIRED = File(...)


@router.post("/")
async def split_endpoint(
    file: UploadFile = FILE_REQUIRED,
    start: int = 1,
    end: int = 1,
):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise bad_request("Only PDF files allowed")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise bad_request("Uploaded file is empty")

    output = split_pdf_op(pdf_bytes, start, end)

    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=split.pdf"},
    )

