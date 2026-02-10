"""Content analysis module using Claude Vision API."""

import base64
import asyncio
from pathlib import Path
from loguru import logger

try:
    import anthropic
except ImportError:
    anthropic = None


class ContentAnalyzer:
    """Analyzes video content using Claude Vision API."""

    BASE_PROMPT_TEMPLATE = """You are a content safety analyzer for children's media.

Analyze this screenshot from a YouTube video and determine if it's appropriate for children under {max_age}.

Evaluate for STANDARD categories:
1. Violence (fighting, weapons, gore, death)
2. Horror (scary imagery, jump scares, creepy content)
3. Adult content (sexual themes, nudity)
4. Drugs/alcohol
5. Gambling
6. Disturbing content (Elsagate-style, weird animations targeting kids)
7. Excessive profanity
8. Dangerous activities kids might imitate

{custom_rules_section}

Respond in JSON format:
{{
    "appropriate": true/false,
    "confidence": 0.0-1.0,
    "categories_detected": ["category1", "category2"],
    "severity": "none" | "low" | "medium" | "high",
    "reason": "Brief explanation",
    "recommendation": "allow" | "warn" | "block",
    "custom_rule_violations": ["rule1", "rule2"]
}}

Be cautious - when in doubt, flag for review. Children's safety is the priority."""

    def __init__(self, config: dict):
        self.api_key = config.get("api_key")
        self.model = config.get("model", "claude-sonnet-4-5")
        self.custom_rules = config.get("custom_rules", {})
        self.max_child_age = config.get("max_child_age", 12)
        self.client = None

        # Generate analysis prompt with custom rules
        self.analysis_prompt = self._build_analysis_prompt()

        if anthropic and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            logger.info("ContentAnalyzer initialized with Claude API")
            logger.info(f"Custom rules enabled: {self._get_enabled_rules()}")
        else:
            logger.warning("Claude API not configured - content analysis disabled")

    def _get_enabled_rules(self) -> list:
        """Get list of enabled custom rule types."""
        enabled = []
        for rule_type, rule_config in self.custom_rules.items():
            if isinstance(rule_config, dict) and rule_config.get("enabled"):
                enabled.append(rule_type)
        return enabled

    def _build_analysis_prompt(self) -> str:
        """Build analysis prompt with custom rules from config."""
        custom_sections = []

        # Language restrictions
        if self.custom_rules.get("language", {}).get("enabled"):
            lang_config = self.custom_rules["language"]
            allowed = lang_config.get("allowed_languages", [])
            if allowed:
                langs_str = ", ".join(allowed)
                custom_sections.append(f"""
LANGUAGE RESTRICTIONS:
- ONLY allow content in these languages: {langs_str}
- If you detect speech or text in other languages, mark as violation
- Check video title, on-screen text, and spoken language""")

        # Action restrictions
        if self.custom_rules.get("actions", {}).get("enabled"):
            actions = self.custom_rules["actions"].get("blocked_actions", [])
            if actions:
                action_list = []
                for action in actions:
                    action_type = action.get("type", "")
                    desc = action.get("description", "")
                    keywords = ", ".join(action.get("keywords", []))
                    action_list.append(f"  - {action_type}: {desc}")
                    if keywords:
                        action_list.append(f"    Keywords: {keywords}")

                custom_sections.append(f"""
ACTION/BEHAVIOR RESTRICTIONS:
The following actions are STRICTLY PROHIBITED:
{chr(10).join(action_list)}
- Look for these movements, gestures, or activities in the video
- Even if cartoonish or comedic, still flag as violation""")

        # Audio restrictions
        if self.custom_rules.get("audio", {}).get("enabled"):
            audio_types = self.custom_rules["audio"].get("blocked_audio_types", [])
            if audio_types:
                audio_list = []
                for audio in audio_types:
                    audio_type = audio.get("type", "")
                    desc = audio.get("description", "")
                    audio_list.append(f"  - {audio_type}: {desc}")

                custom_sections.append(f"""
AUDIO/SOUND RESTRICTIONS:
The following audio patterns are PROHIBITED:
{chr(10).join(audio_list)}
- Analyze facial expressions and body language that suggest these sounds
- Check for visual cues like open mouths (screaming), angry faces (yelling)""")

        # Visual style restrictions
        if self.custom_rules.get("visual", {}).get("enabled"):
            styles = self.custom_rules["visual"].get("blocked_styles", [])
            if styles:
                style_list = []
                for style in styles:
                    style_type = style.get("type", "")
                    desc = style.get("description", "")
                    style_list.append(f"  - {style_type}: {desc}")

                custom_sections.append(f"""
VISUAL STYLE RESTRICTIONS:
The following visual styles are NOT ALLOWED:
{chr(10).join(style_list)}
- Analyze color palette, lighting, composition, and overall visual tone""")

        # Theme restrictions
        if self.custom_rules.get("themes", {}).get("enabled"):
            themes = self.custom_rules["themes"].get("blocked_themes", [])
            if themes:
                themes_str = ", ".join(themes)
                custom_sections.append(f"""
THEME/TOPIC RESTRICTIONS:
Prohibited themes: {themes_str}
- Check video context for these themes
- Consider title, thumbnail, and visible content""")

        # Keyword blacklist
        if self.custom_rules.get("keywords", {}).get("enabled"):
            keywords = self.custom_rules["keywords"].get("blocked_keywords", [])
            if keywords:
                keywords_str = ", ".join(keywords)
                custom_sections.append(f"""
KEYWORD BLACKLIST:
Blocked keywords: {keywords_str}
- Check for these words in video title, description, or on-screen text
- Any match should be flagged as violation""")

        # Combine all sections
        if custom_sections:
            custom_rules_text = "\n" + "="*60 + "\nPARENT CUSTOM RULES (HIGHEST PRIORITY):\n" + "="*60 + "\n".join(custom_sections) + "\n" + "="*60
        else:
            custom_rules_text = ""

        return self.BASE_PROMPT_TEMPLATE.format(
            max_age=self.max_child_age,
            custom_rules_section=custom_rules_text
        )
    
    async def analyze(self, capture: dict) -> dict:
        """Analyze captured content.
        
        Args:
            capture: dict with 'frames' (list of image paths) and 'audio' (optional)
            
        Returns:
            Analysis result dict
        """
        if not self.client:
            logger.warning("No Claude client available")
            return self._default_result()
        
        frames = capture.get("frames", [])
        if not frames:
            logger.warning("No frames to analyze")
            return self._default_result()
        
        # Analyze the middle frame (most representative)
        frame_path = frames[len(frames) // 2]
        
        try:
            result = await self._analyze_frame(frame_path)
            
            # Map result to our format
            return {
                "inappropriate": result.get("recommendation") == "block",
                "reason": result.get("reason", "Unknown"),
                "categories": result.get("categories_detected", []),
                "severity": result.get("severity", "none"),
                "confidence": result.get("confidence", 0),
                "recommendation": result.get("recommendation", "allow"),
                "raw_response": result
            }
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return self._default_result()
    
    async def _analyze_frame(self, frame_path: str) -> dict:
        """Analyze a single frame using Claude Vision."""
        # Read and encode image
        with open(frame_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        # Get file extension for media type
        ext = Path(frame_path).suffix.lower()
        media_type = "image/png" if ext == ".png" else "image/jpeg"
        
        # Call Claude Vision API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": self.analysis_prompt
                        }
                    ]
                }
            ]
        )
        
        # Parse JSON response
        import json
        response_text = response.content[0].text
        
        # Try to extract JSON from response
        try:
            # Find JSON in response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response_text[start:end])
        except json.JSONDecodeError:
            pass
        
        # Fallback: assume safe if we can't parse
        logger.warning("Could not parse analysis response")
        return {
            "appropriate": True,
            "confidence": 0.5,
            "categories_detected": [],
            "severity": "none",
            "reason": "Could not analyze",
            "recommendation": "allow"
        }
    
    def _default_result(self) -> dict:
        """Return default (safe) result when analysis unavailable."""
        return {
            "inappropriate": False,
            "reason": "Analysis unavailable",
            "categories": [],
            "severity": "none",
            "confidence": 0,
            "recommendation": "allow"
        }
