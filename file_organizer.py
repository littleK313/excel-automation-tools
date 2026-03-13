#!/usr/bin/env python3
"""
File Organizer - 文件智能整理器
功能：按类型/日期分类、批量重命名
作者：littleK313
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


class FileOrganizer:
    def __init__(self, source_folder):
        self.source = Path(source_folder)
        self.stats = {"moved": 0, "errors": []}
    
    def organize_by_type(self):
        """按文件类型分类"""
        type_mapping = {
            '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'],
            '文档': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
            '视频': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            '音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
            '压缩': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            '代码': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php']
        }
        
        for file in self.source.iterdir():
            if file.is_file():
                for folder, extensions in type_mapping.items():
                    if file.suffix.lower() in extensions:
                        target = self.source / folder
                        target.mkdir(exist_ok=True)
                        try:
                            shutil.move(str(file), str(target / file.name))
                            self.stats["moved"] += 1
                            print(f"✓ {file.name} → {folder}/")
                        except Exception as e:
                            self.stats["errors"].append(f"{file.name}: {e}")
                        break
        
        return f"✅ 已整理 {self.stats['moved']} 个文件"
    
    def organize_by_date(self):
        """按修改日期分类"""
        for file in self.source.iterdir():
            if file.is_file():
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                date_folder = self.source / f"{mtime.year}年" / f"{mtime.month:02d}月"
                date_folder.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.move(str(file), str(date_folder / file.name))
                    self.stats["moved"] += 1
                    print(f"✓ {file.name} → {mtime.year}年/{mtime.month:02d}月/")
                except Exception as e:
                    self.stats["errors"].append(f"{file.name}: {e}")
        
        return f"✅ 已按日期整理 {self.stats['moved']} 个文件"
    
    def batch_rename(self, pattern="{name}_{index:03d}{ext}", start_index=1):
        """批量重命名"""
        files = [f for f in self.source.iterdir() if f.is_file()]
        
        for idx, file in enumerate(files, start=start_index):
            new_name = pattern.format(
                name=file.stem,
                index=idx,
                ext=file.suffix
            )
            try:
                new_path = self.source / new_name
                file.rename(new_path)
                print(f"✓ {file.name} → {new_name}")
            except Exception as e:
                self.stats["errors"].append(f"{file.name}: {e}")
        
        return f"✅ 已重命名 {len(files)} 个文件"


def main():
    print("=" * 50)
    print("文件智能整理器")
    print("=" * 50)
    print("1. 按类型分类（图片/文档/视频等）")
    print("2. 按日期分类（年/月文件夹）")
    print("3. 批量重命名")
    print("=" * 50)
    
    folder = input("要整理的文件夹路径: ")
    organizer = FileOrganizer(folder)
    
    choice = input("请选择功能 (1/2/3): ")
    
    if choice == "1":
        print(organizer.organize_by_type())
    elif choice == "2":
        print(organizer.organize_by_date())
    elif choice == "3":
        print(organizer.batch_rename())
    
    if organizer.stats["errors"]:
        print(f"\n⚠️ 错误: {len(organizer.stats['errors'])} 个")
    
    print("\n完成！按回车退出...")
    input()


if __name__ == "__main__":
    main()
