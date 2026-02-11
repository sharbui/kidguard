#!/usr/bin/env python3
"""
YouTube 資訊提取器
使用 Selenium 從 YouTube 頁面的 HTML 中直接提取影片標題、頻道、描述等資訊
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class YouTubeExtractor:
    """YouTube 資訊提取器"""

    def __init__(self, headless=True):
        """
        初始化 Selenium WebDriver

        Args:
            headless: 是否以無頭模式運行（不顯示瀏覽器視窗）
        """
        self.headless = headless
        self.driver = None

    def start(self):
        """啟動瀏覽器"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--mute-audio')  # 靜音

        self.driver = webdriver.Chrome(options=chrome_options)
        print("✓ Selenium WebDriver 已啟動")

    def stop(self):
        """關閉瀏覽器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("✓ Selenium WebDriver 已關閉")

    def extract_video_info(self, video_url):
        """
        從 YouTube 影片頁面提取資訊

        Args:
            video_url: YouTube 影片 URL

        Returns:
            dict: 包含影片資訊的字典
        """
        if not self.driver:
            raise RuntimeError("WebDriver 未啟動，請先調用 start()")

        info = {
            'title': None,
            'channel': None,
            'description': None,
            'views': None,
            'url': video_url,
            'success': False
        }

        try:
            # 載入影片頁面
            self.driver.get(video_url)

            # 等待頁面載入
            wait = WebDriverWait(self.driver, 10)

            # 提取影片標題
            try:
                title_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ytd-watch-metadata yt-formatted-string"))
                )
                info['title'] = title_element.text.strip()
            except TimeoutException:
                print("⚠️  無法提取影片標題")

            # 提取頻道名稱
            try:
                channel_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-channel-name a")
                info['channel'] = channel_element.text.strip()
            except NoSuchElementException:
                print("⚠️  無法提取頻道名稱")

            # 提取影片描述（點擊展開）
            try:
                # 點擊「顯示完整資訊」按鈕
                expand_button = self.driver.find_element(By.CSS_SELECTOR, "tp-yt-paper-button#expand")
                expand_button.click()
                time.sleep(0.5)

                description_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-text-inline-expander#description-inline-expander yt-formatted-string")
                info['description'] = description_element.text.strip()
            except NoSuchElementException:
                # 如果沒有展開按鈕，嘗試直接讀取
                try:
                    description_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-text-inline-expander#description-inline-expander yt-formatted-string")
                    info['description'] = description_element.text.strip()
                except NoSuchElementException:
                    print("⚠️  無法提取影片描述")

            # 提取觀看次數
            try:
                views_element = self.driver.find_element(By.CSS_SELECTOR, "span.view-count")
                info['views'] = views_element.text.strip()
            except NoSuchElementException:
                print("⚠️  無法提取觀看次數")

            info['success'] = True

        except Exception as e:
            print(f"❌ 提取影片資訊失敗: {e}")

        return info

    def get_current_video_url(self):
        """
        獲取當前瀏覽器中的 YouTube 影片 URL

        Returns:
            str: 影片 URL，如果不是 YouTube 影片頁面則返回 None
        """
        if not self.driver:
            return None

        try:
            current_url = self.driver.current_url
            if 'youtube.com/watch?v=' in current_url:
                return current_url
        except Exception:
            pass

        return None


def main():
    """測試腳本"""
    # 創建提取器
    extractor = YouTubeExtractor(headless=False)  # 顯示瀏覽器視窗以便觀察
    extractor.start()

    try:
        # 測試 URL
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        print(f"\n正在提取影片資訊: {test_url}\n")

        # 提取資訊
        info = extractor.extract_video_info(test_url)

        # 顯示結果
        print("\n提取結果:")
        print("=" * 70)
        print(f"成功: {info['success']}")
        print(f"標題: {info['title']}")
        print(f"頻道: {info['channel']}")
        print(f"描述: {info['description'][:200] if info['description'] else None}...")
        print(f"觀看次數: {info['views']}")
        print("=" * 70)

    finally:
        # 關閉瀏覽器
        input("\n按 Enter 關閉瀏覽器...")
        extractor.stop()


if __name__ == "__main__":
    main()
