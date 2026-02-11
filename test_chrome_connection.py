#!/usr/bin/env python3
"""測試 Chrome 連接"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    print("嘗試連接到 Chrome (端口 9222)...")
    print("正在設置 ChromeDriver...")

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # 使用 webdriver-manager 自動下載並管理 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f"✓ 連接成功！")
    print(f"當前 URL: {driver.current_url}")
    print(f"頁面標題: {driver.title}")

    driver.quit()

except Exception as e:
    print(f"❌ 連接失敗: {e}")
    print(f"\n錯誤類型: {type(e).__name__}")
    import traceback
    traceback.print_exc()
