from __future__ import annotations

from pathlib import Path


def _stem_and_suffix(path: str | Path) -> tuple[str, str]:
    p = Path(path)
    # Handle paths like ".bashrc" where stem can be empty.
    suffix = p.suffix
    if suffix:
        return p.stem, suffix
    return p.name, ""


def _ensure_file_name(original: str | Path) -> str:
    p = Path(original)
    # Preserve only the filename component.
    return p.name


def _append_suffix_to_stem(stem: str, suffix: str) -> str:
    return f"{stem}{suffix}"


def generate_converted_filename(original: str | Path, *, src_ext: str, target_ext: str) -> str:
    """PDF/Word conversion naming.

    Example:
      Structural Report.pdf -> Structural Report_converted.docx
      Method Statement.docx -> Method Statement_converted.pdf
    """
    original_name = _ensure_file_name(original)
    stem, _ = _stem_and_suffix(original_name)

    # Apply only the policy suffix; keep extension from target_ext.
    target_ext = target_ext if target_ext.startswith(".") else f".{target_ext}"
    return f"{stem}_converted{target_ext}"


def generate_compressed_filename(original: str | Path) -> str:
    """PDF compression naming.

    Example: Structural Report.pdf -> Structural Report_compressed.pdf
    """
    original_name = _ensure_file_name(original)
    stem, suffix = _stem_and_suffix(original_name)
    if not suffix:
        suffix = ".pdf"
    return f"{stem}_compressed{suffix}"


def generate_split_filename(original: str | Path, *, start: int, end: int) -> str:
    """Split PDF page range naming.

    Example: Structural Report.pdf, 3-8 -> Structural Report_pages_3_8.pdf
    """
    original_name = _ensure_file_name(original)
    stem, suffix = _stem_and_suffix(original_name)
    if not suffix:
        suffix = ".pdf"
    return f"{stem}_pages_{start}_{end}{suffix}"


def generate_extracted_filename(original: str | Path) -> str:
    """Extract text naming.

    Example: Structural Report.pdf -> Structural Report_extracted.txt
    """
    original_name = _ensure_file_name(original)
    stem, _ = _stem_and_suffix(original_name)
    return f"{stem}_extracted.txt"


def generate_page_filename(original: str | Path, *, page_index: int, page_ext: str = ".png") -> str:
    """PDF page image filename.

    Example: Structural Report.pdf page 1 -> Structural Report_page_1.png
    """
    original_name = _ensure_file_name(original)
    stem, _ = _stem_and_suffix(original_name)
    page_ext = page_ext if page_ext.startswith(".") else f".{page_ext}"
    return f"{stem}_page_{page_index}{page_ext}"


def generate_merged_filename(original: str | Path) -> str:
    """Merged PDF naming.

    Example: merged_documents.pdf

    Note: since merged output is logically independent of source filenames,
    we provide a default deterministic name when original is a source name.
    """
    # If caller passes a name that is already descriptive, we still normalize
    # to the repo-specified default output file.
    return "merged_documents.pdf"


def generate_resized_filename(original: str | Path, *, ext: str | None = None) -> str:
    """Image resize naming.

    Example: site_photo.jpg -> site_photo_resized.jpg
    """
    original_name = _ensure_file_name(original)
    stem, suffix = _stem_and_suffix(original_name)
    if ext is not None:
        suffix = ext if ext.startswith(".") else f".{ext}"
    if not suffix:
        suffix = ".jpg"
    return f"{stem}_resized{suffix}"

