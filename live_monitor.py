#!/usr/bin/env python3
"""
KidGuard - Live Monitor (Claude Visual Analysis Mode)

實時監控 YouTube，由 Claude 直接進行視覺分析和內容干預。
"""

import time
import subprocess
import psutil
from pathlib import Path
from datetime import datetime
import mss
import mss.tools
from PIL import Image

class LiveMonitor:
    """即時監控系統"""

    def __init__(self):
        self.monitoring = False
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.check_interval = 10  # 每 10 秒檢查一次
        self.capture_count = 0

    def detect_youtube(self):
        """檢測 YouTube 是否在運行"""
        # 檢查瀏覽器進程
        browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'brave.exe', 'opera.exe']

        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                # 檢查是否是瀏覽器
                if proc.info['name'] and proc.info['name'].lower() in browsers:
                    # 檢查命令行參數是否包含 youtube
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and any('youtube.com' in str(arg).lower() for arg in cmdline):
                        return True, proc.info['name']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return False, None

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

                # 壓縮圖片（減少文件大小）
                img = Image.open(filepath)
                # 縮小到 1280x720 以便快速分析
                img.thumbnail((1280, 720), Image.Resampling.LANCZOS)
                img.save(filepath, optimize=True, quality=85)

            self.capture_count += 1
            return filepath

        except Exception as e:
            print(f"❌ 擷取失敗: {e}")
            return None

    def close_browser_tab(self):
        """嘗試關閉當前瀏覽器分頁"""
        print("🚫 執行干預：關閉 YouTube 分頁...")

        try:
            # Windows: 使用 Alt+F4 或 Ctrl+W
            import pyautogui
            pyautogui.hotkey('ctrl', 'w')  # 關閉分頁
            print("   ✓ 已發送關閉指令")
            return True
        except Exception as e:
            print(f"   ✗ 關閉失敗: {e}")
            return False

    def redirect_to_safe(self):
        """重導向到安全頻道"""
        print("↪️  執行干預：重導向到安全內容...")

        try:
            import pyautogui
            import pyperclip

            # 安全頻道 URL（例如：Cocomelon）
            safe_url = "https://www.youtube.com/c/Cocomelon"

            # 複製到剪貼板
            pyperclip.copy(safe_url)

            # Ctrl+L 選擇網址列，Ctrl+V 貼上，Enter 前往
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')

            print("   ✓ 已重導向到安全頻道")
            return True
        except Exception as e:
            print(f"   ✗ 重導向失敗: {e}")
            return False

    def pause_video(self):
        """暫停影片播放"""
        print("⏸️  執行干預：暫停影片...")

        try:
            import pyautogui
            # YouTube 的暫停快捷鍵是空白鍵
            pyautogui.press('space')
            print("   ✓ 已暫停影片")
            return True
        except Exception as e:
            print(f"   ✗ 暫停失敗: {e}")
            return False

    def show_warning(self):
        """顯示警告訊息"""
        print("⚠️  執行干預：顯示警告...")

        try:
            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning(
                "KidGuard 內容警告",
                "偵測到不適當的內容！\n\n此影片可能不適合兒童觀看。\n\n請選擇其他適合年齡的內容。"
            )
            root.destroy()

            print("   ✓ 已顯示警告")
            return True
        except Exception as e:
            print(f"   ✗ 顯示警告失敗: {e}")
            return False

    def execute_action(self, action: str):
        """執行干預動作"""
        actions = {
            'close': self.close_browser_tab,
            'redirect': self.redirect_to_safe,
            'pause': self.pause_video,
            'warn': self.show_warning
        }

        if action in actions:
            return actions[action]()
        else:
            print(f"⚠️  未知動作: {action}")
            return False

    def start(self):
        """啟動監控"""
        print("=" * 70)
        print("🛡️  KidGuard Live Monitor - Claude Visual Analysis Mode")
        print("=" * 70)
        print()
        print("監控設定:")
        print(f"  • 檢查間隔: {self.check_interval} 秒")
        print(f"  • 截圖保存: {self.screenshot_dir.absolute()}")
        print()
        print("可用的干預動作:")
        print("  • close    - 關閉當前分頁")
        print("  • redirect - 重導向到安全頻道")
        print("  • pause    - 暫停影片")
        print("  • warn     - 顯示警告訊息")
        print()
        print("🟢 監控已啟動，等待 YouTube...")
        print("   (按 Ctrl+C 停止監控)")
        print()

        self.monitoring = True
        youtube_detected = False

        try:
            while self.monitoring:
                is_youtube, browser = self.detect_youtube()

                if is_youtube:
                    if not youtube_detected:
                        print("=" * 70)
                        print(f"⚠️  偵測到 YouTube！ (瀏覽器: {browser})")
                        print("=" * 70)
                        youtube_detected = True

                    # 擷取螢幕
                    screenshot_path = self.capture_screen()

                    if screenshot_path:
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
                            else:
                                print(f"⚠️  未知指令: {command}")

                        except EOFError:
                            # 如果在非互動環境中運行
                            print("⚠️  非互動模式，自動繼續...")

                        print()
                        print(f"⏳ 等待 {self.check_interval} 秒後繼續監控...")
                        print("-" * 70)
                        print()

                else:
                    if youtube_detected:
                        print("✓ YouTube 已關閉，繼續待機...")
                        youtube_detected = False

                # 等待下次檢查
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print()
            print("=" * 70)
            print("🛑 監控已停止")
            print(f"📊 總共擷取: {self.capture_count} 張截圖")
            print("=" * 70)

        self.monitoring = False


def main():
    """主程式"""

    # 檢查依賴
    try:
        import mss
        import psutil
        import pyautogui
        import pyperclip
    except ImportError as e:
        print("❌ 缺少必要的套件，請安裝：")
        print("   pip install mss psutil pyautogui pyperclip pillow")
        return

    # 啟動監控
    monitor = LiveMonitor()
    monitor.start()


if __name__ == "__main__":
    main()
