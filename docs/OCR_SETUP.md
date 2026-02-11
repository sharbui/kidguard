# 📝 OCR 功能設置指南

## 概述

Live Monitor 現在可以從截圖中提取影片標題和頻道名稱，幫助 Claude 更準確地分析內容。

---

## 🔧 安裝 OCR 支援

### Windows 安裝步驟

#### 1️⃣ 安裝 Tesseract OCR

**方法 A：使用安裝包（推薦）**

1. 下載 Tesseract 安裝包：
   https://github.com/UB-Mannheim/tesseract/wiki

2. 下載最新版本（例如：tesseract-ocr-w64-setup-5.3.3.exe）

3. 執行安裝，記住安裝路徑（預設：`C:\Program Files\Tesseract-OCR`）

4. **重要：** 安裝時勾選 "Additional language data"
   - ✅ 勾選 Chinese - Traditional (chi_tra)
   - ✅ 勾選 English (eng)

#### 2️⃣ 設置環境變數

將 Tesseract 加入 PATH：

1. 右鍵「此電腦」→「內容」
2. 「進階系統設定」→「環境變數」
3. 在「系統變數」中找到「Path」，點擊「編輯」
4. 點擊「新增」，輸入：`C:\Program Files\Tesseract-OCR`
5. 點擊「確定」保存

#### 3️⃣ 安裝 Python 套件

```cmd
cd C:\projects\kidguard
.venv\Scripts\activate
uv pip install pytesseract
```

或使用 pip：
```cmd
pip install pytesseract
```

#### 4️⃣ 驗證安裝

```cmd
tesseract --version
```

應該顯示：
```
tesseract 5.3.3
  ...
```

---

## 🧪 測試 OCR 功能

創建測試腳本：

```python
# test_ocr.py
import pytesseract
from PIL import Image

# 測試中文
print("測試 OCR...")
img = Image.open("testuserpic/test.jpg")
text = pytesseract.image_to_string(img, lang='chi_tra+eng')
print(f"識別文字: {text}")
```

執行：
```cmd
python test_ocr.py
```

---

## 🎯 Live Monitor 中的使用

### 啟動監控

```cmd
.venv\Scripts\python live_monitor.py
```

### OCR 可用時的輸出

當 OCR 正常工作時，你會看到：

```
📸 擷取螢幕: yt_capture_20260210_171234_001.png

📺 影片資訊:
   標題: 小豬佩奇 第一季 第1集 泥坑
   頻道: Peppa Pig 中文官方頻道

📋 截圖已保存，請將圖片給 Claude 分析：
   路徑: C:\projects\kidguard\screenshots\yt_capture_...
```

### OCR 不可用時

如果沒有安裝 pytesseract，會看到：

```
📸 擷取螢幕: yt_capture_20260210_171234_001.png
   ⚠️  OCR 不可用（需要安裝 pytesseract）

📋 截圖已保存，請將圖片給 Claude 分析：
   ...
```

**仍然可以正常使用，只是不會顯示影片標題和頻道名稱。**

---

## 💡 Claude 分析時的優勢

### 有 OCR 時

你給我截圖時，我會看到：
```
截圖 + 標題：「恐怖遊戲實況」+ 頻道：「XX遊戲頻道」
```

我可以：
- ✅ 直接從標題判斷內容類型
- ✅ 根據頻道名稱評估可信度
- ✅ 結合畫面和文字做綜合判斷

### 沒有 OCR 時

我只能看到：
```
截圖（無文字資訊）
```

我需要：
- 只能根據畫面視覺內容判斷
- 無法知道影片標題和頻道

---

## 🔍 OCR 識別準確度

### 影響因素

✅ **容易識別：**
- 清晰的字體
- 高對比度（黑字白底）
- 標準字型大小

⚠️ **較難識別：**
- 藝術字體
- 低對比度
- 重疊文字
- 過小的字體

### 提高準確度

1. **全螢幕播放** - YouTube 標題更大更清晰
2. **暫停影片** - 避免動態文字
3. **關閉字幕** - 減少干擾
4. **深色模式** - 白字黑底較易識別

---

## 🐛 故障排除

### 問題 1：找不到 tesseract 命令

**錯誤：**
```
TesseractNotFoundError: tesseract is not installed
```

**解決：**
1. 確認 Tesseract 已安裝
2. 檢查環境變數 PATH
3. 重啟命令提示字元

### 問題 2：無法識別中文

**錯誤：**
```
Error: Tesseract failed to load language 'chi_tra'
```

**解決：**
1. 重新安裝 Tesseract
2. 安裝時勾選 Chinese - Traditional
3. 或手動下載語言包：
   https://github.com/tesseract-ocr/tessdata

放到：`C:\Program Files\Tesseract-OCR\tessdata\`

### 問題 3：識別準確度低

**解決：**
- 提高截圖解析度
- 調整 YouTube 播放器大小
- 使用全螢幕模式
- 確保頁面完全載入

---

## 📊 效果對比

### 範例 1：有 OCR

```
📺 影片資訊:
   標題: 恐怖遊戲實況 PART 10 最終章
   頻道: XX遊戲頻道

🤖 Claude 分析:
⚠️ 不適合！
- 標題明確標示「恐怖」
- 遊戲實況可能有驚嚇畫面
建議動作: close
```

### 範例 2：無 OCR

```
📋 截圖已保存...

🤖 Claude 分析:
⚠️ 不適合！
- 畫面顯示陰暗場景
- 可能是恐怖內容
建議動作: close
```

**有 OCR 可以更快更準確地判斷！**

---

## 🚀 建議配置

### 最佳配置（有 OCR）

```python
# live_monitor.py 設定
self.check_interval = 10  # 每 10 秒
# OCR 自動啟用
```

### 基本配置（無 OCR）

```python
# live_monitor.py 設定
self.check_interval = 15  # 可以稍微放寬間隔
# 僅靠視覺分析
```

---

## 📝 總結

### 是否需要 OCR？

**需要（推薦）：**
- ✅ 想要更準確的內容判斷
- ✅ 想要檢查關鍵字黑名單
- ✅ 願意花 10 分鐘安裝

**不需要（可選）：**
- ✅ 只依賴視覺分析也足夠
- ✅ 不想安裝額外軟體
- ✅ 系統資源有限

---

**建議：先不安裝 OCR 測試基本功能，如果需要更精確的判斷再安裝！**
