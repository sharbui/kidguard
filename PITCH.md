# KidGuard — Hackathon Pitch

## One-Liner

**AI-powered YouTube guardian that uses Claude Vision to protect children from inappropriate content in real-time.**

---

## The Problem (30 seconds)

Kids under 6 can't tell YouTube from YouTube Kids. They sit down, click whatever's recommended, and end up watching horror games, violent content, or "Elsagate" weirdness.

YouTube's protections? Useless. "Are you 18?" — *click* — bypassed.

Parents can't watch 24/7. We need AI backup.

---

## The Solution (60 seconds)

**KidGuard** runs in the background and:

1. **Detects** when YouTube opens
2. **Identifies** who's watching via webcam (age estimation or family member recognition)
3. **Monitors** content by capturing short clips
4. **Analyzes** with Claude Vision — is this appropriate for kids?
5. **Acts** — auto-skip, redirect to safe channels, notify parents

All local. Privacy-first. No cloud storage of videos.

---

## Why Claude? (30 seconds)

- **Vision API** understands context, not just keywords
- Can detect subtle inappropriate content (creepy animations, jump scares)
- Fast enough for real-time intervention
- Multi-modal: analyze frames + audio transcription together

---

## Demo Hook (what the judges will see)

Live demo:
1. Open YouTube on a laptop
2. KidGuard detects my "child profile" via webcam
3. Click a Five Nights at Freddy's video
4. 5 seconds later → auto-redirected to Cocomelon
5. My phone buzzes with a Telegram alert: "Blocked horror content for 鴨鴨"

**Boom.** That's the product.

---

## Technical Stack

| Layer | Tech |
|-------|------|
| Detection | Browser extension + process monitor |
| Vision | Webcam + OpenCV + face_recognition |
| Intelligence | **Claude Vision API** |
| Control | Browser automation |
| Notification | Telegram Bot |

---

## Why This Wins

- ✅ **Real problem** — every parent relates
- ✅ **Claude-native** — Vision API is the core
- ✅ **Demo-able** — visual, immediate, impressive
- ✅ **Privacy-conscious** — all local processing
- ✅ **Extensible** — can grow into full parental control suite

---

## Team

Solo developer, parent of three kids (🐔🦆🐟), building what I wish existed.

---

## Ask

Select us for the hackathon. We'll ship a working prototype in 6 days and demo it at the birthday party.

Let's make YouTube safer for kids. 🛡️
