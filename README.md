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

### Future Roadmap

- [ ] Family member profile management
- [ ] Viewing history dashboard
- [ ] ~~Custom filter rules~~ ✅ **DONE** - Fully configurable parent rules
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

### Option 1: Quick Start with Web UI (Recommended) 🌐

```bash
# Clone the repo
git clone https://github.com/[username]/kidguard.git
cd kidguard

# Install dependencies
pip install -r requirements.txt

# Launch Web UI
python web_ui.py

# Open http://localhost:5555 in your browser
# Configure settings through the friendly web interface
```

### Option 2: Manual Configuration

```bash
# Clone the repo
git clone https://github.com/[username]/kidguard.git
cd kidguard

# Install dependencies
pip install -r requirements.txt

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
