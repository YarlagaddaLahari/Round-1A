import os
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

INPUT_FILE = "input/sample.pdf"
OUTPUT_FILE = "output/sample.json"

FONT_THRESHOLD_H1 = 16.0
FONT_THRESHOLD_H2 = 12.0
FONT_THRESHOLD_H3 = 11.0
FONT_THRESHOLD_H4 = 10.0

# Helper: Check if text is a pure number or numbered like "1.", "1.2"
def is_invalid_heading(text):
    stripped = text.strip()
    return stripped.isdigit() or all(part.isdigit() for part in stripped.replace('.', '').split() if part)

# Extract PDF metadata title
def extract_pdf_title(pdf_path):
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        if hasattr(doc, 'info') and isinstance(doc.info, list) and len(doc.info) > 0:
            info = doc.info[0]
            return info.get('Title', '').decode('utf-8') if b'Title' in info else os.path.basename(pdf_path)
    return os.path.basename(pdf_path)

def extract_text_elements(pdf_path):
    elements = []
    for page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    text = text_line.get_text().strip()
                    if not text or is_invalid_heading(text):
                        continue
                    sizes = [char.size for char in text_line if isinstance(char, LTChar)]
                    avg_size = round(sum(sizes) / len(sizes), 1) if sizes else 0
                    is_bold = any('Bold' in char.fontname for char in text_line if isinstance(char, LTChar))
                    elements.append({
                        "text": text,
                        "size": avg_size,
                        "bold": is_bold,
                        "page": page_number
                    })
    return elements

def assign_headings(elements):
    outline = []

    for el in elements:
        text = el["text"]
        size = el["size"]
        bold = el["bold"]
        page = el["page"]

        if not bold:
            continue

        heading_node = {
            "text": text,
            "page": page,
            "level": ""
        }

        if size >= FONT_THRESHOLD_H1:
            heading_node["level"] = "h1"
        elif FONT_THRESHOLD_H2 <= size < FONT_THRESHOLD_H1:
            heading_node["level"] = "h2"
        elif FONT_THRESHOLD_H3 <= size < FONT_THRESHOLD_H2:
            heading_node["level"] = "h3"
        elif FONT_THRESHOLD_H4 <= size < FONT_THRESHOLD_H3:
            heading_node["level"] = "h3"  # promote small h4 as h3

        if heading_node["level"]:
            outline.append(heading_node)

    return outline

def main():
    pdf_title = extract_pdf_title(INPUT_FILE)
    elements = extract_text_elements(INPUT_FILE)
    outline = assign_headings(elements)

    os.makedirs("output", exist_ok=True)
    output = {
        "title": pdf_title,
        "outline": outline
    }

    # Write to JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Output written to {OUTPUT_FILE}")

    # ALSO print the full JSON output to Docker terminal
    print("\n📤 JSON Output:")
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
