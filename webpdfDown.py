import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tqdm import tqdm
from urllib.parse import urljoin

def download_pdfs(url, save_dir):
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.content, 'html.parser')

        # 查找所有PDF链接
        pdf_links = soup.find_all('a', href=True)
        pdf_links = [link['href'] for link in pdf_links if link['href'].endswith('.pdf')]

        # Debug: 输出找到的 PDF 链接
        print("Found PDF links:")
        for link in pdf_links:
            print(link)

        # 如果没有找到PDF链接，显示提示信息
        if not pdf_links:
            messagebox.showinfo("提示", "未找到PDF链接。")
            return

        # 设置进度条最大值
        progress_bar['maximum'] = len(pdf_links)

        # 下载每个PDF文件
        for i, pdf_link in enumerate(pdf_links):
            # 如果链接是相对路径，补全为绝对路径
            pdf_link = urljoin(url, pdf_link)
            
            pdf_response = requests.get(pdf_link, stream=True)
            pdf_response.raise_for_status()  # 检查请求是否成功

            # 获取PDF文件名
            pdf_name = pdf_link.split('/')[-1]
            pdf_path = os.path.join(save_dir, pdf_name)

            # 保存PDF文件
            with open(pdf_path, 'wb') as pdf_file:
                total_size = int(pdf_response.headers.get('content-length', 0))
                chunk_size = 1024
                for data in tqdm(pdf_response.iter_content(chunk_size), total=total_size//chunk_size, unit='KB'):
                    pdf_file.write(data)

            # 更新进度条
            progress_bar['value'] = i + 1
            root.update_idletasks()

            # 显示已经下载完成的PDF文件名
            downloaded_list.insert(tk.END, pdf_name)

        messagebox.showinfo("成功", "所有PDF文件下载完成。")
    except Exception as e:
        messagebox.showerror("错误", f"下载过程中发生错误: {e}")

def select_save_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        save_dir_entry.delete(0, tk.END)
        save_dir_entry.insert(0, dir_path)

def start_download():
    url = url_entry.get()
    save_dir = save_dir_entry.get()
    if url and save_dir:
        downloaded_list.delete(0, tk.END)
        download_pdfs(url, save_dir)
    else:
        messagebox.showwarning("警告", "请输入有效的URL和保存目录。")

# 创建主窗口
root = tk.Tk()
root.title("PDF文件下载器")

# 网页URL输入框
tk.Label(root, text="网页URL:").grid(row=0, column=0, padx=10, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# 保存目录选择框
tk.Label(root, text="保存目录:").grid(row=1, column=0, padx=10, pady=5)
save_dir_entry = tk.Entry(root, width=50)
save_dir_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="浏览", command=select_save_dir).grid(row=1, column=2, padx=10, pady=5)

# 下载按钮
tk.Button(root, text="下载", command=start_download).grid(row=2, column=1, pady=20)

# 进度条
progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.grid(row=3, column=1, padx=10, pady=5)

# 已下载PDF文件列表
tk.Label(root, text="已下载PDF文件:").grid(row=4, column=0, padx=10, pady=5)
downloaded_list = tk.Listbox(root, width=50, height=10)
downloaded_list.grid(row=4, column=1, padx=10, pady=5)

root.mainloop()
