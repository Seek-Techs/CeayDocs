from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import io

from utils.images import pdf_to_images, images_to_pdf

router = APIRouter()


@router.post("/pdf-to-images")
async def pdf_to_images_endpoint(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    output = pdf_to_images(pdf_bytes)

    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=images.zip"}
    )


@router.post("/images-to-pdf")
async def images_to_pdf_endpoint(files: list[UploadFile] = File(...)):
    images_bytes = [await f.read() for f in files]
    output = images_to_pdf(images_bytes)

    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=output.pdf"}
    )
