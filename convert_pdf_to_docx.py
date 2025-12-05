from pdf2docx import Converter
import os
from pathlib import Path
import argparse
from typing import Optional
import sys

# Configuration
BASE_DIR = Path(__file__).parent
DEFAULT_PDF_DIR = BASE_DIR / "pdfs"
DEFAULT_OUTPUT_DIR = BASE_DIR / "docx"
DEFAULT_PDF_FILE = "Executive Summary_Onshore_3004.pdf"
DEFAULT_DOCX_FILE = "Executive Summary_Onshore_3004.docx"

# Ensure directories exist
os.makedirs(DEFAULT_PDF_DIR, exist_ok=True)
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)

def convert_pdf_to_docx(pdf_path: str, output_path: str, start: int = 0, end: Optional[int] = None) -> None:
    """Convert a single PDF to DOCX with error handling."""
    try:
        cv = Converter(pdf_path)  # Remove 'with' context
        cv.convert(output_path, start=start, end=end, fancy_table=True)
        cv.close()  # Manually close to avoid resource leak
        print(f"Successfully converted {pdf_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

def convert_multiple_pdfs(pdf_dir: Path, output_dir: Path) -> None:
    """Convert all PDFs in a directory to DOCX files."""
    for pdf_file in pdf_dir.glob("*.pdf"):
        output_file = output_dir / f"{pdf_file.stem}.docx"
        convert_pdf_to_docx(str(pdf_file), str(output_file))

def create_executable() -> None:
    """Guide users to create an executable."""
    print("To create a standalone executable:")
    print("1. Install pyinstaller: pip install pyinstaller")
    print("2. Run: pyinstaller --onefile convert_to_docx.py")
    print("3. Find the .exe in the 'dist' folder and share it!")
    sys.exit(0)

def main(pdf_input: str = str(DEFAULT_PDF_DIR / DEFAULT_PDF_FILE),
         output: str = str(DEFAULT_OUTPUT_DIR / DEFAULT_DOCX_FILE),
         start_page: int = 0,
         end_page: Optional[int] = None,
         batch: bool = False,
         executable: bool = False) -> None:
    """Main function to handle conversion with command-line arguments."""
    if executable:
        create_executable()
    
    pdf_path = Path(pdf_input)
    
    if batch and pdf_path.is_dir():
        convert_multiple_pdfs(pdf_path, Path(output).parent)
    elif pdf_path.is_file():
        convert_pdf_to_docx(pdf_input, output, start_page, end_page)
    else:
        print(f"Error: {pdf_input} is not a valid file or directory. Ensure the PDF exists in {DEFAULT_PDF_DIR} or specify a valid path.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to DOCX with scalable options.")
    parser.add_argument("--input", default=str(DEFAULT_PDF_DIR / DEFAULT_PDF_FILE), help="Path to PDF file or directory")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR / DEFAULT_DOCX_FILE), help="Path to output DOCX file or directory")
    parser.add_argument("--start", type=int, default=0, help="Starting page number (0-based)")
    parser.add_argument("--end", type=int, help="Ending page number (inclusive, None for all)")
    parser.add_argument("--batch", action="store_true", help="Process all PDFs in a directory")
    parser.add_argument("--executable", action="store_true", help="Get instructions to create a standalone executable")
    
    args = parser.parse_args()
    main(args.input, args.output, args.start, args.end, args.batch, args.executable)