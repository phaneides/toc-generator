```markdown
# TOC Generator

Extract and apply structured tables of contents (TOCs) to scanned PDFs using Gemini and PyMuPDF.

## Features

- Extract TOC pages from a PDF
- Use Gemini 2.5 Flash to convert TOC images to structured data
- Apply the TOC directly to the original PDF
- Supports page offset and automatic "Content" marker

## Usage

1. Install dependencies:

    ```bash
    pip install google-generativeai pymupdf
    ```

2. Create `config.py` with your API key:

    ```python
    GOOGLE_API_KEY = "your-api-key-here"
    ```

3. Create a JSON descriptor in `tocs/`:

    ```json
    {
      "toc_pages": [3, 6],
      "offset": 10,
      "file_path": "~/Books/book.pdf"
    }
    ```

4. Run the pipeline:

    ```bash
    python process_toc.py
    ```

The result will be saved as `TOC_book.pdf`.

## Notes

- Requires `pdftoppm` (from poppler-utils)
```

