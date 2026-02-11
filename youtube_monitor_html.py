#!/usr/bin/env python3
"""
KidGuard - Live Monitor with HTML Extraction
使用 Chrome DevTools Protocol 連接到已打開的 Chrome，直接從 HTML 提取影片資訊
"""

import time
from pathlib import Path
from datetime import datetime
import mss
import mss.tools
from PIL import Image

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class LiveMonitorHTML:
    """使用 HTML 提取的即時監控系統"""

    def __init__(self):
        self.monitoring = False
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.check_interval = 2  # 每 2 秒檢查一次
        self.capture_count = 0
        self.last_video_id = None  # 追蹤上一個影片 ID
        self.driver = None

    def connect_to_chrome(self, debug_port=9222):
        """
        連接到已打開的 Chrome 瀏覽器

        使用方法：
        1. 先關閉所有 Chrome 視窗
        2. 用以下指令啟動 Chrome：
           chrome.exe --remote-debugging-port=9222

        Args:
            debug_port: Chrome 的除錯端口（預設 9222）
        """
        if not SELENIUM_AVAILABLE:
            print("❌ 需要安裝 Selenium: uv pip install selenium")
            return False

        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")

            self.driver = webdriver.Chrome(options=chrome_options)
            print(f"✓ 已連接到 Chrome (端口 {debug_port})")
            return True

        except Exception as e:
            print(f"❌ 連接 Chrome 失敗: {e}")
            print("\n請確保：")
            print("1. 已關閉所有 Chrome 視窗")
            print("2. 用以下指令啟動 Chrome：")
            print("   chrome.exe --remote-debugging-port=9222")
            return False

    def extract_video_info(self):
        """從當前 YouTube 頁面提取影片資訊"""
        if not self.driver:
            return None

        info = {
            'video_id': None,
            'title': None,
            'channel': None,
            'description': None,
            'url': None,
            'success': False
        }

        try:
            current_url = self.driver.current_url

            # 檢查是否是 YouTube 影片頁面
            if 'youtube.com/watch?v=' not in current_url:
                return None

            # 提取影片 ID
            if 'v=' in current_url:
                video_id = current_url.split('v=')[1].split('&')[0]
                info['video_id'] = video_id
                info['url'] = current_url

            # 提取影片標題
            try:
                title_element = self.driver.find_element(By.CSS_SELECTOR, "h1.ytd-watch-metadata yt-formatted-string")
                info['title'] = title_element.text.strip()
            except Exception:
                pass

            # 提取頻道名稱
            try:
                channel_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-channel-name a")
                info['channel'] = channel_element.text.strip()
            except Exception:
                pass

            # 提取影片描述（不展開，只取前面的部分）
            try:
                description_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-text-inline-expander#description-inline-expander yt-formatted-string")
                info['description'] = description_element.text.strip()[:300]  # 限制長度
            except Exception:
                pass

            info['success'] = bool(info['video_id'])

        except Exception as e:
            print(f"   ⚠️  提取影片資訊時發生錯誤: {e}")

        return info if info['success'] else None

    def capture_screen(self):
        """擷取螢幕截圖"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"yt_capture_{timestamp}_{self.capture_count:03d}.png"
        filepath = self.screenshot_dir / filename

        print(f"📸 擷取螢幕: {filename}")

        try:
            with mss.mss() as sct:
                # 擷取主螢幕
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)

                # 保存截圖
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=str(filepath))

                # 壓縮圖片
                img = Image.open(filepath)
                img.thumbnail((1280, 720), Image.Resampling.LANCZOS)
                img.save(filepath, optimize=True, quality=85)

            self.capture_count += 1
            return filepath

        except Exception as e:
            print(f"❌ 擷取失敗: {e}")
            return None

    def execute_action(self, action: str):
        """執行干預動作"""
        try:
            import pyautogui

            if action == 'close':
                print("🚫 執行干預：關閉 YouTube 分頁...")
                pyautogui.hotkey('ctrl', 'w')
                print("   ✓ 已發送關閉指令")
                return True

            elif action == 'redirect':
                print("↪️  執行干預：重導向到安全內容...")
                import pyperclip
                safe_url = "https://www.youtube.com/c/Cocomelon"
                pyperclip.copy(safe_url)
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(0.3)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.3)
                pyautogui.press('enter')
                print("   ✓ 已重導向到安全頻道")
                return True

            elif action == 'pause':
                print("⏸️  執行干預：暫停影片...")
                pyautogui.press('space')
                print("   ✓ 已暫停影片")
                return True

            elif action == 'warn':
                print("⚠️  執行干預：顯示警告...")
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showwarning(
                    "KidGuard 內容警告",
                    "偵測到不適當的內容！\n\n此影片可能不適合兒童觀看。"
                )
                root.destroy()
                print("   ✓ 已顯示警告")
                return True

        except Exception as e:
            print(f"   ✗ 執行失敗: {e}")
            return False

    def start(self):
        """啟動監控"""
        print("=" * 70)
        print("🛡️  KidGuard Live Monitor - HTML Extraction Mode")
        print("=" * 70)
        print()

        # 連接到 Chrome
        if not self.connect_to_chrome():
            return

        print()
        print("監控設定:")
        print(f"  • 檢測模式: 影片跳轉時觸發（基於 video ID）")
        print(f"  • 檢查頻率: 每 {self.check_interval} 秒")
        print(f"  • 截圖保存: {self.screenshot_dir.absolute()}")
        print(f"  • 資訊提取: 從 HTML DOM 直接提取（不使用 OCR）")
        print()
        print("🟢 監控已啟動，等待 YouTube 影片跳轉...")
        print("   (按 Ctrl+C 停止監控)")
        print()

        self.monitoring = True

        try:
            while self.monitoring:
                # 提取當前影片資訊
                video_info = self.extract_video_info()

                if video_info:
                    # 檢查影片是否切換
                    if video_info['video_id'] != self.last_video_id:
                        if self.last_video_id is not None:
                            print()
                            print("=" * 70)
                            print("🎬 偵測到影片跳轉！")
                        else:
                            print()
                            print("=" * 70)
                            print("🎬 偵測到 YouTube 影片")

                        print(f"   影片 ID: {video_info['video_id']}")
                        if video_info['title']:
                            print(f"   標題: {video_info['title'][:60]}...")
                        if video_info['channel']:
                            print(f"   頻道: {video_info['channel']}")
                        print("=" * 70)

                        # 更新追蹤的影片 ID
                        self.last_video_id = video_info['video_id']

                        # 擷取螢幕
                        screenshot_path = self.capture_screen()

                        if screenshot_path:
                            print()
                            print("📺 影片資訊（從 HTML 提取）:")
                            print(f"   標題: {video_info['title']}")
                            print(f"   頻道: {video_info['channel']}")
                            if video_info['description']:
                                print(f"   描述: {video_info['description'][:100]}...")
                            print(f"   URL: {video_info['url']}")
                            print()
                            print("📋 截圖已保存，請將圖片給 Claude 分析：")
                            print(f"   路徑: {screenshot_path.absolute()}")
                            print()
                            print("🤖 Claude 分析後，輸入指令執行動作：")
                            print("   - 'close' = 關閉分頁")
                            print("   - 'redirect' = 重導向安全頻道")
                            print("   - 'pause' = 暫停影片")
                            print("   - 'warn' = 顯示警告")
                            print("   - 'ok' = 內容安全，繼續監控")
                            print("   - 'stop' = 停止監控")
                            print()

                            # 等待用戶/Claude 的指令
                            try:
                                command = input("👉 請輸入指令: ").strip().lower()

                                if command == 'stop':
                                    print("🛑 停止監控")
                                    break
                                elif command == 'ok':
                                    print("✅ 內容安全，繼續監控...")
                                elif command in ['close', 'redirect', 'pause', 'warn']:
                                    self.execute_action(command)
                                    # 執行動作後，重置追蹤
                                    if command in ['close', 'redirect']:
                                        self.last_video_id = None
                                else:
                                    print(f"⚠️  未知指令: {command}")

                            except EOFError:
                                print("⚠️  非互動模式，自動繼續...")

                            print()
                            print("⏳ 繼續監控影片跳轉...")
                            print("-" * 70)
                            print()

                # 等待下次檢查
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print()
            print("=" * 70)
            print("🛑 監控已停止")
            print(f"📊 總共擷取: {self.capture_count} 張截圖")
            print("=" * 70)

        finally:
            if self.driver:
                # 不關閉瀏覽器，只斷開連接
                self.driver.quit()

        self.monitoring = False


def main():
    """主程式"""
    print()
    print("=" * 70)
    print("📌 使用說明")
    print("=" * 70)
    print()
    print("1. 先關閉所有 Chrome 視窗")
    print()
    print("2. 用以下指令啟動 Chrome（啟用遠端除錯）：")
    print()
    print('   "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')
    print()
    print("   或在命令提示字元中：")
    print('   start chrome --remote-debugging-port=9222')
    print()
    print("3. 在 Chrome 中開啟 YouTube")
    print()
    print("4. 回到這個程式，它會自動連接到 Chrome")
    print()
    print("=" * 70)
    print()

    input("按 Enter 開始連接...")

    # 啟動監控
    monitor = LiveMonitorHTML()
    monitor.start()


if __name__ == "__main__":
    main()
