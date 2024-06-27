import docx
import pandas as pd

def extract_first_column_from_table(doc_path):
    # 打开Word文档
    doc = docx.Document(doc_path)
    
    # 存储第一列内容的列表
    first_column_data = []
    
    # 遍历文档中的所有表格
    for table in doc.tables:
        # 遍历表格中的所有行
        for row in table.rows:
            # 提取第一列的内容
            first_column_data.append(row.cells[0].text)
    
    return first_column_data

def save_to_excel(data, excel_path):
    # 将数据转换为DataFrame
    df = pd.DataFrame(data, columns=["First Column"])
    
    # 将DataFrame保存为Excel文件
    df.to_excel(excel_path, index=False)

if __name__ == "__main__":
    # 指定Word文档的路径
    word_doc_path = r'E:\附件C5 《成都天府国际机场特种作业人员登记表》-高处作业(2).docx'
    
    # 指定输出Excel文件的路径
    excel_file_path = r'E:\2.xlsx'
    
    # 提取表格第一列的内容
    first_column_data = extract_first_column_from_table(word_doc_path)
    
    # 保存提取的内容到Excel文件
    save_to_excel(first_column_data, excel_file_path)
    
    print(f"First column data has been saved to {excel_file_path}")
