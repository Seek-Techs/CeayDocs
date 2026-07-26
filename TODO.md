# Streamlit Application Repair

## Fixes Checklist

- [x] 1. **`utils/split.py`** — Fix legacy dispatch logic, eliminate TypeError fallthrough, fix return type
- [x] 2. **`utils/compress.py`** — Accept optional `dpi` and `quality` parameters
- [x] 3. **`app.py` — Split PDF** — Use canonical bytes API, add MIME type, handle bytes caching
- [x] 4. **`app.py` — Compress PDF** — Inline nested function, pass dpi/quality, add exception handling
- [x] 5. **`app.py` — Merge PDFs** — Add MIME type
- [x] 6. **`app.py` — PDF → Word** — Add MIME type
- [x] 7. **`app.py` — Images → PDF** — Add MIME type
- [x] 8. **`app.py` — Extract Text** — Add MIME type, encode as bytes
- [x] 9. **`app.py` — Drawing Analyzer** — Fix register CSV download to bytes, add MIME types
- [x] 10. **Run smoke tests** — Verify all fixes (9/9 passed; 7/7 unit tests passed)

