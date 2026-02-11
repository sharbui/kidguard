#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KidGuard - Live Monitor (Auto Detection Mode)

自動檢測影片跳轉並擷取截圖，從視窗標題提取影片資訊
"""

import sys
import os

# 設置 Windows 控制台使用 UTF-8 編碼
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    # 重新配置標準輸出為 UTF-8
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

import time
from pathlib import Path
from datetime import datetime
import mss
import mss.tools
from PIL import Image


class AutoMonitor:
    """自動監控系統"""

    def __init__(self):
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.check_interval = 2  # 每 2 秒檢查一次
        self.capture_count = 0
        self.last_video_title = None  # 追蹤上一個影片標題
        self.monitoring = False

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
        filename = f"auto_capture_{timestamp}_{self.capture_count:03d}.png"
        filepath = self.screenshot_dir / filename

        print(f"[截圖] 擷取螢幕: {filename}")

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
        """啟動監控"""
        print("=" * 70)
        print("[KidGuard] Live Monitor - Auto Detection Mode")
        print("=" * 70)
        print()
        print("監控設定:")
        print(f"  - 檢測模式: 自動檢測影片跳轉")
        print(f"  - 檢查頻率: 每 {self.check_interval} 秒")
        print(f"  - 資訊來源: 視窗標題（不需要 OCR 或 Selenium）")
        print(f"  - 截圖保存: {self.screenshot_dir.absolute()}")
        print()
        print("[啟動] 監控已啟動，等待 YouTube 影片跳轉...")
        print("   (按 Ctrl+C 停止監控)")
        print()

        self.monitoring = True
        youtube_detected = False

        try:
            while self.monitoring:
                # 獲取當前 YouTube 資訊
                video_info = self.get_youtube_info()

                if video_info:
                    if not youtube_detected:
                        print("=" * 70)
                        print("[偵測] 偵測到 YouTube！")
                        print("=" * 70)
                        youtube_detected = True

                    current_title = video_info['full_title']

                    # 檢查是否是新影片
                    if current_title != self.last_video_title:
                        if self.last_video_title is not None:
                            print()
                            print("=" * 70)
                            print("[跳轉] 偵測到影片跳轉！")
                            print(f"   上一部: {self.last_video_title[:50]}...")
                            print(f"   新影片: {current_title[:50]}...")
                            print("=" * 70)
                        else:
                            print()
                            print("=" * 70)
                            print("[新影片] 偵測到新影片")
                            print("=" * 70)

                        # 更新追蹤的標題
                        self.last_video_title = current_title

                        # 顯示影片資訊
                        print()
                        print("[影片資訊] 從視窗標題提取:")
                        print(f"   標題: {video_info['title']}")
                        if video_info['channel']:
                            print(f"   頻道: {video_info['channel']}")
                        print()

                        # 擷取螢幕
                        screenshot_path = self.capture_screen()

                        if screenshot_path:
                            print()
                            print("[截圖] 截圖已保存：")
                            print(f"   路徑: {screenshot_path.absolute()}")
                            print()
                            print("[等待] 請將截圖給 Claude 分析，他會建議執行什麼動作")
                            print()
                            print("[監控] 繼續監控影片跳轉...")
                            print("-" * 70)
                            print()

                else:
                    if youtube_detected:
                        print("[關閉] YouTube 已關閉，繼續待機...")
                        youtube_detected = False
                        self.last_video_title = None

                # 等待下次檢查
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print()
            print("=" * 70)
            print("[停止] 監控已停止")
            print(f"[統計] 總共擷取: {self.capture_count} 張截圖")
            print("=" * 70)

        self.monitoring = False


def main():
    """主程式"""
    monitor = AutoMonitor()
    monitor.start()


if __name__ == "__main__":
    main()
