from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io

from utils.compress import compress_pdf

router = APIRouter()


@router.post("/")
async def compress_endpoint(file: UploadFile = File(...)):
    output = compress_pdf(file)
    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=compressed.pdf"}
    )
