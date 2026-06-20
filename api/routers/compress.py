from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io

from CeayDocs.api.core.errors import bad_request

from CeayDocs.services.operations.compress_ops import compress_pdf_op



router = APIRouter()


@router.post("/")
async def compress_endpoint(file: UploadFile = File(...)):
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

