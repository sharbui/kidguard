@echo off
echo.
echo ========================================
echo   🛡️ KidGuard Live Monitor
echo   Claude Visual Analysis Mode
echo ========================================
echo.
echo 此模式讓 Claude 直接分析截圖並進行內容干預
echo.
echo 監控流程:
echo   1. 偵測 YouTube 開啟
echo   2. 自動擷取螢幕截圖
echo   3. 你將截圖給 Claude 分析
echo   4. Claude 告訴你該執行什麼動作
echo   5. 系統自動執行干預
echo.
echo 按任意鍵啟動監控...
pause > nul
echo.

python live_monitor.py

echo.
pause
