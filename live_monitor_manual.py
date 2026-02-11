#!/usr/bin/env python3
"""
KidGuard - Live Monitor (Manual Mode)

手動模式：按任意鍵擷取截圖，不依賴 YouTube 檢測
"""

import time
from pathlib import Path
from datetime import datetime
import mss
import mss.tools
from PIL import Image

class ManualMonitor:
    """手動監控系統"""

    def __init__(self):
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.capture_count = 0
        self.last_video_title = None  # 追蹤上一個影片標題

    def get_youtube_info(self):
        """從視窗標題獲取 YouTube 影片資訊"""
        try:
            import pygetwindow as gw
            windows = gw.getAllTitles()
            for title in windows:
                if 'youtube' in title.lower() and title.strip():
                    # 清理標題
                    clean_title = title
                    for browser in [' - Google Chrome', ' - Mozilla Firefox', ' - Microsoft Edge', ' - Brave', ' - Opera']:
                        clean_title = clean_title.replace(browser, '')
                    clean_title = clean_title.replace(' - YouTube', '').strip()

                    if clean_title and clean_title.lower() != 'youtube':
                        # 嘗試分離影片標題和頻道名稱
                        # YouTube 視窗標題格式: "影片標題 - 頻道名稱"
                        parts = clean_title.split(' - ')
                        if len(parts) >= 2:
                            return {
                                'title': parts[0].strip(),
                                'channel': parts[1].strip(),
                                'full_title': clean_title
                            }
                        else:
                            return {
                                'title': clean_title,
                                'channel': None,
                                'full_title': clean_title
                            }
        except Exception as e:
            print(f"   ⚠️  無法獲取視窗標題: {e}")

        return None

    def capture_screen(self):
        """擷取螢幕截圖"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"manual_capture_{timestamp}_{self.capture_count:03d}.png"
        filepath = self.screenshot_dir / filename

        print(f"\n📸 擷取螢幕: {filename}")

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

    def start(self):
        """啟動手動監控"""
        print("=" * 70)
        print("🛡️  KidGuard Live Monitor - Manual Mode")
        print("=" * 70)
        print()
        print("📸 手動擷取模式")
        print("   不需要自動檢測 YouTube，隨時可以擷取截圖")
        print()
        print("💡 使用方法:")
        print("   1. 開啟 YouTube 播放影片")
        print("   2. 按 Enter 鍵擷取截圖")
        print("   3. 將截圖給 Claude 分析")
        print("   4. 根據 Claude 的建議輸入指令")
        print()
        print("🎮 可用指令:")
        print("   • Enter     - 擷取截圖")
        print("   • close     - 關閉當前分頁")
        print("   • redirect  - 重導向到安全頻道")
        print("   • pause     - 暫停影片")
        print("   • warn      - 顯示警告")
        print("   • ok        - 內容安全，繼續")
        print("   • stop/quit - 停止監控")
        print()
        print("🟢 監控已啟動！")
        print("-" * 70)
        print()

        try:
            while True:
                command = input("👉 按 Enter 擷取截圖（或輸入指令）: ").strip().lower()

                if command in ['stop', 'quit', 'exit']:
                    print("\n🛑 監控已停止")
                    break

                elif command == 'close':
                    print("🚫 執行：關閉分頁...")
                    try:
                        import pyautogui
                        pyautogui.hotkey('ctrl', 'w')
                        print("   ✓ 已發送關閉指令")
                    except Exception as e:
                        print(f"   ✗ 失敗: {e}")

                elif command == 'redirect':
                    print("↪️  執行：重導向到安全頻道...")
                    try:
                        import pyautogui
                        import pyperclip
                        safe_url = "https://www.youtube.com/c/Cocomelon"
                        pyperclip.copy(safe_url)
                        pyautogui.hotkey('ctrl', 'l')
                        time.sleep(0.3)
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(0.3)
                        pyautogui.press('enter')
                        print("   ✓ 已重導向")
                    except Exception as e:
                        print(f"   ✗ 失敗: {e}")

                elif command == 'pause':
                    print("⏸️  執行：暫停影片...")
                    try:
                        import pyautogui
                        pyautogui.press('space')
                        print("   ✓ 已暫停")
                    except Exception as e:
                        print(f"   ✗ 失敗: {e}")

                elif command == 'warn':
                    print("⚠️  執行：顯示警告...")
                    try:
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
                    except Exception as e:
                        print(f"   ✗ 失敗: {e}")

                elif command == 'ok':
                    print("✅ 內容安全，繼續監控...")

                else:
                    # 預設：擷取截圖
                    # 先獲取影片資訊
                    video_info = self.get_youtube_info()

                    # 檢查是否是新影片
                    if video_info:
                        current_title = video_info['full_title']
                        if current_title != self.last_video_title:
                            if self.last_video_title:
                                print()
                                print("=" * 70)
                                print("🎬 偵測到影片跳轉！")
                                print(f"   上一部: {self.last_video_title[:50]}...")
                                print(f"   新影片: {current_title[:50]}...")
                                print("=" * 70)
                            self.last_video_title = current_title

                    screenshot_path = self.capture_screen()

                    if screenshot_path:
                        print()

                        # 顯示從視窗標題提取的資訊
                        if video_info:
                            print("📺 影片資訊（從視窗標題提取）:")
                            print(f"   標題: {video_info['title']}")
                            if video_info['channel']:
                                print(f"   頻道: {video_info['channel']}")
                            print()

                        print("📋 截圖已保存，請將圖片給 Claude 分析：")
                        print(f"   路徑: {screenshot_path.absolute()}")
                        print()
                        print("🤖 等待 Claude 分析...")
                        print("   將截圖給 Claude，他會告訴你該執行什麼動作")
                        print()

        except KeyboardInterrupt:
            print("\n\n🛑 監控已停止")

        print(f"📊 總共擷取: {self.capture_count} 張截圖")
        print("=" * 70)


def main():
    """主程式"""
    monitor = ManualMonitor()
    monitor.start()


if __name__ == "__main__":
    main()
