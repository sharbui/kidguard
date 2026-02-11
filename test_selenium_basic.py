#!/usr/bin/env python3
"""基本 Selenium 測試"""

import sys
print("Python version:", sys.version)

try:
    print("\n1. 導入 selenium...")
    from selenium import webdriver
    print("   ✓ selenium 導入成功")

    print("\n2. 導入 webdriver_manager...")
    from webdriver_manager.chrome import ChromeDriverManager
    print("   ✓ webdriver_manager 導入成功")

    print("\n3. 下載 ChromeDriver...")
    driver_path = ChromeDriverManager().install()
    print(f"   ✓ ChromeDriver 路徑: {driver_path}")

    print("\n4. 創建 Chrome 選項...")
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    print("   ✓ Chrome 選項創建成功")

    print("\n5. 啟動 Chrome（無頭模式）...")
    from selenium.webdriver.chrome.service import Service
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("   ✓ Chrome 啟動成功")

    print("\n6. 測試訪問網頁...")
    driver.get("https://www.google.com")
    print(f"   ✓ 頁面標題: {driver.title}")

    print("\n7. 關閉瀏覽器...")
    driver.quit()
    print("   ✓ 關閉成功")

    print("\n✅ 所有測試通過！")

except Exception as e:
    print(f"\n❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
