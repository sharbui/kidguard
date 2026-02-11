# 🛡️ KidGuard

> AI-powered YouTube content guardian for young children

## Hackathon Submission

**Event:** Built with Opus 4.6: The Claude Code Hackathon  
**Team Size:** 1  
**Timeline:** Feb 10-16, 2026

---

## 🎯 The Problem

Every parent knows this scenario:

Your 5-year-old sits down at the computer. Within seconds, they've opened YouTube (not YouTube Kids) and started clicking through autoplay recommendations. By the time you notice, they've stumbled onto content that's inappropriate, scary, or just plain weird.

**YouTube's age verification?** A joke. Kids just click "I'm over 18" without reading.

**Restricted Mode?** One toggle away from being disabled.

**YouTube Kids?** Great, but kids don't know the difference — they just see "the video app."

Parents can't monitor 24/7. We need AI to help.

### A Parent's Reality

*"Sure, you might say: just don't let kids touch screens or YouTube — problem solved!"*

But here's my reality as a father of three:

**My first child** grew up without TV or tablets until elementary school. Just books. By kindergarten, he was reading at a 4th-grade level.

**Then came child #2, and #3.** Suddenly it's just Mom and Dad managing three kids. We can't give each one the same one-on-one attention. We can't even catch our breath.

**That's when we needed help.** Not to replace parenting, but to **extend our reach** when we physically can't be everywhere at once.

This is where AI can truly help families:
- **Not just AdGuard** or simple blocklists
- **Intelligent, context-aware protection** that understands what kids are actually watching
- **Low-cost, embedded assistance** that doesn't require a computer science degree
- **A safety net** for when parents are cooking dinner, helping with homework, or just trying to survive the day

Many people say they're afraid to have kids, or don't know how to raise them. What if AI could make parenting more manageable? What if technology could be a **guardian**, not just a babysitter?

That's the idea behind KidGuard.

---

## 💡 The Solution

**KidGuard** uses Claude's vision capabilities to create a real-time content guardian:

```
[YouTube Opens] 
       ↓
[Webcam Check] → Who's watching? (Age estimation / Family member ID)
       ↓
   Under 12?
       ↓ Yes
[Capture 5-sec clip]
       ↓
[Claude Vision Analysis] → Is this kid-appropriate?
       ↓
   Inappropriate?
       ↓ Yes
[Auto-skip / Redirect to safe channel]
       ↓
[Notify parent via Telegram]
```

### Why Claude?

- **Vision API** analyzes video frames for violence, horror, adult themes, and "YouTube rabbit hole" content
- **Nuanced understanding** — not just keyword blocking, but contextual analysis
- **Multi-modal** — can analyze both visuals AND audio transcription
- **Fast enough** for real-time intervention

---

## 🔧 Technical Architecture

| Component | Technology | Notes |
|-----------|------------|-------|
| YouTube Detection | Browser extension / Process monitor | Detects youtube.com |
| Face Recognition | OpenCV + face_recognition | Local processing, privacy-first |
| Age Estimation | Claude Vision | Fallback for unknown faces |
| Screen Capture | ffmpeg / Windows API | 5-second clips |
| Content Analysis | **Claude Vision API** | Core intelligence |
| Browser Control | Puppeteer / Extension API | Skip / redirect |
| Parent Notification | Telegram Bot | Real-time alerts |

### Privacy-First Design

- All face recognition runs **locally**
- Video clips are analyzed and immediately deleted
- No data leaves the device except API calls to Claude
- Parent controls what gets logged

---

## 🚀 Features

### MVP (Hackathon Scope)

- [x] Detect YouTube browser activity
- [x] Webcam-based viewer identification
- [x] Age estimation for unknown viewers
- [x] Screen capture of YouTube content
- [x] Claude Vision content analysis
- [x] Auto-skip inappropriate content
- [x] Redirect to whitelisted channels
- [x] Telegram notifications to parents
- [x] **🆕 Parent custom rules** (language, actions, audio, themes, keywords)
- [x] **🆕 Smart video transition detection** - Only analyzes when videos change (saves API costs)
- [x] **🆕 Window title extraction** - Gets video info without Selenium/OCR
- [x] **🆕 Auto monitoring mode** - Hands-free protection

### Future Roadmap

- [ ] Family member profile management
- [ ] Viewing history dashboard
- [ ] ~~Custom filter rules~~ ✅ **DONE** - Fully configurable parent rules
- [ ] ~~Video transition detection~~ ✅ **DONE** - Smart cost-saving analysis
- [ ] Audio analysis (screaming, profanity detection)
- [ ] Cross-platform support (tablet, phone)
- [ ] Integration with router-level controls
- [ ] Per-child custom rules

---

## 🎯 Parent Custom Rules (NEW!)

KidGuard now supports **highly customizable filtering rules** that let parents define exactly what content is appropriate for their children:

### What You Can Customize

| Rule Type | Examples | Configuration |
|-----------|----------|---------------|
| 🌍 **Language** | Only Chinese, Only English, etc. | Block non-allowed languages |
| 🤺 **Actions** | No sword fighting, No dangerous stunts | Detect specific movements |
| 🔊 **Audio** | No screaming, No loud yelling | Analyze facial expressions |
| 🎨 **Visual Style** | No dark themes, No blood | Check visual aesthetics |
| 📺 **Themes** | No gambling, No pranks | Context understanding |
| 🔤 **Keywords** | Custom blacklist | Title/description matching |

### Configuration Examples

**Strict Mode (Ages 4-7):**
```yaml
custom_rules:
  language:
    allowed_languages: ["中文"]  # Chinese only
  actions:
    blocked_actions:
      - "砍擊揮砍"  # No sword fighting
      - "危險特技"  # No dangerous stunts
  audio:
    blocked_audio_types:
      - "尖叫"  # No screaming
```

**Relaxed Mode (Ages 10-12):**
```yaml
custom_rules:
  language:
    allowed_languages: ["中文", "英文"]
    action: "warn"  # Warn but don't block
  themes:
    blocked_themes:
      - "賭博遊戲"  # Gambling only
```

📖 **Full Documentation:** See [docs/CUSTOM_RULES.md](docs/CUSTOM_RULES.md) for detailed guide

🔧 **Config Templates:**
- `config/config.strict.yaml` - For young children (ages 4-7)
- `config/config.relaxed.yaml` - For older children (ages 10-12)

---

## 🌐 Web UI - Parent Control Panel (NEW!)

**No more editing YAML files!** Configure KidGuard through a beautiful web interface.

### Features

✨ **5 Configuration Tabs:**
1. **🔧 Basic Settings** - API keys, detection rules, safe channels
2. **👨‍👩‍👧‍👦 Family Members** - Add/manage family profiles
3. **🎯 Custom Rules** - Visual configuration of all filtering rules
4. **📱 Notifications** - Telegram alerts setup
5. **📋 Quick Templates** - Pre-configured strict/relaxed modes

🎨 **User-Friendly:**
- Checkboxes and dropdowns instead of text editing
- Real-time validation
- Preview before saving
- Test API connection with one click
- Mobile-responsive design

### Quick Start

```bash
python web_ui.py
# Open http://localhost:5555
```

📖 **Full Web UI Guide:** See [docs/WEB_UI.md](docs/WEB_UI.md)

---

## 🎬 Live Monitoring Modes (NEW!)

KidGuard offers **three monitoring modes** to fit different use cases:

### 1. 🤖 Auto Monitor (Recommended)
**Smart, cost-efficient, hands-free**

```bash
python live_monitor_auto.py
```

✨ **Features:**
- **Video transition detection** - Only captures when videos change
- **Window title extraction** - Gets video info without Selenium/OCR
- **Cost-saving** - ~90% fewer API calls vs. fixed interval
- **Dual analysis modes** - AI analysis OR keyword filtering
- **Automatic** - No manual intervention needed

**How it works:**
1. Monitors YouTube window title every 2 seconds
2. Detects when video changes (title change)
3. Captures screenshot + extracts video info (title, channel, description)
4. **Choose analysis mode:**
   - **AI Mode** (use_ai_analysis: true): Claude analyzes screenshot → You execute recommended action
   - **Keyword Mode** (use_ai_analysis: false): Keyword filtering → Auto-suggest action
5. Repeats for next video

💰 **Cost:**
- **AI Mode:** ~$0.01 per video (~0.3 TWD)
- **Keyword Mode:** $0 (completely free!)

---

### 2. ⌨️ Manual Monitor
**Full control, manual triggering**

```bash
python live_monitor_manual.py
```

✨ **Features:**
- Press Enter to capture screenshot
- Execute actions via commands
- Best for spot-checking

**Commands:**
- `Enter` - Capture screenshot
- `close` - Close current tab
- `redirect` - Go to safe channel
- `pause` - Pause video
- `warn` - Show warning
- `ok` - Content is safe

---

### 3. 🔧 Full Mode (with Face Recognition)
**Complete protection with user identification**

```bash
python kidguard.py
```

✨ **Features:**
- Webcam-based viewer identification
- Age-based rule enforcement
- Automatic intervention
- Telegram notifications

---

## 🎯 Analysis Modes: AI vs. Keyword Filtering

KidGuard supports **two analysis modes** - choose based on your needs and budget:

### Mode 1: AI Analysis (use_ai_analysis: true)

**When to use:**
- Need deep content understanding
- Detect subtle inappropriate content
- Analyze visual elements (violence, horror, etc.)
- Best accuracy

**How it works:**
1. Extract video title + channel from window
2. Capture screenshot
3. Send to Claude Vision API for analysis
4. Claude provides detailed assessment + recommended action
5. You confirm and execute

**Cost:** ~$0.01 per video (~0.3 TWD)

**Configuration:**
```yaml
# config/config.yaml
analysis:
  use_ai_analysis: true

claude:
  api_key: "your-api-key"
```

---

### Mode 2: Keyword Filtering (use_ai_analysis: false)

**When to use:**
- Budget-conscious (zero API costs)
- Simple blacklist filtering is enough
- Block obvious inappropriate content
- Fast decision making

**How it works:**
1. Extract video title + channel from window
2. Check against keyword blacklist
3. Auto-suggest action if match found
4. You confirm and execute
5. Screenshot saved for records (optional)

**Cost:** $0 (completely free!)

**Configuration:**
```yaml
# config/config.yaml
analysis:
  use_ai_analysis: false

  keyword_filter:
    blocked_keywords:
      - "鬼"
      - "恐怖"
      - "暴力"
      # ... more keywords
    blocked_channels:
      - "恐怖"
      - "靈異"
```

---

### Comparison

| Feature | AI Analysis | Keyword Filtering |
|---------|-------------|-------------------|
| **Cost** | ~$0.01/video | $0 (Free) |
| **Accuracy** | ⭐⭐⭐⭐⭐ Very High | ⭐⭐⭐ Good |
| **Visual Analysis** | ✅ Yes | ❌ No |
| **Context Understanding** | ✅ Yes | ❌ No |
| **Speed** | ~2-3 seconds | Instant |
| **Setup** | Need API key | Just keywords |
| **Best for** | Deep protection | Budget-conscious |

**💡 Recommendation:**
- **Start with Keyword Mode** to save costs
- **Upgrade to AI Mode** when you need deeper analysis
- **Hybrid approach:** Use keyword as pre-filter, AI for edge cases

---

## 📋 Content Analysis Criteria

Claude analyzes captured content for:

| Category | Examples | Action |
|----------|----------|--------|
| 🔴 Violence | Fighting, weapons, gore | Immediate skip |
| 🔴 Horror | Jump scares, creepy content | Immediate skip |
| 🔴 Adult | Sexual content, drugs | Immediate skip |
| 🟡 Inappropriate | Excessive consumerism, clickbait | Warn + log |
| 🟡 Rabbit Hole | Elsagate-style, weird animations | Redirect to safe content |
| 🟢 Safe | Educational, age-appropriate | Allow |

---

## 🛠️ Installation

### Prerequisites

```bash
# Using uv (recommended)
pip install uv
uv venv
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### Option 1: Quick Start - Auto Monitor (Recommended) 🚀

**Fastest way to start protecting - no configuration needed!**

```bash
# Clone the repo
git clone https://github.com/sharbui/kidguard.git
cd kidguard

# Install dependencies
uv pip install -r requirements.txt

# Start monitoring
uv run python live_monitor_auto.py

# Open YouTube and play videos
# Monitor will auto-detect video changes and capture screenshots
```

### Option 2: Web UI Configuration 🌐

```bash
# Launch Web UI
python web_ui.py

# Open http://localhost:5555 in your browser
# Configure settings through the friendly web interface
```

### Option 3: Full Mode (Face Recognition + Automation)

```bash
# Configure
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your settings

# Run
python kidguard.py
```

### Configuration

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

## 📱 Demo

[Demo video will be here]

**Scenario:**
1. Child opens YouTube on family computer
2. KidGuard detects YouTube + identifies viewer as "鴨鴨" (age 6)
3. Child clicks on a horror game video
4. KidGuard captures 5 seconds, Claude analyzes → "Horror content detected"
5. Video auto-skips to a Cocomelon episode
6. Parent receives Telegram notification with details

---

## 👨‍👩‍👧‍👦 Why This Matters

- **4.5 billion** videos are watched on YouTube daily
- **80%** of parents worry about what their kids watch online
- **Elsagate** showed us how algorithm-driven content can harm children
- Existing parental controls are easily bypassed

KidGuard puts AI to work protecting the most vulnerable internet users.

---

## 📄 License

MIT License — Use it, modify it, protect your kids with it.

---

## 🙏 Acknowledgments

- Built with [Claude](https://anthropic.com) by Anthropic
- Powered by [OpenClaw](https://openclaw.ai)
- Made with ❤️ by a parent who's tired of monitoring YouTube 24/7
