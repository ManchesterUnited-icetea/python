import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
from docx import Document

# 指定Tesseract的路径（仅Windows需要）
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def convert_image_to_word():
    # 打开文件对话框选择图片
    image_path = filedialog.askopenfilename(title="选择图片文件", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
    
    if not image_path:
        return
    
    try:
        # 打开图片
        image = Image.open(image_path)
        
        # 使用Tesseract执行OCR
        text = pytesseract.image_to_string(image, lang='chi_sim')
        
        # 创建一个新的Word文档
        doc = Document()
        
        # 将OCR结果添加到Word文档中
        doc.add_paragraph(text)
        
        # 保存Word文档
        save_path = filedialog.asksaveasfilename(title="保存Word文件", defaultextension=".docx", filetypes=[("Word files", "*.docx")])
        if save_path:
            doc.save(save_path)
            messagebox.showinfo("成功", "图片成功转换为Word文档")
    except Exception as e:
        messagebox.showerror("错误", f"转换过程中发生错误: {e}")

# 创建主窗口
root = tk.Tk()
root.title("图片转换为Word")

# 创建按钮并绑定函数
convert_button = tk.Button(root, text="选择图片并转换为Word", command=convert_image_to_word)
convert_button.pack(pady=20)

# 运行主循环
root.mainloop()
