**Adobe India Hackathon - Round 1A Submission Solution Overview**-This project extracts the heading structure (outline) from a PDF document based on font size, bold styling, and logical heading hierarchy. The extracted output is saved as a JSON file and also printed directly inside the Docker terminal when executed.

**Approach**-The main idea is to extract bold text from a PDF and classify it as:
             h1 – Main Titles (Font size ≥ 16.0)
             h2 – Section Headings (12.0 ≤ Font size < 16.0)
             h3 – Sub-Headings (11.0 ≤ Font size < 12.0)
             h4 (promoted) – Deep subheadings (10.0 ≤ Font size < 11.0)
**Libraries Used** - pdfminer.six – for parsing PDF and extracting layout, font sizes, bold info.
                     os, json – Python standard libraries for file handling and JSON operations.

**Key Featres** - Extracts the important heading and subheading in under 60 seconds Works entirely offline (no network dependencies) Memory efficient (<1GB RAM usage) Produces standardized JSON output.

**System Requirements** - Docker (with Linux containers) AMD64 architecture 16GB RAM recommended 5GB disk space
                          CPU architecture: amd64 (x86_64)
                          No GPU dependencies
                          Model size (if used) ≤ 200MB
                          Should work offline — no network/internet calls

**Project Structure** - pdf-outline-extractor/
                                ├── Dockerfile
                                ├── requirements.txt
                                ├── main.py
                                ├── input/          # Place your .pdf files here
                                └── output/         # JSON files will be saved here
                                
**Build & Execution Instructions**
1. Prerequisites Ensure you have: Docker installed and running Input PDFs placed in ./input directory Valid pdfs in inpbut folder and make sure that docker file is created and present or not.
Structure of Docker file: FROM python:3.10-slim
                          WORKDIR /app
                          COPY requirements.txt .
                          RUN pip install --no-cache-dir -r requirements.txt
                          COPY . .
                          CMD ["python", "main.py"]
2. Build Docker Image: Open a terminal inside the project folder and run:
                     ---> docker build -t pdf-outline-extractor .
3. Run the Container: Ensure the PDF file is inside the input/ folder, then run:
                     ---> docker run --rm -v "%cd%:/app" pdf-outline-extractor
   this will process the Process input/sample.pdf and Create output/sample.json

**Example Output**
{
  "title": "Optimizing Database Queries",
  "outline": {
      "text": "PROJECT REPORT",
      "page": 1,
      "level": "h1"
    },
    {
      "text": "INTRODUCTION",
      "page": 2,
      "level": "h2"
    },
    {
      "text": "Features",
      "page": 3,
      "level": "h3"
    }
  ]
}



