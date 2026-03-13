```python
#!/usr/bin/env python3
"""
Excel Batch Processor - Excel批量处理器
功能：合并多表、数据清洗、格式转换
作者：littleK313
"""

import pandas as pd
import os
from pathlib import Path


class ExcelProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
    
    def merge_sheets(self, output_name="merged.xlsx"):
        """合并文件夹内所有Excel文件"""
        all_data = []
        for file in self.input_folder.glob("*.xlsx"):
            try:
                df = pd.read_excel(file)
                df['来源文件'] = file.name
                all_data.append(df)
                print(f"✓ 读取: {file.name}")
            except Exception as e:
                print(f"✗ 错误: {file.name} - {e}")
        
        if all_data:
            merged = pd.concat(all_data, ignore_index=True)
            output_path = self.output_folder / output_name
            merged.to_excel(output_path, index=False)
            return f"✅ 已合并 {len(all_data)} 个文件 → {output_path}"
        return "⚠️ 未找到Excel文件"
    
    def clean_data(self, file_path, remove_duplicates=True):
        """数据清洗：去重、去空值"""
        df = pd.read_excel(file_path)
        
        before = len(df)
        if remove_duplicates:
            df = df.drop_duplicates()
            print(f"✓ 去重: {before - len(df)} 行")
        
        df = df.dropna(how='all')
        after = len(df)
        
        output_path = self.output_folder / f"cleaned_{Path(file_path).name}"
        df.to_excel(output_path, index=False)
        
        return f"✅ 清洗完成: {before} → {after} 行 → {output_path}"
    
    def convert_format(self, file_path, target_format="csv"):
        """格式转换"""
        df = pd.read_excel(file_path)
        base_name = Path(file_path).stem
        
        if target_format == "csv":
            output_path = self.output_folder / f"{base_name}.csv"
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
        elif target_format == "json":
            output_path = self.output_folder / f"{base_name}.json"
            df.to_json(output_path, orient='records', force_ascii=False)
        
        return f"✅ 已转换: {output_path}"


def main():
    print("=" * 50)
    print("Excel批量处理器")
    print("=" * 50)
    print("1. 合并多个Excel文件")
    print("2. 清洗数据（去重、删空行）")
    print("3. 格式转换（Excel/CSV/JSON）")
    print("=" * 50)
    
    choice = input("请选择功能 (1/2/3): ")
    
    if choice == "1":
        input_dir = input("输入文件夹路径: ")
        output_dir = input("输出文件夹路径: ")
        processor = ExcelProcessor(input_dir, output_dir)
        print(processor.merge_sheets())
    
    elif choice == "2":
        file_path = input("Excel文件路径: ")
        output_dir = input("输出文件夹路径: ")
        processor = ExcelProcessor(".", output_dir)
        print(processor.clean_data(file_path))
    
    elif choice == "3":
        file_path = input("Excel文件路径: ")
        output_dir = input("输出文件夹路径: ")
        fmt = input("目标格式 (csv/json): ")
        processor = ExcelProcessor(".", output_dir)
        print(processor.convert_format(file_path, fmt))
    
    print("\n完成！按回车退出...")
    input()


if __name__ == "__main__":
    main()
