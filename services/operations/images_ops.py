from __future__ import annotations

from utils.images import pdf_to_images, images_to_pdf


def pdf_to_images_op(pdf_bytes: bytes) -> bytes:
    return pdf_to_images(pdf_bytes)


def images_to_pdf_op(image_bytes_list: list[bytes]) -> bytes:
    return images_to_pdf(image_bytes_list)

