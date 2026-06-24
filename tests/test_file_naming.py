from __future__ import annotations

import pytest

from core.file_naming import (
    generate_compressed_filename,
    generate_converted_filename,
    generate_extracted_filename,
    generate_merged_filename,
    generate_page_filename,
    generate_resized_filename,
    generate_split_filename,
)


@pytest.mark.parametrize(
    "original, src_ext, target_ext, expected",
    [
        ("Structural Report.pdf", ".pdf", ".docx", "Structural Report_converted.docx"),
        ("Method Statement.docx", ".docx", ".pdf", "Method Statement_converted.pdf"),
    ],
)
def test_generate_converted_filename(original, src_ext, target_ext, expected):
    assert generate_converted_filename(original, src_ext=src_ext, target_ext=target_ext) == expected


@pytest.mark.parametrize(
    "original, expected",
    [
        ("Structural Report.pdf", "Structural Report_compressed.pdf"),
        ("site_photo.jpg", "site_photo_compressed.jpg"),
    ],
)
def test_generate_compressed_filename(original, expected):
    assert generate_compressed_filename(original) == expected


def test_generate_split_filename():
    assert (
        generate_split_filename("Structural Report.pdf", start=3, end=8)
        == "Structural Report_pages_3_8.pdf"
    )


def test_generate_extracted_filename():
    assert generate_extracted_filename("Structural Report.pdf") == "Structural Report_extracted.txt"


@pytest.mark.parametrize(
    "original, page_index, expected",
    [
        ("Structural Report.pdf", 1, "Structural Report_page_1.png"),
        ("Structural Report.pdf", 2, "Structural Report_page_2.png"),
    ],
)
def test_generate_page_filename(original, page_index, expected):
    assert generate_page_filename(original, page_index=page_index) == expected


def test_generate_resized_filename():
    assert generate_resized_filename("site_photo.jpg") == "site_photo_resized.jpg"


def test_generate_merged_filename():
    assert generate_merged_filename("any_input.pdf") == "merged_documents.pdf"


def test_filenames_without_extension():
    # Compression defaults to .pdf when extension is missing.
    assert generate_compressed_filename("file") == "file_compressed.pdf"
    # Extracted always uses txt.
    assert generate_extracted_filename("file") == "file_extracted.txt"
    # Split defaults to .pdf.
    assert generate_split_filename("file", start=1, end=2) == "file_pages_1_2.pdf"

