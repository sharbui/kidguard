# 🎯 家長自定義規則指南 (Custom Rules Guide)

## 概述

KidGuard 允許家長根據自己的育兒理念，設定更細緻的內容過濾規則。這些規則會被整合到 Claude Vision API 的分析提示詞中，實現高度客製化的內容審查。

---

## 📋 配置位置

編輯 `config/config.yaml` 文件中的 `analysis.custom_rules` 部分。

---

## 🔧 可配置規則類型

### 1. 語言限制 (Language Restrictions)

**用途：** 只允許特定語言的內容，避免孩子接觸不熟悉語言的內容。

**配置範例：**
```yaml
custom_rules:
  language:
    enabled: true
    allowed_languages:
      - "中文"
      - "英文"
    action: "block"  # block | warn | redirect
    reason: "非家長允許的語言內容"
```

**效果：**
- 🚫 阻擋非中文/英文的影片
- ✅ Claude 會檢測影片中的語音、字幕、標題等語言
- 📱 違規時立即通知家長

---

### 2. 動作行為限制 (Action/Behavior Restrictions)

**用途：** 禁止特定的動作場景，防止孩子模仿危險行為。

**配置範例：**
```yaml
custom_rules:
  actions:
    enabled: true
    blocked_actions:
      - type: "砍擊揮砍"
        description: "持刀劍等武器進行砍擊、揮砍的動作"
        keywords: ["sword fighting", "slashing", "chopping", "刀劍", "砍殺"]
        severity: "high"

      - type: "危險特技"
        description: "高空跳躍、危險動作可能被模仿"
        keywords: ["dangerous stunts", "jumping", "parkour", "特技", "跳樓"]
        severity: "medium"
    action: "block"
```

**支援的動作類型：**
- 🗡️ 砍擊揮砍（武器動作）
- 👊 拳打腳踢（格鬥場景）
- 🤸 危險特技（高空動作、極限運動）
- 💥 破壞行為（砸東西、破壞物品）

**工作原理：**
- Claude Vision 分析畫面中的動作
- 根據 `keywords` 和視覺特徵判斷
- 即使是卡通或搞笑風格，仍會標記違規

---

### 3. 聲音表現限制 (Audio/Sound Restrictions)

**用途：** 過濾刺耳、驚嚇或不當的音效。

**配置範例：**
```yaml
custom_rules:
  audio:
    enabled: true
    blocked_audio_types:
      - type: "尖叫"
        description: "高分貝尖叫、恐怖音效"
        keywords: ["screaming", "shrieking", "尖叫", "慘叫"]
        severity: "high"

      - type: "誇張大叫"
        description: "過度誇張的叫喊、噪音"
        keywords: ["yelling", "shouting loudly", "大叫", "吼叫"]
        severity: "medium"
    action: "block"
```

**檢測方式：**
- 📸 分析畫面中的臉部表情（張大嘴、驚恐表情）
- 🎭 身體語言線索（雙手抱頭、後退動作）
- 📝 字幕或標題中的關鍵字

**注意：** 由於我們分析的是截圖，無法直接聽到聲音，但 Claude 可以透過視覺線索推測音頻內容。

---

### 4. 視覺風格限制 (Visual Style Restrictions)

**用途：** 過濾特定的視覺風格，例如恐怖、血腥或過度刺激的畫面。

**配置範例：**
```yaml
custom_rules:
  visual:
    enabled: true
    blocked_styles:
      - type: "血腥畫面"
        description: "血液、傷口、屍體等畫面"
        severity: "high"

      - type: "陰暗恐怖"
        description: "黑暗、陰森、恐怖的視覺風格"
        severity: "high"

      - type: "過度閃爍"
        description: "快速閃爍可能引發不適"
        severity: "medium"
    action: "block"
```

**支援的風格類型：**
- 🩸 血腥畫面
- 🌑 陰暗恐怖
- ⚡ 過度閃爍
- 👙 性感暴露

---

### 5. 主題內容限制 (Content Theme Restrictions)

**用途：** 禁止特定主題的影片，即使沒有明顯的不當畫面。

**配置範例：**
```yaml
custom_rules:
  themes:
    enabled: true
    blocked_themes:
      - "賭博遊戲"
      - "戀愛交往"
      - "校園霸凌"
      - "超自然靈異"
      - "開箱炫富"
      - "惡作劇整人"
    action: "block"
```

**常見主題範例：**
- 🎰 賭博遊戲
- 💕 戀愛交往（依年齡可能不適合）
- 😢 校園霸凌
- 👻 超自然靈異
- 📦 開箱炫富（過度消費主義）
- 😈 惡作劇整人

---

### 6. 關鍵字黑名單 (Keyword Blacklist)

**用途：** 直接封鎖包含特定關鍵字的影片。

**配置範例：**
```yaml
custom_rules:
  keywords:
    enabled: true
    blocked_keywords:
      - "鬼"
      - "靈異"
      - "恐怖"
      - "血腥"
      - "殺人"
      - "18+"
      - "成人"
    action: "block"
```

**檢測範圍：**
- 📺 影片標題
- 📝 影片描述
- 🖼️ 畫面中的文字（OCR）

---

## ⚙️ 動作類型 (Action Types)

每個規則都可以設定違規時的處理方式：

| Action | 行為 | 說明 |
|--------|------|------|
| `block` | 🚫 阻擋 | 立即跳過影片或重導向到安全頻道 |
| `warn` | ⚠️ 警告 | 記錄違規但不干預，通知家長 |
| `redirect` | ↪️ 重導向 | 切換到白名單頻道 |

---

## 🎨 實際使用範例

### 範例 1：嚴格模式（適合 4-6 歲）

```yaml
analysis:
  custom_rules:
    language:
      enabled: true
      allowed_languages: ["中文"]  # 只允許中文
      action: "block"

    actions:
      enabled: true
      blocked_actions:
        - type: "砍擊揮砍"
          description: "任何武器動作"
          keywords: ["sword", "knife", "weapon", "刀", "劍"]
          severity: "high"
        - type: "拳打腳踢"
          description: "任何打鬥場景"
          keywords: ["fighting", "punching", "打架"]
          severity: "high"
      action: "block"

    audio:
      enabled: true
      blocked_audio_types:
        - type: "尖叫"
          description: "任何尖叫聲"
          keywords: ["screaming", "尖叫"]
          severity: "high"
      action: "block"

    visual:
      enabled: true
      blocked_styles:
        - type: "陰暗恐怖"
          description: "黑暗場景"
          severity: "high"
      action: "block"

    themes:
      enabled: true
      blocked_themes:
        - "超自然靈異"
        - "恐怖"
        - "打鬥"
      action: "block"
```

### 範例 2：寬鬆模式（適合 10-12 歲）

```yaml
analysis:
  custom_rules:
    language:
      enabled: true
      allowed_languages: ["中文", "英文"]  # 中英文都可以
      action: "warn"  # 只警告不阻擋

    actions:
      enabled: true
      blocked_actions:
        - type: "危險特技"
          description: "極限運動等危險動作"
          keywords: ["dangerous stunts", "特技"]
          severity: "medium"
      action: "warn"  # 記錄但不阻擋

    themes:
      enabled: true
      blocked_themes:
        - "賭博遊戲"
        - "成人內容"
      action: "block"
```

---

## 🔍 技術細節

### Claude Vision 提示詞整合

所有自定義規則會被動態整合到 Claude Vision API 的提示詞中：

```python
# 自動生成的提示詞範例
"""
PARENT CUSTOM RULES (HIGHEST PRIORITY):
============================================================
LANGUAGE RESTRICTIONS:
- ONLY allow content in these languages: 中文, 英文
- If you detect speech or text in other languages, mark as violation

ACTION/BEHAVIOR RESTRICTIONS:
The following actions are STRICTLY PROHIBITED:
  - 砍擊揮砍: 持刀劍等武器進行砍擊、揮砍的動作
    Keywords: sword fighting, slashing, chopping, 刀劍, 砍殺

AUDIO/SOUND RESTRICTIONS:
The following audio patterns are PROHIBITED:
  - 尖叫: 高分貝尖叫、恐怖音效
============================================================
"""
```

### 分析結果格式

```json
{
  "appropriate": false,
  "confidence": 0.95,
  "categories_detected": ["violence", "loud_content"],
  "severity": "high",
  "reason": "影片中出現揮刀動作，違反家長設定的動作限制",
  "recommendation": "block",
  "custom_rule_violations": ["砍擊揮砍", "尖叫"]
}
```

---

## 📊 優先級

規則檢查優先級（由高到低）：

1. **家長自定義規則** ⭐ (Highest priority)
2. **系統預設規則** (暴力、色情、恐怖等)
3. **YouTube 自帶分級**

即使 YouTube 標記為「兒童內容」，只要違反家長自定義規則，仍會被阻擋。

---

## 🛠️ 調試與測試

### 查看實際生成的提示詞

啟用 DEBUG 日誌：

```yaml
logging:
  level: "DEBUG"
```

運行時會輸出：
```
Custom rules enabled: ['language', 'actions', 'audio']
```

### 測試自定義規則

1. 配置規則
2. 運行 KidGuard
3. 播放包含違規內容的影片
4. 檢查 `logs/kidguard.log` 確認規則是否生效

---

## ⚡ 性能考量

- **提示詞長度：** 自定義規則會增加提示詞長度，影響 API 成本
- **分析時間：** 更複雜的規則可能增加 0.5-1 秒分析時間
- **建議：** 只啟用真正需要的規則，避免過度配置

---

## 📞 常見問題

### Q: 可以針對不同孩子設定不同規則嗎？

**A:** 目前版本規則對所有孩子統一生效。未來版本會支援 per-child rules。

### Q: 如果 Claude 誤判怎麼辦？

**A:** 可以調整 `confidence_threshold` 或將特定頻道加入白名單：

```yaml
safe_channels:
  - id: "UCX6OQ3DkcsbYNE6H8uQQuVA"
    name: "MrBeast"
```

### Q: 可以添加自己的規則類型嗎？

**A:** 可以！在 `custom_rules` 下添加新的規則類型，只需確保格式一致即可。

---

## 🚀 進階：創建自己的規則類型

範例：添加「教育價值」檢查

```yaml
custom_rules:
  educational_value:
    enabled: true
    require_educational: true
    min_educational_score: 0.6
    description: "影片必須有教育意義（科學、數學、歷史等）"
    action: "warn"
```

然後在 `content_analyzer.py` 中添加對應的提示詞生成邏輯。

---

## 📚 相關文檔

- [README.md](../README.md) - 專案概述
- [config.example.yaml](../config/config.example.yaml) - 完整配置範例

---

**💡 提示：** 配置規則時，從嚴格開始，逐步放寬，直到找到適合自己家庭的平衡點。

**⚠️ 注意：** KidGuard 是輔助工具，不能完全替代家長的監督與陪伴。
