import io

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from utils.images import images_to_pdf, pdf_to_images

router = APIRouter()

FILE_REQUIRED = File(...)



@router.post("/pdf-to-images")
async def pdf_to_images_endpoint(file: UploadFile = FILE_REQUIRED):

    pdf_bytes = await file.read()
    output = pdf_to_images(pdf_bytes)

    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=images.zip"}
    )


@router.post("/images-to-pdf")
async def images_to_pdf_endpoint(files: list[UploadFile] = FILE_REQUIRED):

    images_bytes = [await f.read() for f in files]
    output = images_to_pdf(images_bytes)

    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=output.pdf"}
    )
