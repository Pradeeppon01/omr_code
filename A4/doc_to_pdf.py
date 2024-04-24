from docx import Document
from docx2pdf import convert

import os
import PyPDF2
import subprocess

def docx_to_pdf(docx_path, pdf_path):
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", docx_path, "--outdir", "./output_pdf"])
    
def merge_pdfs(pdf_dir, output_path):
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

    merger = PyPDF2.PdfFileMerger()

    for pdf_file in pdf_files:
        with open(os.path.join(pdf_dir, pdf_file), "rb") as f:
            merger.append(PyPDF2.PdfFileReader(f))

    with open(output_path, "wb") as f:
        merger.write(f)
        

def pdfConversionMain():
    docx_folder = "output_doc"
    pdf_folder = "output_pdf"

    # Convert each DOCX file to a PDF file
    for docx_file in os.listdir(docx_folder):
        if docx_file.endswith(".docx"):
            docx_path = os.path.join(docx_folder, docx_file)
            pdf_path = os.path.join(pdf_folder, docx_file.replace(".docx", ".pdf"))
            docx_to_pdf(docx_path, pdf_path)

# if __name__ == "__main__":
#     docx_folder = "output_doc"
#     pdf_folder = "output_pdf"

#     # Convert each DOCX file to a PDF file
#     for docx_file in os.listdir(docx_folder):
#         if docx_file.endswith(".docx"):
#             docx_path = os.path.join(docx_folder, docx_file)
#             pdf_path = os.path.join(pdf_folder, docx_file.replace(".docx", ".pdf"))
#             docx_to_pdf(docx_path, pdf_path)

    # Merge all PDF files into a single PDF
    # merge_pdfs(pdf_folder, "output_combined.pdf")
