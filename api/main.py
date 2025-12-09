from fastapi import FastAPI
from api.routers import convert, compress, merge, split, extract, images

app = FastAPI(
    title="CeayDocs API",
    description="Document processing API for PDFs and Word files",
    version="1.0.0",
)

app.include_router(convert.router, prefix="/convert", tags=["Convert"])
app.include_router(compress.router, prefix="/compress", tags=["Compress"])
app.include_router(merge.router, prefix="/merge", tags=["Merge"])
app.include_router(split.router, prefix="/split", tags=["Split"])
app.include_router(extract.router, prefix="/extract", tags=["Extract"])
app.include_router(images.router, prefix="/images", tags=["Images"])