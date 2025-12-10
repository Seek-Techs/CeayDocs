# app.py (full file - main Streamlit app)
import streamlit as st
from utils.convert import pdf_to_word, word_to_pdf
from utils.merge import merge_pdfs
from utils.split import split_pdf
from utils.compress import compress_pdf
from utils.extract import extract_text_from_pdf
from utils.images import pdf_to_images, images_to_pdf
from services.drawing_index import generate_index, generate_qa, index_to_csv
from services.analyzer import analyze_drawing
from services.drawing_register import build_register
import pandas as pd
from pathlib import Path
import io
from utils.compress import _find_ghostscript
import hashlib
import fitz
from io import BytesIO
from PIL import Image

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
        "Extract Text from PDF",
        "Drawing Analyzer (AEC)"
    ]
)

# ===== PDF → Word =====
if menu == "PDF → Word":
    uploaded = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded:
        with st.spinner("Converting..."):
            pdf_bytes = uploaded.read()
            output = pdf_to_word(pdf_bytes)
        st.success("Done!")
        st.download_button("Download Word File", output, file_name="converted.docx")

# ===== Word → PDF =====
elif menu == "Word → PDF":
    uploaded = st.file_uploader("Upload Word File", type=["docx"])
    if uploaded:
        with st.spinner("Converting..."):
            docx_bytes  = uploaded.read()
            output = word_to_pdf(docx_bytes)

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
                pdf_bytes = pdf.read()
                output = split_pdf(pdf_bytes, start, end)
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
            text = extract_text_from_pdf(pdf)
        st.text_area("Extracted Text", text, height=400)
        st.download_button("Download Text File", text, file_name="text.txt")

# ===== Drawing Analyzer (AEC) =====
elif menu == "Drawing Analyzer (AEC)":
    st.header("🏗 Engineering Drawing Analyzer (AEC)")

    uploaded_file = st.file_uploader(
        "Upload an engineering drawing (PDF)",
        type=["pdf"],
        key="drawing_analyzer"
    )

    if uploaded_file:
        # Read uploaded bytes and compute hash to detect new upload
        pdf_bytes = uploaded_file.read()
        pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()

        # If new upload (or no state), run analyzer and initialize drawing_state
        if "drawing_state" not in st.session_state or st.session_state.drawing_state.get("source_hash") != pdf_hash:
            with st.spinner("Analyzing drawing..."):
                try:
                    result = analyze_drawing(pdf_bytes)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    st.stop()

            # initialize canonical editable model and clear overrides
            st.session_state.drawing_state = {
                "pages": [p.copy() for p in result.get("pages", [])],
                "raw": result,
                "split_pdfs": result.get("split_pdfs", {}),
                "source_hash": pdf_hash
            }
            st.session_state.overrides = {}  # reset overrides on new upload
        else:
            # reuse existing state & raw
            result = st.session_state.drawing_state.get("raw", {})

        # now canonical pages variable (single source of truth)
        pages = st.session_state.drawing_state["pages"]

        # --- Rule Validation (derived from pages) ---
        st.subheader("📋 Rule Validation")
        # note: rule_check might originally come from analyzer.raw; but we re-evaluate via generate_qa on current pages
        index = generate_index(pages)
        qa = generate_qa(index)
        rule_check = result.get("rule_check", {})  # keep original if present
        # show rule_check status from analyzer if available, else use our QA verdict
        status = rule_check.get("status") or ("PASS" if not qa.get("missing_views") and not qa.get("scale_issues") else "FAIL")

        if status == "PASS":
            st.success("✅ Drawing set satisfies project rules")
        elif status == "FAIL":
            st.error("❌ Drawing validation failed")
            for issue in (rule_check.get("issues", []) or qa.get("scale_issues", []) or []):
                st.write(f"• {issue}")
        else:
            st.warning("Rules not applied")

        # Detected Drawing Scales (from canonical pages)
        st.subheader("Detected Drawing Scales")
        for p in pages:
            st.markdown(f"• **Page {p.get('page')}** — {p.get('view_type')} — **Scale: {p.get('scale')}**")

        # Engineer Corrections (form) - widgets have unique keys, overrides applied only on submit
        st.subheader("🛠 Engineer Corrections")

        # ensure overrides dict exists
        st.session_state.setdefault("overrides", {})

        with st.form("correction_form"):
            # create inputs for each page (keys unique)
            for p in pages:
                page_num = p.get("page")
                if page_num is None:
                    # skip invalid pages
                    continue

                with st.expander(f"Page {page_num}"):
                    # prepare default index safely
                    options = ["PLAN", "SECTION", "ELEVATION", "DETAIL", "COVER PAGE", "STRUCTURAL NOTE PAGE"]
                    current_view = p.get("view_type", "PLAN")
                    try:
                        default_index = options.index(current_view) if current_view in options else 0
                    except Exception:
                        default_index = 0

                    st.selectbox(
                        "View Type",
                        options,
                        index=default_index,
                        key=f"view_type_page_{page_num}"
                    )

                    st.text_input(
                        "Scale",
                        value=p.get("scale", ""),
                        key=f"scale_page_{page_num}"
                    )

            submitted = st.form_submit_button("✅ Apply Corrections")

        # When submitted, gather widget values and persist overrides, then apply to canonical pages
        if submitted:
            # build overrides dict from widget state
            new_overrides = {}
            for p in pages:
                page_num = p.get("page")
                if page_num is None:
                    continue
                new_view = st.session_state.get(f"view_type_page_{page_num}")
                new_scale = st.session_state.get(f"scale_page_{page_num}")
                # compare to canonical
                if new_view != p.get("view_type") or (new_scale or "") != (p.get("scale") or ""):
                    new_overrides[page_num] = {"view_type": new_view, "scale": new_scale}
                else:
                    # remove any existing override for this page if it matches canonical
                    if page_num in st.session_state.get("overrides", {}):
                        st.session_state.overrides.pop(page_num, None)

            # replace overrides in session state (keep other pages unchanged)
            st.session_state.overrides.update(new_overrides)

            # apply overrides to canonical pages
            for idx, p in enumerate(st.session_state.drawing_state["pages"]):
                ov = st.session_state.overrides.get(p.get("page"))
                if ov:
                    st.session_state.drawing_state["pages"][idx].update(ov)

            # recompute derived artifacts
            pages = st.session_state.drawing_state["pages"]
            index = generate_index(pages)
            qa = generate_qa(index)

            st.success("Corrections applied and locked in")

        # Detected Drawing Views (use canonical pages)
        st.subheader("Detected Drawing Views")
        for p in pages:
            badge_color = {
                "PLAN": "🟦",
                "SECTION": "🟥",
                "ELEVATION": "🟩",
                "UNKNOWN": "⬜"
            }.get(p.get("view_type"), "⬜")
            st.markdown(f"**Page {p.get('page')}** → {badge_color} `{p.get('view_type')}`")

        # Download Separated Drawings (use raw split_pdfs or canonical pages if your splitter supports pages)
        st.subheader("Download Separated Drawings")
        split_map = st.session_state.drawing_state.get("split_pdfs", {}) or {}
        for name, pdf_bytes in split_map.items():
            if not pdf_bytes:
                continue
            st.download_button(
                label=f"⬇️ Download {name.upper()} PDF",
                data=pdf_bytes,
                file_name=f"{name}.pdf",
                mime="application/pdf"
            )

        # Drawing Preview (Page 1)
        st.subheader("Drawing Preview (Page 1)")
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            page0 = doc[0]
            pix = page0.get_pixmap(dpi=120)
            image = Image.open(BytesIO(pix.tobytes("png")))

            st.image(
                image,
                caption="Page 1 Preview",
                width='stretch'
            )
        except Exception:
            st.info("Could not render page preview.")

        # Drawing Index and CSV download (derived from canonical pages)
        st.subheader("Drawing Index")
        index = generate_index(pages)
        if index:
            df = pd.DataFrame(index)
            st.dataframe(df)

            csv_text = index_to_csv(index)
            # ensure bytes for download button to avoid media-store issues
            st.download_button(
                "⬇️ Download Index CSV",
                data=csv_text.encode("utf-8"),
                file_name="drawing_index.csv",
                mime="text/csv"
            )
        else:
            st.info("No index available")

        st.subheader("📘 Drawing Register")

        register = build_register(
            index=result.get("index", []),
            project_code="CEAY-001",
            revision="A"
        )

        if register:
            df_reg = pd.DataFrame(register)
            st.dataframe(df_reg)

            csv = df_reg.to_csv(index=False)
            st.download_button(
                "⬇️ Download Drawing Register",
                csv,
                file_name="drawing_register.csv",
                mime="text/csv"
            )
        else:
            st.info("No register entries available.")


        # QA Summary (derived)
        st.subheader("QA Summary")
        qa = generate_qa(index)
        if qa:
            if qa.get("missing_views"):
                st.warning(f"Missing views: {', '.join(qa['missing_views'])}")
            if qa.get("scale_issues"):
                for issue in qa["scale_issues"]:
                    st.warning(issue)
            if qa.get("low_confidence_pages"):
                st.info("Low confidence pages:")
                for p in qa["low_confidence_pages"]:
                    st.write(f"• Page {p.get('page')} — {p.get('view_type')} (conf={p.get('confidence')})")
        else:
            st.write("No QA issues detected.")

        