import PyPDF2
import sys


def merge_pdf(result_file, pdf_list):
    merger = PyPDF2.PdfMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    merger.write(result_file)


def add_watermark(result_file, watermark_file):
    pdf_reader = PyPDF2.PdfReader(result_file)
    watermark_reader = PyPDF2.PdfReader(watermark_file)
    pdf_writer = PyPDF2.PdfWriter()

    watermark_page = watermark_reader.pages[0]

    for i, _page in enumerate(pdf_reader.pages):
        pdf_page = pdf_reader.pages[i]
        pdf_page.merge_page(watermark_page)
        pdf_writer.add_page(pdf_page)
    with open(result_file, "wb") as output_file:
        pdf_writer.write(output_file)


RESULT_FILE = "./result/result.pdf"
inputs = sys.argv[1:]
merge_pdf(RESULT_FILE, inputs)
add_watermark(RESULT_FILE, "./wtr.pdf")
