from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io

from CeayDocs.api.core.errors import bad_request

from CeayDocs.services.operations.merge_ops import merge_pdfs_op



router = APIRouter()


@router.post("/")
async def merge_endpoint(files: list[UploadFile] = File(...)):
    if not files:
        raise bad_request("No files uploaded")

    # Ensure only PDFs and read bytes into the form expected by merge_pdfs
    pdf_inputs = []
    for f in files:
        if not f.filename or not f.filename.lower().endswith(".pdf"):
            raise bad_request("Only PDF files allowed")
        b = await f.read()
        if not b:
            raise bad_request(f"Uploaded file is empty: {f.filename}")
        pdf_inputs.append(b)

    output = merge_pdfs_op(pdf_inputs)


    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=merged.pdf"},
    )

