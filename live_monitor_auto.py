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
import yaml


class AutoMonitor:
    """自動監控系統"""

    def __init__(self, config_path="config/config.yaml"):
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.check_interval = 2  # 每 2 秒檢查一次
        self.capture_count = 0
        self.last_video_title = None  # 追蹤上一個影片標題
        self.monitoring = False

        # 載入配置
        self.config = self.load_config(config_path)
        self.use_ai_analysis = self.config.get('analysis', {}).get('use_ai_analysis', True)

        # 關鍵字過濾設定
        keyword_filter = self.config.get('analysis', {}).get('keyword_filter', {})
        self.blocked_keywords = keyword_filter.get('blocked_keywords', [])
        self.blocked_channels = keyword_filter.get('blocked_channels', [])

    def load_config(self, config_path):
        """載入配置檔"""
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                print(f"[警告] 配置檔不存在: {config_path}")
                print("[提示] 使用預設設定")
                return {}
        except Exception as e:
            print(f"[錯誤] 載入配置檔失敗: {e}")
            return {}

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
            print(f"   [警告] 無法獲取視窗標題: {e}")

        return None

    def check_keywords(self, video_info):
        """關鍵字過濾檢查"""
        if not video_info:
            return {'safe': True, 'reason': None}

        title = video_info.get('title', '').lower()
        channel = video_info.get('channel', '').lower() if video_info.get('channel') else ''

        # 檢查標題中的關鍵字
        for keyword in self.blocked_keywords:
            if keyword.lower() in title:
                return {
                    'safe': False,
                    'reason': f'標題包含禁止關鍵字: {keyword}',
                    'action': 'close'
                }

        # 檢查頻道名稱
        for keyword in self.blocked_channels:
            if keyword.lower() in channel:
                return {
                    'safe': False,
                    'reason': f'頻道名稱包含禁止關鍵字: {keyword}',
                    'action': 'close'
                }

        return {'safe': True, 'reason': '關鍵字檢查通過'}

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
            print(f"[錯誤] 擷取失敗: {e}")
            return None

    def execute_action(self, action: str):
        """執行干預動作"""
        try:
            import pyautogui

            if action == 'close':
                print("[執行] 關閉 YouTube 分頁...")
                pyautogui.hotkey('ctrl', 'w')
                print("[完成] 已發送關閉指令")
                return True

            elif action == 'redirect':
                print("[執行] 重導向到安全內容...")
                import pyperclip
                safe_url = "https://www.youtube.com/c/Cocomelon"
                pyperclip.copy(safe_url)
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(0.3)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.3)
                pyautogui.press('enter')
                print("[完成] 已重導向到安全頻道")
                return True

            elif action == 'pause':
                print("[執行] 暫停影片...")
                pyautogui.press('space')
                print("[完成] 已暫停影片")
                return True

            elif action == 'warn':
                print("[執行] 顯示警告...")
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showwarning(
                    "KidGuard 內容警告",
                    "偵測到不適當的內容！\n\n此影片可能不適合兒童觀看。"
                )
                root.destroy()
                print("[完成] 已顯示警告")
                return True

        except Exception as e:
            print(f"[錯誤] 執行失敗: {e}")
            return False

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
        print(f"  - 分析方式: {'AI API 分析' if self.use_ai_analysis else '關鍵字過濾 (省錢模式)'}")
        print(f"  - 截圖保存: {self.screenshot_dir.absolute()}")
        if not self.use_ai_analysis:
            print(f"  - 關鍵字規則: {len(self.blocked_keywords)} 個標題關鍵字, {len(self.blocked_channels)} 個頻道關鍵字")
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

                        # 根據配置決定使用哪種分析方式
                        if not self.use_ai_analysis:
                            # 關鍵字過濾模式
                            print("[過濾] 執行關鍵字過濾檢查...")
                            filter_result = self.check_keywords(video_info)

                            if not filter_result['safe']:
                                print(f"[警告] {filter_result['reason']}")
                                print(f"[建議] 執行動作: {filter_result['action']}")
                                print()

                                # 擷取截圖作為記錄
                                screenshot_path = self.capture_screen()
                                if screenshot_path:
                                    print(f"[記錄] 截圖已保存: {screenshot_path.name}")

                                # 詢問是否執行動作
                                try:
                                    command = input("[確認] 是否執行建議動作？(y/n 或指定動作): ").strip().lower()

                                    if command == 'y':
                                        command = filter_result['action']

                                    if command in ['close', 'redirect', 'pause', 'warn']:
                                        self.execute_action(command)
                                        if command in ['close', 'redirect']:
                                            self.last_video_title = None
                                    elif command == 'n':
                                        print("[繼續] 忽略警告，繼續監控")
                                except EOFError:
                                    print("[自動] 非互動模式，繼續監控...")
                            else:
                                print(f"[安全] {filter_result['reason']}")

                            print()
                            print("[監控] 繼續監控影片跳轉...")
                            print("-" * 70)
                            print()

                        else:
                            # AI 分析模式
                            screenshot_path = self.capture_screen()

                            if screenshot_path:
                                print()
                                print("[截圖] 截圖已保存：")
                                print(f"   路徑: {screenshot_path.absolute()}")
                                print()
                                print("[AI 模式] 請將截圖給 Claude 分析，他會建議執行什麼動作")
                                print()

                                # 等待用戶輸入指令
                                try:
                                    command = input("[指令] 請輸入 Claude 建議的動作 (ok/warn/pause/redirect/close/stop): ").strip().lower()

                                    if command == 'stop':
                                        print("[停止] 停止監控")
                                        break
                                    elif command == 'ok':
                                        print("[安全] 內容安全，繼續監控...")
                                    elif command in ['close', 'redirect', 'pause', 'warn']:
                                        self.execute_action(command)
                                        if command in ['close', 'redirect']:
                                            self.last_video_title = None
                                    else:
                                        print(f "[未知] 未知指令: {command}")

                                except EOFError:
                                    print("[自動] 非互動模式，自動繼續...")

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
