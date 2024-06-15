import rarfile
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_rar_file(rar_filename, extract_dir):
    with rarfile.RarFile(rar_filename) as rf:
        # 获取 RAR 文件中的文件列表
        file_list = rf.namelist()
        
        # 逐个解压文件到指定目录
        for file in file_list:
            rf.extract(file, path=extract_dir)

def main():
    # 创建 Tkinter 根窗口并隐藏
    root = tk.Tk()
    root.withdraw()

    # 请求用户选择要解压的RAR文件
    rar_filename = filedialog.askopenfilename(filetypes=[("RAR files", "*.rar")])
    if not rar_filename:
        messagebox.showwarning("选择错误", "未选择RAR文件")
        return

    # 请求用户选择解压目录
    extract_dir = filedialog.askdirectory()
    if not extract_dir:
        messagebox.showwarning("选择错误", "未选择解压目录")
        return

    # 解压文件
    try:
        extract_rar_file(rar_filename, extract_dir)
        messagebox.showinfo("解压完成", "RAR文件解压成功")
    except Exception as e:
        messagebox.showerror("解压失败", f"解压RAR文件时出现错误: {e}")

if __name__ == "__main__":
    main()
