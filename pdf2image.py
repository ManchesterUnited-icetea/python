import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
from PIL import Image

def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

def select_save_directory():
    root = tk.Tk()
    root.withdraw()
    save_dir = filedialog.askdirectory()
    return save_dir

def pdf_to_images(pdf_path, save_dir):
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(f"{save_dir}/page_{page_num+1}.png")
    print(f"Images saved to {save_dir}")

# 主程序
input_pdf_path = select_pdf_file()
if input_pdf_path:
    output_dir = select_save_directory()
    if output_dir:
        pdf_to_images(input_pdf_path, output_dir)
    else:
        print("No output directory selected.")
else:
    print("No input file selected.")
