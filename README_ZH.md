# 🛡️ KidGuard

> AI 驅動的 YouTube 內容守護者，專為幼兒設計

[English](README.md) | 繁體中文

## 黑客松提交作品

**活動：** Built with Opus 4.6: The Claude Code Hackathon
**團隊規模：** 1 人
**時間線：** 2026 年 2 月 10-16 日

---

## 🎯 問題所在

每個家長都遇過這種情況：

你 5 歲的孩子坐到電腦前。幾秒鐘內，他們就打開了 YouTube（不是 YouTube Kids），開始點擊自動播放推薦。等你注意到時，他們已經看到了不適當、恐怖或奇怪的內容。

**YouTube 的年齡驗證？** 笑話。孩子根本不看就點「我已年滿 18 歲」。

**限制模式？** 一個開關就能關閉。

**YouTube Kids？** 很好，但孩子分不清差別 — 他們只看到「影片 App」。

家長無法 24/7 監控。我們需要 AI 的幫助。

### 一位家長的真實故事

*「也許你會說：不要讓孩子接觸 3C 與 YouTube 不就好了！」*

但這是我作為三個孩子父親的真實情況：

**我的第一個孩子**在上小學前完全沒接觸過電視和平板。他只有書。上學前就看到四年級的程度了。

**然後老二、老三出生了。**突然間只有爸媽兩個人要照顧三個孩子。我們無法給每個孩子同等的一對一關注。我們連喘口氣都不行。

**這時我們需要幫助。**不是要取代父母的角色，而是**延伸我們的能力** — 當我們身體上無法分身時。

這就是 AI 真正能幫助家庭的地方：
- **不只是 AdGuard** 或簡單的黑名單
- **智能的、理解上下文的保護** — 真正理解孩子在看什麼
- **低成本、嵌入式的協助** — 不需要電腦科學學位
- **安全網** — 當父母在煮晚餐、幫忙做功課，或只是努力撐過一天時

很多人說不敢生小孩，或不知道怎麼帶小孩。如果 AI 能讓育兒變得更容易管理呢？如果科技能成為**守護者**，而不只是保姆呢？

這就是 KidGuard 背後的理念。

---

## 💡 解決方案

**KidGuard** 使用 Claude 的視覺能力創建即時內容守護者：

```
[開啟 YouTube]
       ↓
[攝影機檢查] → 誰在看？（年齡估計 / 家庭成員識別）
       ↓
   12 歲以下？
       ↓ 是
[擷取 5 秒片段]
       ↓
[Claude 視覺分析] → 適合兒童嗎？
       ↓
   不適當？
       ↓ 是
[自動跳過 / 重導向到安全頻道]
       ↓
[透過 Telegram 通知家長]
```

### 為什麼選擇 Claude？

- **視覺 API** 分析影片畫面中的暴力、恐怖、成人主題和「YouTube 兔子洞」內容
- **細緻理解** — 不只是關鍵字阻擋，而是上下文分析
- **多模態** — 可以同時分析視覺和音訊轉錄
- **夠快** 能進行即時干預

---

## 🔧 技術架構

| 元件 | 技術 | 備註 |
|------|------|------|
| YouTube 檢測 | 瀏覽器擴充功能 / 進程監控 | 檢測 youtube.com |
| 人臉識別 | OpenCV + face_recognition | 本地處理，隱私優先 |
| 年齡估計 | Claude Vision | 未知人臉的備用方案 |
| 螢幕擷取 | ffmpeg / Windows API | 5 秒片段 |
| 內容分析 | **Claude Vision API** | 核心智能 |
| 瀏覽器控制 | Puppeteer / Extension API | 跳過 / 重導向 |
| 家長通知 | Telegram Bot | 即時警報 |

### 隱私優先設計

- 所有人臉識別都在**本地**運行
- 影片片段分析後立即刪除
- 除了 Claude API 調用外，沒有資料離開設備
- 家長控制記錄什麼

---

## 🚀 功能特色

### MVP（黑客松範圍）

- [x] 檢測 YouTube 瀏覽器活動
- [x] 基於攝影機的觀看者識別
- [x] 未知觀看者的年齡估計
- [x] YouTube 內容的螢幕擷取
- [x] Claude Vision 內容分析
- [x] 自動跳過不當內容
- [x] 重導向到白名單頻道
- [x] Telegram 通知家長
- [x] **🆕 家長自定義規則**（語言、動作、音訊、主題、關鍵字）
- [x] **🆕 智能影片跳轉檢測** - 只在影片切換時分析（節省 API 成本）
- [x] **🆕 視窗標題提取** - 不需要 Selenium/OCR 就能取得影片資訊
- [x] **🆕 自動監控模式** - 免人工干預的保護

### 未來路線圖

- [ ] 家庭成員檔案管理
- [ ] 觀看歷史儀表板
- [ ] ~~自定義過濾規則~~ ✅ **完成** - 完全可配置的家長規則
- [ ] ~~影片跳轉檢測~~ ✅ **完成** - 智能節省成本分析
- [ ] 音訊分析（尖叫、髒話檢測）
- [ ] 跨平台支援（平板、手機）
- [ ] 整合路由器層級控制
- [ ] 每個孩子的自定義規則

---

## 🎯 家長自定義規則（新功能！）

KidGuard 現在支援**高度可自定義的過濾規則**，讓家長精確定義什麼內容適合他們的孩子：

### 可自定義的內容

| 規則類型 | 範例 | 配置 |
|---------|------|------|
| 🌍 **語言** | 只允許中文、只允許英文等 | 阻擋非允許的語言 |
| 🤺 **動作** | 禁止砍擊揮砍、禁止危險特技 | 檢測特定動作 |
| 🔊 **音訊** | 禁止尖叫、禁止大聲叫喊 | 分析臉部表情 |
| 🎨 **視覺風格** | 禁止黑暗主題、禁止血腥 | 檢查視覺美學 |
| 📺 **主題** | 禁止賭博、禁止惡作劇 | 上下文理解 |
| 🔤 **關鍵字** | 自定義黑名單 | 標題/描述匹配 |

### 配置範例

**嚴格模式（4-7 歲）：**
```yaml
custom_rules:
  language:
    allowed_languages: ["中文"]  # 只允許中文
  actions:
    blocked_actions:
      - "砍擊揮砍"  # 禁止揮劍打鬥
      - "危險特技"  # 禁止危險特技
  audio:
    blocked_audio_types:
      - "尖叫"  # 禁止尖叫
```

**寬鬆模式（10-12 歲）：**
```yaml
custom_rules:
  language:
    allowed_languages: ["中文", "英文"]
    action: "warn"  # 警告但不阻擋
  themes:
    blocked_themes:
      - "賭博遊戲"  # 只阻擋賭博
```

📖 **完整文件：** 詳見 [docs/CUSTOM_RULES.md](docs/CUSTOM_RULES.md)

🔧 **配置範本：**
- `config/config.strict.yaml` - 適合幼兒（4-7 歲）
- `config/config.relaxed.yaml` - 適合較大兒童（10-12 歲）

---

## 🌐 Web UI - 家長控制面板（新功能！）

**不用再編輯 YAML 檔案！** 透過美觀的網頁介面配置 KidGuard。

### 功能特色

✨ **5 個配置分頁：**
1. **🔧 基本設定** - API 金鑰、檢測規則、安全頻道
2. **👨‍👩‍👧‍👦 家庭成員** - 新增/管理家庭檔案
3. **🎯 自定義規則** - 所有過濾規則的視覺化配置
4. **📱 通知設定** - Telegram 警報設置
5. **📋 快速範本** - 預先配置的嚴格/寬鬆模式

🎨 **使用者友善：**
- 核取方塊和下拉選單，不用編輯文字
- 即時驗證
- 保存前預覽
- 一鍵測試 API 連線
- 手機響應式設計

### 快速開始

```bash
python web_ui.py
# 開啟 http://localhost:5555
```

📖 **完整 Web UI 指南：** 詳見 [docs/WEB_UI.md](docs/WEB_UI.md)

---

## 🎬 即時監控模式（新功能！）

KidGuard 提供**三種監控模式**以適應不同使用情境：

### 1. 🤖 自動監控（推薦）
**智能、省錢、免人工**

```bash
python live_monitor_auto.py
```

✨ **功能特色：**
- **影片跳轉檢測** - 只在影片切換時擷取
- **視窗標題提取** - 不需要 Selenium/OCR 就能取得影片資訊
- **節省成本** - 比固定間隔少 90% API 調用
- **雙分析模式** - AI 分析或關鍵字過濾
- **自動化** - 不需要手動干預

**運作方式：**
1. 每 2 秒監控 YouTube 視窗標題
2. 檢測影片切換（標題變更）
3. 擷取截圖 + 提取影片資訊（標題、頻道、描述）
4. **選擇分析模式：**
   - **AI 模式**（use_ai_analysis: true）：Claude 分析截圖 → 你執行建議動作
   - **關鍵字模式**（use_ai_analysis: false）：關鍵字過濾 → 自動建議動作
5. 重複下一部影片

💰 **成本：**
- **AI 模式：** 每部影片約 $0.01 美元（約 0.3 台幣）
- **關鍵字模式：** $0（完全免費！）

---

### 2. ⌨️ 手動監控
**完全控制，手動觸發**

```bash
python live_monitor_manual.py
```

✨ **功能特色：**
- 按 Enter 擷取截圖
- 透過指令執行動作
- 最適合抽查

**指令：**
- `Enter` - 擷取截圖
- `close` - 關閉當前分頁
- `redirect` - 前往安全頻道
- `pause` - 暫停影片
- `warn` - 顯示警告
- `ok` - 內容安全

---

### 3. 🔧 完整模式（含人臉識別）
**完整保護與使用者識別**

```bash
python kidguard.py
```

✨ **功能特色：**
- 基於攝影機的觀看者識別
- 基於年齡的規則執行
- 自動干預
- Telegram 通知

---

## 🎯 分析模式：AI vs. 關鍵字過濾

KidGuard 支援**兩種分析模式** — 根據需求和預算選擇：

### 模式 1：AI 分析（use_ai_analysis: true）

**何時使用：**
- 需要深度內容理解
- 檢測細微的不當內容
- 分析視覺元素（暴力、恐怖等）
- 最佳準確度

**運作方式：**
1. 從視窗提取影片標題 + 頻道
2. 擷取截圖
3. 發送到 Claude Vision API 進行分析
4. Claude 提供詳細評估 + 建議動作
5. 你確認並執行

**成本：** 每部影片約 $0.01 美元（約 0.3 台幣）

**配置：**
```yaml
# config/config.yaml
analysis:
  use_ai_analysis: true

claude:
  api_key: "your-api-key"
```

---

### 模式 2：關鍵字過濾（use_ai_analysis: false）

**何時使用：**
- 注重預算（零 API 成本）
- 簡單黑名單過濾就足夠
- 阻擋明顯不當內容
- 快速決策

**運作方式：**
1. 從視窗提取影片標題 + 頻道
2. 對照關鍵字黑名單檢查
3. 如果匹配則自動建議動作
4. 你確認並執行
5. 截圖保存作為記錄（可選）

**成本：** $0（完全免費！）

**配置：**
```yaml
# config/config.yaml
analysis:
  use_ai_analysis: false

  keyword_filter:
    blocked_keywords:
      - "鬼"
      - "恐怖"
      - "暴力"
      # ... 更多關鍵字
    blocked_channels:
      - "恐怖"
      - "靈異"
```

---

### 比較

| 功能 | AI 分析 | 關鍵字過濾 |
|------|---------|-----------|
| **成本** | 約 $0.01/影片 | $0（免費） |
| **準確度** | ⭐⭐⭐⭐⭐ 非常高 | ⭐⭐⭐ 良好 |
| **視覺分析** | ✅ 是 | ❌ 否 |
| **上下文理解** | ✅ 是 | ❌ 否 |
| **速度** | 約 2-3 秒 | 即時 |
| **設定** | 需要 API 金鑰 | 只需關鍵字 |
| **最適合** | 深度保護 | 預算有限 |

**💡 建議：**
- **從關鍵字模式開始**以節省成本
- **需要更深入分析時升級到 AI 模式**
- **混合方法：**使用關鍵字作為預過濾，AI 處理邊緣案例

---

## 📋 內容分析標準

Claude 分析擷取的內容包含：

| 類別 | 範例 | 動作 |
|-----|------|------|
| 🔴 暴力 | 打鬥、武器、血腥 | 立即跳過 |
| 🔴 恐怖 | 驚嚇、詭異內容 | 立即跳過 |
| 🔴 成人 | 性內容、毒品 | 立即跳過 |
| 🟡 不當 | 過度消費主義、點擊誘餌 | 警告 + 記錄 |
| 🟡 兔子洞 | Elsagate 風格、怪異動畫 | 重導向到安全內容 |
| 🟢 安全 | 教育性、適齡 | 允許 |

---

## 🛠️ 安裝

### 前置需求

```bash
# 使用 uv（推薦）
pip install uv
uv venv
uv pip install -r requirements.txt

# 或使用 pip
pip install -r requirements.txt
```

### 選項 1：快速開始 - 自動監控（推薦）🚀

**最快開始保護的方式 - 不需要配置！**

```bash
# 克隆倉庫
git clone https://github.com/sharbui/kidguard.git
cd kidguard

# 安裝依賴
uv pip install -r requirements.txt

# 開始監控
uv run python live_monitor_auto.py

# 開啟 YouTube 並播放影片
# 監控器會自動檢測影片變更並擷取截圖
```

### 選項 2：Web UI 配置 🌐

```bash
# 啟動 Web UI
python web_ui.py

# 在瀏覽器中開啟 http://localhost:5555
# 透過友善的網頁介面配置設定
```

### 選項 3：完整模式（人臉識別 + 自動化）

```bash
# 配置
cp config/config.example.yaml config/config.yaml
# 編輯 config.yaml 填入你的設定

# 執行
python kidguard.py
```

### 配置

```yaml
# config.yaml
claude_api_key: "your-api-key"

family:
  - name: "小雞"
    age: 8
    face_encoding: "encodings/chicken.pkl"
  - name: "鴨鴨"
    age: 6
    face_encoding: "encodings/duck.pkl"
  - name: "臭魚"
    age: 4
    face_encoding: "encodings/fish.pkl"

rules:
  max_child_age: 12
  auto_skip: true
  safe_channels:
    - "UCX6OQ3DkcsbYNE6H8uQQuVA"  # MrBeast
    - "UC295-Dw_tDNtZXFeAPAQKEw"  # Cocomelon

notifications:
  telegram_bot_token: "your-bot-token"
  telegram_chat_id: "your-chat-id"
```

---

## 📱 示範

[示範影片將在此處]

**情境：**
1. 孩子在家用電腦上開啟 YouTube
2. KidGuard 檢測到 YouTube + 識別觀看者為「鴨鴨」（6 歲）
3. 孩子點擊恐怖遊戲影片
4. KidGuard 擷取 5 秒，Claude 分析 →「偵測到恐怖內容」
5. 影片自動跳過到 Cocomelon 節目
6. 家長收到 Telegram 通知及詳細資訊

---

## 👨‍👩‍👧‍👦 為什麼這很重要

- 每天有 **45 億**部影片在 YouTube 上被觀看
- **80%** 的家長擔心孩子在網路上看什麼
- **Elsagate** 向我們展示了演算法驅動的內容如何傷害兒童
- 現有的家長控制很容易被繞過

KidGuard 讓 AI 為保護最脆弱的網路使用者而工作。

---

## 📄 授權

MIT License — 使用它、修改它、用它保護你的孩子。

---

## 🙏 致謝

- 使用 Anthropic 的 [Claude](https://anthropic.com) 建立
- 由 [OpenClaw](https://openclaw.ai) 提供支援
- 由一位厭倦了 24/7 監控 YouTube 的家長用 ❤️ 製作
