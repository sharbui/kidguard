#!/usr/bin/env python3
"""
KidGuard - Age Detection Test Script

Test the age estimation functionality using Claude Vision API.
"""

import sys
import base64
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    import anthropic
except ImportError:
    print("❌ Error: anthropic package not installed")
    print("   Run: pip install anthropic")
    sys.exit(1)


def analyze_age(image_path: str, api_key: str):
    """Analyze age from image using Claude Vision API."""

    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Get file extension for media type
    ext = Path(image_path).suffix.lower()
    media_type = "image/png" if ext == ".png" else "image/jpeg"

    # Create Claude client
    client = anthropic.Anthropic(api_key=api_key)

    # Age estimation prompt
    prompt = """分析這張圖片中的人物，估計其年齡。

請以 JSON 格式回覆：
{
    "detected": true/false,
    "age_estimate": 估計年齡（數字）,
    "age_range": "年齡範圍（例如：4-6歲）",
    "confidence": 0.0-1.0,
    "is_child": true/false (12歲以下為 true),
    "facial_features": "簡述判斷依據",
    "recommendation": "是否需要啟動家長保護"
}

請仔細觀察臉部特徵、身形比例等來判斷年齡。"""

    # Call Claude Vision API
    print("🔍 正在分析圖片...")
    response = client.messages.create(
        model="claude-sonnet-4-5",
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
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return response.content[0].text


def main():
    """Main test function."""
    print("=" * 60)
    print("🛡️  KidGuard - Age Detection Test")
    print("=" * 60)
    print()

    # Get API key
    api_key = input("請輸入 Claude API Key (或按 Enter 跳過): ").strip()
    if not api_key:
        print("⚠️  未提供 API Key，無法執行測試")
        print("   您可以從 https://console.anthropic.com/ 獲取 API Key")
        sys.exit(1)

    # Test image path
    image_path = "testuserpic/test.jpg"

    if not Path(image_path).exists():
        print(f"❌ 圖片不存在: {image_path}")
        sys.exit(1)

    print(f"📸 測試圖片: {image_path}")
    print()

    try:
        # Analyze
        result = analyze_age(image_path, api_key)

        print("✅ 分析完成！")
        print()
        print("=" * 60)
        print("📊 分析結果：")
        print("=" * 60)
        print(result)
        print()

        # Try to parse JSON
        import json
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            if start >= 0 and end > start:
                data = json.loads(result[start:end])

                print()
                print("=" * 60)
                print("🎯 KidGuard 決策：")
                print("=" * 60)

                if data.get("is_child"):
                    print("⚠️  偵測到兒童！")
                    print(f"   估計年齡: {data.get('age_range', '未知')}")
                    print(f"   信心度: {data.get('confidence', 0) * 100:.1f}%")
                    print()
                    print("🛡️  建議動作:")
                    print("   ✓ 啟動 YouTube 內容監控")
                    print("   ✓ 啟用自定義過濾規則")
                    print("   ✓ 準備 Telegram 通知")
                    print("   ✓ 開始定期擷取螢幕內容")
                else:
                    print("✓ 未偵測到需要保護的兒童")
                    print("  系統將保持待機狀態")

        except json.JSONDecodeError:
            print("⚠️  無法解析 JSON 結果，但分析已完成")

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        sys.exit(1)

    print()
    print("=" * 60)
    print("測試完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
