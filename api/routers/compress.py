import io

from CeayDocs.api.core.errors import bad_request
from CeayDocs.services.operations.compress_ops import compress_pdf_op
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

router = APIRouter()

FILE_REQUIRED = File(...)


@router.post("/")
async def compress_endpoint(file: UploadFile = FILE_REQUIRED):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise bad_request("Only PDF files allowed")

    data = await file.read()
    if not data:
        raise bad_request("Uploaded file is empty")

    output = compress_pdf_op(data)


    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=compressed.pdf"},
    )

