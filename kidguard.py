#!/usr/bin/env python3
"""
KidGuard - AI-powered YouTube content guardian for young children

Main entry point for the application.
"""

import asyncio
import signal
import sys
from pathlib import Path
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.detection.youtube_detector import YouTubeDetector
from src.vision.face_recognition import FaceRecognizer
from src.vision.content_analyzer import ContentAnalyzer
from src.control.browser_controller import BrowserController
from src.notification.telegram_notifier import TelegramNotifier
from src.config import load_config


class KidGuard:
    """Main KidGuard application."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = load_config(config_path)
        self.running = False
        
        # Initialize components
        self.detector = YouTubeDetector()
        self.face_recognizer = FaceRecognizer(self.config.get("family", []))

        # Prepare analyzer config with custom rules
        analyzer_config = {
            **self.config.get("claude", {}),
            "custom_rules": self.config.get("analysis", {}).get("custom_rules", {}),
            "max_child_age": self.config.get("rules", {}).get("max_child_age", 12)
        }
        self.content_analyzer = ContentAnalyzer(analyzer_config)

        self.browser_controller = BrowserController()
        self.notifier = TelegramNotifier(self.config.get("notifications", {}))
        
        logger.info("KidGuard initialized")
    
    async def run(self):
        """Main run loop."""
        self.running = True
        logger.info("KidGuard started - protecting your kids 🛡️")
        
        while self.running:
            try:
                # Step 1: Check if YouTube is open
                youtube_active = await self.detector.is_youtube_active()
                
                if youtube_active:
                    logger.debug("YouTube detected")
                    
                    # Step 2: Identify viewer
                    viewer = await self.face_recognizer.identify_viewer()
                    
                    if viewer and viewer.get("is_child", False):
                        logger.info(f"Child detected: {viewer['name']} (age {viewer['age']})")
                        
                        # Step 3: Capture and analyze content
                        clip = await self.detector.capture_clip(
                            duration=self.config.get("rules", {}).get("clip_duration", 5)
                        )
                        
                        analysis = await self.content_analyzer.analyze(clip)
                        
                        # Step 4: Take action if needed
                        if analysis.get("inappropriate", False):
                            logger.warning(f"Inappropriate content detected: {analysis['reason']}")
                            
                            # Take action
                            action = self.config.get("rules", {}).get("action", "redirect")
                            await self._take_action(action, analysis)
                            
                            # Notify parent
                            await self.notifier.notify(
                                viewer=viewer,
                                analysis=analysis,
                                action_taken=action
                            )
                
                # Wait before next check
                interval = self.config.get("rules", {}).get("check_interval", 30)
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(5)
    
    async def _take_action(self, action: str, analysis: dict):
        """Take action on inappropriate content."""
        if action == "skip":
            await self.browser_controller.skip_video()
        elif action == "redirect":
            safe_channels = self.config.get("safe_channels", [])
            if safe_channels:
                await self.browser_controller.redirect_to_channel(safe_channels[0]["id"])
        elif action == "pause":
            await self.browser_controller.pause_video()
        # notify_only: just log and notify, no browser action
    
    def stop(self):
        """Stop the application."""
        logger.info("Stopping KidGuard...")
        self.running = False


def main():
    """Entry point."""
    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        level="INFO"
    )
    logger.add(
        "logs/kidguard.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG"
    )
    
    # Create application
    app = KidGuard()
    
    # Handle shutdown signals
    def shutdown(sig, frame):
        app.stop()
    
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    
    # Run
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    
    logger.info("KidGuard stopped. Stay safe! 👋")


if __name__ == "__main__":
    main()
