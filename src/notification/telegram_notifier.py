"""Telegram notification module.

Sends alerts to parents when inappropriate content is detected.
"""

import asyncio
from pathlib import Path
from loguru import logger

try:
    from telegram import Bot
    from telegram.error import TelegramError
except ImportError:
    Bot = None
    TelegramError = Exception


class TelegramNotifier:
    """Sends notifications via Telegram."""
    
    def __init__(self, config: dict):
        self.enabled = config.get("enabled", False)
        self.include_screenshot = config.get("include_screenshot", True)
        self.block_only = config.get("block_only", False)
        
        telegram_config = config.get("telegram", {})
        self.bot_token = telegram_config.get("bot_token")
        self.chat_id = telegram_config.get("chat_id")
        
        self.bot = None
        if Bot and self.bot_token and self.enabled:
            self.bot = Bot(token=self.bot_token)
            logger.info("TelegramNotifier initialized")
        elif self.enabled:
            logger.warning("Telegram notifications enabled but not configured")
    
    async def notify(self, viewer: dict, analysis: dict, action_taken: str):
        """Send notification about detected content.
        
        Args:
            viewer: dict with viewer info (name, age)
            analysis: dict with analysis results
            action_taken: what action was taken (skip, redirect, etc.)
        """
        if not self.bot:
            logger.debug("Telegram not configured, skipping notification")
            return
        
        # Skip warnings if block_only is set
        if self.block_only and analysis.get("recommendation") != "block":
            return
        
        # Build message
        message = self._build_message(viewer, analysis, action_taken)
        
        try:
            await self._send_message(message)
            logger.info("Notification sent to parent")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
    
    def _build_message(self, viewer: dict, analysis: dict, action_taken: str) -> str:
        """Build notification message."""
        severity_emoji = {
            "none": "✅",
            "low": "⚠️",
            "medium": "🟠",
            "high": "🔴"
        }
        
        action_emoji = {
            "skip": "⏭️",
            "redirect": "↩️",
            "pause": "⏸️",
            "notify_only": "📢"
        }
        
        severity = analysis.get("severity", "medium")
        emoji = severity_emoji.get(severity, "⚠️")
        action_icon = action_emoji.get(action_taken, "📢")
        
        categories = ", ".join(analysis.get("categories", [])) or "Unknown"
        
        message = f"""🛡️ **KidGuard Alert**

{emoji} **Inappropriate content detected**

👤 **Viewer:** {viewer.get('name', 'Unknown')} (age {viewer.get('age', '?')})
📋 **Categories:** {categories}
⚡ **Severity:** {severity.upper()}
📝 **Reason:** {analysis.get('reason', 'N/A')}

{action_icon} **Action taken:** {action_taken.replace('_', ' ').title()}

---
_Confidence: {analysis.get('confidence', 0):.0%}_"""
        
        return message
    
    async def _send_message(self, message: str):
        """Send message via Telegram."""
        if not self.bot or not self.chat_id:
            return
        
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode="Markdown"
        )
    
    async def send_screenshot(self, image_path: str, caption: str = ""):
        """Send screenshot with notification."""
        if not self.bot or not self.chat_id:
            return
        
        path = Path(image_path)
        if not path.exists():
            logger.warning(f"Screenshot not found: {image_path}")
            return
        
        try:
            with open(path, "rb") as photo:
                await self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=photo,
                    caption=caption
                )
        except TelegramError as e:
            logger.error(f"Failed to send screenshot: {e}")
    
    async def test_connection(self) -> bool:
        """Test Telegram connection."""
        if not self.bot:
            return False
        
        try:
            me = await self.bot.get_me()
            logger.info(f"Connected to Telegram as @{me.username}")
            return True
        except TelegramError as e:
            logger.error(f"Telegram connection failed: {e}")
            return False
