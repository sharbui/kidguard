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
import re
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

class LiveMonitor:
    """即時監控系統"""

    def __init__(self):
        self.monitoring = False
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.check_interval = 2  # 每 2 秒檢查影片是否跳轉
        self.capture_count = 0
        self.last_video_title = None  # 追蹤上一個影片標題

    def get_youtube_window_title(self):
        """獲取 YouTube 視窗標題"""
        try:
            import pygetwindow as gw
            windows = gw.getAllTitles()
            for title in windows:
                if 'youtube' in title.lower() and title.strip():
                    # 清理標題，移除瀏覽器名稱後綴
                    # 例如："Video Title - YouTube - Google Chrome" -> "Video Title"
                    clean_title = title
                    for browser in [' - Google Chrome', ' - Mozilla Firefox', ' - Microsoft Edge', ' - Brave', ' - Opera']:
                        clean_title = clean_title.replace(browser, '')
                    clean_title = clean_title.replace(' - YouTube', '').strip()

                    # 如果標題不是空的且不只是 "YouTube"，就返回
                    if clean_title and clean_title.lower() != 'youtube':
                        return clean_title
        except Exception as e:
            pass
        return None

    def detect_youtube(self):
        """檢測 YouTube 是否在運行"""
        # 檢查瀏覽器進程
        browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'brave.exe', 'opera.exe']

        # 方法1: 檢查視窗標題
        try:
            import pygetwindow as gw
            windows = gw.getAllTitles()
            for title in windows:
                if 'youtube' in title.lower():
                    # 找到對應的瀏覽器進程
                    for proc in psutil.process_iter(['name']):
                        try:
                            if proc.info['name'] and proc.info['name'].lower() in browsers:
                                return True, proc.info['name']
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    return True, 'browser'
        except Exception as e:
            print(f"   檢測視窗失敗，使用備用方法: {e}")

        # 方法2: 檢查命令行參數（備用）
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

        # 方法3: 如果有瀏覽器在運行，假設可能在看 YouTube（最寬鬆）
        # 這個方法會在有瀏覽器時就開始截圖，讓用戶判斷
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() in browsers:
                    # 不自動返回 True，避免誤報
                    pass
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return False, None

    def extract_video_info(self, screenshot_path):
        """從截圖中提取影片標題和頻道名稱"""
        info = {
            'title': None,
            'channel': None,
            'extracted': False
        }

        if not OCR_AVAILABLE:
            print("   ⚠️  OCR 不可用（需要安裝 pytesseract）")
            return info

        try:
            # 讀取截圖
            img = Image.open(screenshot_path)
            width, height = img.size

            # YouTube 標題通常在上方 20% 的區域
            title_region = img.crop((0, 0, width, int(height * 0.2)))

            # 頻道名稱通常在標題下方
            channel_region = img.crop((0, int(height * 0.15), width, int(height * 0.3)))

            # 使用 OCR 提取文字
            title_text = pytesseract.image_to_string(title_region, lang='chi_tra+eng')
            channel_text = pytesseract.image_to_string(channel_region, lang='chi_tra+eng')

            # 清理文字
            title_text = ' '.join(title_text.split()).strip()
            channel_text = ' '.join(channel_text.split()).strip()

            if title_text:
                # 移除常見的 YouTube UI 元素
                title_text = re.sub(r'(YouTube|訂閱|Subscribe|分享|Share)', '', title_text)
                info['title'] = title_text[:100]  # 限制長度

            if channel_text:
                channel_text = re.sub(r'(訂閱|Subscribe|已訂閱|Subscribed)', '', channel_text)
                info['channel'] = channel_text[:50]

            info['extracted'] = bool(info['title'] or info['channel'])

        except Exception as e:
            print(f"   ⚠️  提取影片資訊失敗: {e}")

        return info

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

            # 提取影片資訊
            video_info = self.extract_video_info(filepath)

            return filepath, video_info

        except Exception as e:
            print(f"❌ 擷取失敗: {e}")
            return None, None

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
        print("🛡️  KidGuard Live Monitor - Video Transition Detection Mode")
        print("=" * 70)
        print()
        print("監控設定:")
        print(f"  • 檢測模式: 影片跳轉時觸發（非固定時間間隔）")
        print(f"  • 檢查頻率: 每 {self.check_interval} 秒檢查一次影片是否切換")
        print(f"  • 截圖保存: {self.screenshot_dir.absolute()}")
        print()
        print("可用的干預動作:")
        print("  • close    - 關閉當前分頁")
        print("  • redirect - 重導向到安全頻道")
        print("  • pause    - 暫停影片")
        print("  • warn     - 顯示警告訊息")
        print()
        print("💡 提示:")
        print("  • 只有在 YouTube 切換到新影片時才會觸發分析")
        print("  • 輸入 'stop' 停止監控")
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
                        # 重置上次的影片標題
                        self.last_video_title = None

                    # 獲取當前影片標題
                    current_title = self.get_youtube_window_title()

                    # 檢查影片是否切換
                    if current_title and current_title != self.last_video_title:
                        if self.last_video_title is not None:
                            print()
                            print("=" * 70)
                            print("🎬 偵測到影片跳轉！")
                            print(f"   上一部: {self.last_video_title[:60]}...")
                            print(f"   新影片: {current_title[:60]}...")
                            print("=" * 70)
                        else:
                            print()
                            print("=" * 70)
                            print("🎬 偵測到新影片")
                            print(f"   標題: {current_title[:60]}...")
                            print("=" * 70)

                        # 更新追蹤的標題
                        self.last_video_title = current_title

                        # 擷取螢幕
                        screenshot_path, video_info = self.capture_screen()

                        if screenshot_path:
                            print()

                            # 顯示提取的影片資訊
                            if video_info and video_info.get('extracted'):
                                print("📺 影片資訊:")
                                if video_info.get('title'):
                                    print(f"   標題: {video_info['title']}")
                                if video_info.get('channel'):
                                    print(f"   頻道: {video_info['channel']}")
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
                                    # 執行動作後，重置標題追蹤
                                    if command in ['close', 'redirect']:
                                        self.last_video_title = None
                                else:
                                    print(f"⚠️  未知指令: {command}")

                            except EOFError:
                                # 如果在非互動環境中運行
                                print("⚠️  非互動模式，自動繼續...")

                            print()
                            print("⏳ 繼續監控影片跳轉...")
                            print("-" * 70)
                            print()

                else:
                    if youtube_detected:
                        print("✓ YouTube 已關閉，繼續待機...")
                        youtube_detected = False
                        self.last_video_title = None

                # 等待下次檢查（檢查影片是否切換）
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
