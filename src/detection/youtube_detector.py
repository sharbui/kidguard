"""YouTube detection module.

Detects when YouTube is being accessed via browser.
"""

import asyncio
from pathlib import Path
from datetime import datetime
from loguru import logger

try:
    import psutil
except ImportError:
    psutil = None

try:
    import mss
    import mss.tools
except ImportError:
    mss = None


class YouTubeDetector:
    """Detects YouTube activity and captures content."""
    
    YOUTUBE_DOMAINS = ["youtube.com", "youtu.be", "www.youtube.com"]
    BROWSER_PROCESSES = ["chrome", "firefox", "msedge", "brave", "opera"]
    
    def __init__(self):
        self.last_capture = None
        self.capture_dir = Path("captures")
        self.capture_dir.mkdir(exist_ok=True)
        logger.info("YouTubeDetector initialized")
    
    async def is_youtube_active(self) -> bool:
        """Check if YouTube is currently active in any browser.
        
        TODO: Implement proper detection:
        - Option 1: Browser extension that reports active tab
        - Option 2: Window title monitoring
        - Option 3: Network traffic analysis
        """
        # Placeholder: check for browser windows with "YouTube" in title
        return await self._check_window_titles()
    
    async def _check_window_titles(self) -> bool:
        """Check window titles for YouTube."""
        # This is a simplified check
        # Real implementation would use win32gui on Windows
        # or similar APIs on other platforms
        
        if psutil is None:
            logger.warning("psutil not installed, cannot check processes")
            return False
        
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                name = proc.info['name'].lower()
                if any(browser in name for browser in self.BROWSER_PROCESSES):
                    # Browser is running - assume YouTube might be active
                    # Real implementation would check window title
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False
    
    async def capture_clip(self, duration: int = 5) -> dict:
        """Capture screen clip for analysis.
        
        Args:
            duration: Duration in seconds
            
        Returns:
            dict with 'frames' (list of image paths) and 'audio' (path or None)
        """
        if mss is None:
            logger.error("mss not installed, cannot capture screen")
            return {"frames": [], "audio": None}
        
        frames = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with mss.mss() as sct:
            # Capture frames over duration
            for i in range(min(duration, 5)):  # Max 5 frames
                screenshot = sct.grab(sct.monitors[1])  # Primary monitor
                
                # Save frame
                frame_path = self.capture_dir / f"frame_{timestamp}_{i}.png"
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=str(frame_path))
                frames.append(str(frame_path))
                
                await asyncio.sleep(1)
        
        self.last_capture = {
            "frames": frames,
            "audio": None,  # TODO: Implement audio capture
            "timestamp": timestamp
        }
        
        logger.debug(f"Captured {len(frames)} frames")
        return self.last_capture
    
    async def cleanup_captures(self):
        """Delete old capture files."""
        for file in self.capture_dir.glob("frame_*.png"):
            try:
                file.unlink()
            except Exception as e:
                logger.warning(f"Could not delete {file}: {e}")
