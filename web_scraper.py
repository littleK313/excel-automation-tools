#!/usr/bin/env python3
"""
Web Scraper - 网页数据爬虫
功能：抓取表格/列表数据，导出Excel
作者：littleK313
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin


class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_tables(self, url):
        """抓取页面所有表格"""
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            
            print(f"✓ 找到 {len(tables)} 个表格")
            
            results = []
            for idx, table in enumerate(tables):
                try:
                    df = pd.read_html(str(table))[0]
                    results.append({
                        'index': idx,
                        'data': df,
                        'rows': len(df),
                        'columns': len(df.columns)
                    })
                    print(f"  表格 {idx}: {len(df)} 行 × {len(df.columns)} 列")
                except Exception as e:
                    print(f"  表格 {idx}: 解析失败 - {e}")
            
            return results
        except Exception as e:
            print(f"✗ 请求失败: {e}")
            return []
    
    def export_to_excel(self, tables, filename="scraped_data.xlsx"):
        """导出到Excel"""
        if not tables:
            print("⚠️ 没有数据可导出")
            return
        
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for item in tables:
                    sheet_name = f"Table_{item['index']}"
                    item['data'].to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"✅ 已导出: {filename}")
            print(f"   包含 {len(tables)} 个表格")
        except Exception as e:
            print(f"✗ 导出失败: {e}")


def main():
    print("=" * 50)
    print("网页数据爬虫")
    print("=" * 50)
    print("功能：抓取网页表格数据，导出Excel")
    print("注意：只抓取公开数据，遵守网站规则")
    print("=" * 50)
    
    url = input("请输入网页URL: ")
    
    scraper = WebScraper()
    tables = scraper.scrape_tables(url)
    
    if tables:
        filename = input("保存文件名 (默认: scraped_data.xlsx): ") or "scraped_data.xlsx"
        scraper.export_to_excel(tables, filename)
    else:
        print("未能抓取到表格数据")
    
    print("\n完成！按回车退出...")
    input()


if __name__ == "__main__":
    main()
