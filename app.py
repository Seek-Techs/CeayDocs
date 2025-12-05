import streamlit as st
from utils.convert import pdf_to_word, word_to_pdf
from utils.merge import merge_pdfs
from utils.split import split_pdf
from utils.compress import compress_pdf
from utils.extract import extract_text
from utils.images import pdf_to_images, images_to_pdf
from pathlib import Path
import io
from utils.compress import _find_ghostscript

# paths
ASSETS = Path(__file__).parent / "assets"
LOGO_LIGHT = ASSETS / "ceaydocs_logo_light.png"
LOGO_DARK  = ASSETS / "ceaydocs_logo_dark.png"
SVG_LIGHT  = ASSETS / "ceaydocs_logo_light.svg"
SVG_DARK   = ASSETS / "ceaydocs_logo_dark.svg"

# --- theme CSS blocks ---
light_css = """
:root{
  --primary: #006B3D;
  --accent: #DAA520;
  --bg: #F7F4EC;
  --card: #FFFFFF;
  --text: #1E1E1E;
  --muted: #7A7A7A;
}
.stApp {
  background-color: var(--bg);
}
.css-1d391kg { background-color: var(--bg); } /* body override (may change between streamlit versions) */
"""

dark_css = """
:root{
  --primary: #00A368;
  --accent: #DAA520;
  --bg: #121212;
  --card: #1E1E1E;
  --text: #EDEDED;
  --muted: #CCCCCC;
}
.stApp {
  background-color: var(--bg);
  color: var(--text);
}
"""

# theme selector (sidebar)
st.sidebar.title("CeayDocs")
theme_choice = st.sidebar.radio("🌗 Theme", ["Light", "Dark"], index=0)

# inject CSS & select logo
if theme_choice == "Light":
    st.markdown(f"<style>{light_css}</style>", unsafe_allow_html=True)
    logo_path = LOGO_LIGHT if LOGO_LIGHT.exists() else SVG_LIGHT
else:
    st.markdown(f"<style>{dark_css}</style>", unsafe_allow_html=True)
    logo_path = LOGO_DARK if LOGO_DARK.exists() else SVG_DARK

# show logo (respects both PNG & SVG)
try:
    st.sidebar.image(str(logo_path), width=160)
except Exception:
    # fallback: show text if image not available
    st.sidebar.markdown("## CeayDocs\n_document tools_")

# small branded footer in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 CeayDocs — Built by Yusuff O. Sikiru")

st.set_page_config(page_title="Document Tools", page_icon="📄", layout="wide")

st.title("📄 Document Toolkit")
st.write("A simple multi-tool web application to help you process PDF and Word documents.")

menu = st.sidebar.selectbox(
    "Choose a tool",
    [
        "PDF → Word",
        "Word → PDF",
        "Merge PDFs",
        "Split PDF",
        "Compress PDF",
        "PDF → Images",
        "Images → PDF",
        "Extract Text from PDF"
    ]
)

# ===== PDF → Word =====
if menu == "PDF → Word":
    uploaded = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded:
        with st.spinner("Converting..."):
            output = pdf_to_word(uploaded)
        st.success("Done!")
        st.download_button("Download Word File", output, file_name="converted.docx")

# ===== Word → PDF =====
elif menu == "Word → PDF":
    uploaded = st.file_uploader("Upload Word File", type=["docx"])
    if uploaded:
        with st.spinner("Converting..."):
            output = word_to_pdf(uploaded)
        st.success("Done!")
        st.download_button("Download PDF File", output, file_name="converted.pdf")

# ===== Merge PDFs =====
elif menu == "Merge PDFs":
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        with st.spinner("Merging..."):
            output = merge_pdfs(uploaded_files)
        st.download_button("Download Merged PDF", output, file_name="merged.pdf")

# ===== Split PDF =====
elif menu == "Split PDF":
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf:
        start = st.number_input("Start Page", min_value=1, value=1)
        end = st.number_input("End Page", min_value=1, value=1)
        if st.button("Split"):
            with st.spinner("Splitting..."):
                output = split_pdf(pdf, start, end)
            st.download_button("Download Split PDF", output, file_name="split.pdf")

# ===== Compress PDF =====
elif menu == "Compress PDF":
    
    def compression_ui():
        st.header("📦 Compress PDF")

        uploaded = st.file_uploader("Upload PDF", type=["pdf"])

        if uploaded:
            pdf_bytes = uploaded.read()
            original_size = len(pdf_bytes)

            st.info(f"Original file size: **{original_size / 1024:.2f} KB**")

            st.subheader("Compression Settings")

            preset = st.selectbox(
                "Select Compression Level",
                [
                    "🔵 High Quality (Large File)",
                    "🟢 Medium (Balanced)",
                    "🟡 Low (Small File)",
                    "🔴 Extreme (Minimum Size)"
                ]
            )

            # Map preset to internal DPI + quality
            preset_map = {
                "🔵 High Quality (Large File)": (180, 80),
                "🟢 Medium (Balanced)": (150, 60),
                "🟡 Low (Small File)": (120, 40),
                "🔴 Extreme (Minimum Size)": (100, 25),
            }

            dpi, quality = preset_map[preset]

            st.write(f"DPI: **{dpi}** | JPEG Quality: **{quality}%**")

            # Detect compressor type
            if _find_ghostscript():
                st.success("Using Ghostscript (best compression).")
            else:
                st.warning("Ghostscript not available — using fallback compressor.")

            if st.button("🔧 Compress Now"):
                with st.spinner("Compressing PDF... Please wait ⏳"):
                    output_bytes = compress_pdf(
                        io.BytesIO(pdf_bytes),   # pass file-like object
                    )

                compressed_size = len(output_bytes)
                ratio = compressed_size / original_size

                st.success("Compression successful!")

                st.write(f"**New size:** {compressed_size / 1024:.2f} KB")
                st.write(f"**Compression ratio:** {ratio:.2%}")

                st.download_button(
                    label="⬇️ Download Compressed PDF",
                    data=output_bytes,
                    file_name="compressed.pdf",
                    mime="application/pdf",
                )
    compression_ui()

# ===== PDF → Images =====
elif menu == "PDF → Images":
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf:
        with st.spinner("Extracting images..."):
            images = pdf_to_images(pdf)  # returns list[BytesIO]
        # create a ZIP for download
        from io import BytesIO as _BytesIO
        import zipfile as _zipfile
        zip_buf = _BytesIO()
        with _zipfile.ZipFile(zip_buf, "w") as z:
            for i, img in enumerate(images):
                img.seek(0)
                z.writestr(f"page_{i+1}.png", img.read())
        zip_buf.seek(0)
        st.download_button("Download Images ZIP", zip_buf.read(), file_name="images.zip")

# ===== Images → PDF =====
elif menu == "Images → PDF":
    imgs = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if imgs:
        with st.spinner("Converting..."):
            output = images_to_pdf(imgs)
        st.download_button("Download PDF", output, file_name="images_to_pdf.pdf")

# ===== Extract Text =====
elif menu == "Extract Text from PDF":
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf:
        with st.spinner("Extracting text..."):
            text = extract_text(pdf)
        st.text_area("Extracted Text", text, height=400)
        st.download_button("Download Text File", text, file_name="text.txt")
