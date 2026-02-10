#!/usr/bin/env python3
"""
KidGuard Web UI - Parent Configuration Interface

A friendly web interface for parents to configure KidGuard settings
without manually editing YAML files.
"""

import os
import sys
import yaml
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

app = Flask(__name__,
            template_folder='web/templates',
            static_folder='web/static')

CONFIG_PATH = Path("config/config.yaml")
EXAMPLE_CONFIG_PATH = Path("config/config.example.yaml")


@app.route('/')
def index():
    """Main settings page."""
    return render_template('settings.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration."""
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        else:
            # Load example config as default
            with open(EXAMPLE_CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

        return jsonify({
            'success': True,
            'config': config,
            'exists': CONFIG_PATH.exists()
        })
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config', methods=['POST'])
def save_config():
    """Save configuration."""
    try:
        config = request.json

        # Validate config structure
        if not isinstance(config, dict):
            return jsonify({
                'success': False,
                'error': 'Invalid configuration format'
            }), 400

        # Ensure config directory exists
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Save config
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        logger.info(f"Configuration saved to {CONFIG_PATH}")

        return jsonify({
            'success': True,
            'message': '配置已成功保存！'
        })
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config/templates', methods=['GET'])
def get_templates():
    """Get available configuration templates."""
    templates = {}

    template_files = {
        'strict': 'config/config.strict.yaml',
        'relaxed': 'config/config.relaxed.yaml',
        'example': 'config/config.example.yaml'
    }

    for name, path in template_files.items():
        try:
            if Path(path).exists():
                with open(path, 'r', encoding='utf-8') as f:
                    templates[name] = yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Failed to load template {name}: {e}")

    return jsonify({
        'success': True,
        'templates': templates
    })


@app.route('/api/config/validate', methods=['POST'])
def validate_config():
    """Validate configuration."""
    try:
        config = request.json

        errors = []
        warnings = []

        # Check required fields
        if 'claude' not in config:
            errors.append('缺少 Claude API 配置')
        elif not config['claude'].get('api_key'):
            warnings.append('未設定 Claude API Key')

        if 'family' not in config or not config['family']:
            warnings.append('未添加家庭成員')

        if 'analysis' in config:
            custom_rules = config['analysis'].get('custom_rules', {})
            enabled_rules = [k for k, v in custom_rules.items()
                           if isinstance(v, dict) and v.get('enabled')]

            if not enabled_rules:
                warnings.append('未啟用任何自定義規則')

        # Check notification settings
        if config.get('notifications', {}).get('enabled'):
            telegram = config['notifications'].get('telegram', {})
            if telegram.get('enabled') and not telegram.get('bot_token'):
                warnings.append('Telegram 通知已啟用但未設定 bot token')

        return jsonify({
            'success': True,
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/test/claude', methods=['POST'])
def test_claude_api():
    """Test Claude API connection."""
    try:
        api_key = request.json.get('api_key')

        if not api_key:
            return jsonify({
                'success': False,
                'error': '請提供 API Key'
            }), 400

        # Test API connection
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "請回覆：KidGuard API 測試成功！"
            }]
        )

        return jsonify({
            'success': True,
            'message': 'API 連接成功！',
            'response': response.content[0].text
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'API 測試失敗：{str(e)}'
        }), 500


@app.route('/api/family/capture', methods=['POST'])
def capture_family_member():
    """Capture face for family member registration."""
    # This would integrate with the face recognition module
    # For now, return a placeholder
    return jsonify({
        'success': True,
        'message': '功能開發中...'
    })


def main():
    """Start the web UI."""
    logger.info("Starting KidGuard Web UI...")
    logger.info("Open http://localhost:5555 in your browser")

    app.run(
        host='0.0.0.0',
        port=5555,
        debug=True
    )


if __name__ == '__main__':
    main()
