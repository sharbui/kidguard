// KidGuard i18n - Internationalization

const translations = {
    'zh-TW': {
        // Header
        'app.title': 'KidGuard 家長控制面板',
        'app.subtitle': '保護您的孩子免受不當內容影響',

        // Status
        'status.ready': '準備就緒',
        'status.loading': '載入中...',
        'status.saving': '保存中...',
        'status.saved': '已保存',
        'status.error': '錯誤',

        // Tabs
        'tab.basic': '基本設定',
        'tab.family': '家庭成員',
        'tab.rules': '自定義規則',
        'tab.notifications': '通知設定',
        'tab.templates': '快速模板',

        // Basic Settings
        'basic.title': '基本設定',
        'basic.claude.title': 'Claude API 配置',
        'basic.claude.apikey': 'API Key',
        'basic.claude.model': '模型選擇',
        'basic.claude.test': '測試連接',

        'basic.rules.title': '檢測規則',
        'basic.rules.age': '保護年齡上限',
        'basic.rules.action': '偵測到不當內容時',
        'basic.rules.interval': '檢查間隔（秒）',
        'basic.rules.threshold': '信心閾值',

        'basic.channels.title': '安全頻道白名單',
        'basic.channels.add': '添加安全頻道',

        // Action types
        'action.redirect': '重導向到安全頻道',
        'action.skip': '跳過影片',
        'action.pause': '暫停播放',
        'action.notify': '僅通知家長',

        // Family
        'family.title': '家庭成員管理',
        'family.desc': '添加家庭成員以啟用臉部識別功能',
        'family.add': '添加家庭成員',
        'family.name': '姓名',
        'family.age': '歲',
        'family.child': '兒童',
        'family.delete': '刪除',

        // Custom Rules
        'rules.title': '自定義過濾規則',
        'rules.desc': '根據您的育兒理念自定義內容過濾規則',

        'rules.language.title': '語言限制',
        'rules.language.enable': '啟用語言限制',
        'rules.language.allowed': '允許的語言',
        'rules.language.action': '違規處理',

        'rules.actions.title': '動作行為限制',
        'rules.actions.enable': '啟用動作限制',
        'rules.actions.add': '添加動作限制',

        'rules.audio.title': '聲音表現限制',
        'rules.audio.enable': '啟用聲音限制',
        'rules.audio.add': '添加聲音限制',

        'rules.visual.title': '視覺風格限制',
        'rules.visual.enable': '啟用視覺限制',

        'rules.themes.title': '主題內容限制',
        'rules.themes.enable': '啟用主題限制',

        'rules.keywords.title': '關鍵字黑名單',
        'rules.keywords.enable': '啟用關鍵字過濾',
        'rules.keywords.desc': '封鎖的關鍵字（每行一個）',

        // Notifications
        'notif.title': '通知設定',
        'notif.enable': '啟用通知功能',
        'notif.telegram.title': 'Telegram 通知',
        'notif.telegram.enable': '啟用 Telegram 通知',
        'notif.telegram.token': 'Bot Token',
        'notif.telegram.chatid': 'Chat ID',
        'notif.options.title': '通知選項',
        'notif.screenshot': '通知中包含截圖',
        'notif.blockonly': '僅在阻擋內容時通知',

        // Templates
        'template.title': '快速配置模板',
        'template.desc': '選擇預設模板快速開始，之後可以自行調整',
        'template.strict.title': '嚴格模式',
        'template.strict.desc': '適合 4-7 歲幼兒',
        'template.strict.feat1': '只允許中文',
        'template.strict.feat2': '禁止所有暴力動作',
        'template.strict.feat3': '禁止尖叫和大叫',
        'template.strict.feat4': '極嚴格的主題限制',

        'template.relaxed.title': '寬鬆模式',
        'template.relaxed.desc': '適合 10-12 歲兒童',
        'template.relaxed.feat1': '中英文都允許',
        'template.relaxed.feat2': '只限制極端暴力',
        'template.relaxed.feat3': '多數情況僅警告',
        'template.relaxed.feat4': '給予更多自由度',

        'template.default.title': '預設配置',
        'template.default.desc': '標準配置模板',
        'template.default.feat1': '平衡的保護設定',
        'template.default.feat2': '適合大多數家庭',
        'template.default.feat3': '可自行調整',

        'template.use': '使用此模板',

        // Actions
        'btn.save': '保存配置',
        'btn.validate': '驗證配置',
        'btn.preview': '預覽 YAML',
        'btn.copy': '複製到剪貼板',

        // Messages
        'msg.confirm.template': '確定要載入「{name}」模板嗎？目前的設定將被覆蓋。',
        'msg.success.save': '配置已成功保存！',
        'msg.success.copy': '已複製到剪貼板！',
        'msg.error.save': '保存失敗',
        'msg.api.success': 'API 連接成功！',
        'msg.api.error': 'API 測試失敗',
    },

    'en': {
        // Header
        'app.title': 'KidGuard Parent Control Panel',
        'app.subtitle': 'Protect your children from inappropriate content',

        // Status
        'status.ready': 'Ready',
        'status.loading': 'Loading...',
        'status.saving': 'Saving...',
        'status.saved': 'Saved',
        'status.error': 'Error',

        // Tabs
        'tab.basic': 'Basic Settings',
        'tab.family': 'Family Members',
        'tab.rules': 'Custom Rules',
        'tab.notifications': 'Notifications',
        'tab.templates': 'Quick Templates',

        // Basic Settings
        'basic.title': 'Basic Settings',
        'basic.claude.title': 'Claude API Configuration',
        'basic.claude.apikey': 'API Key',
        'basic.claude.model': 'Model Selection',
        'basic.claude.test': 'Test Connection',

        'basic.rules.title': 'Detection Rules',
        'basic.rules.age': 'Max Child Age',
        'basic.rules.action': 'When inappropriate content detected',
        'basic.rules.interval': 'Check Interval (seconds)',
        'basic.rules.threshold': 'Confidence Threshold',

        'basic.channels.title': 'Safe Channels Whitelist',
        'basic.channels.add': 'Add Safe Channel',

        // Action types
        'action.redirect': 'Redirect to safe channel',
        'action.skip': 'Skip video',
        'action.pause': 'Pause playback',
        'action.notify': 'Notify parents only',

        // Family
        'family.title': 'Family Member Management',
        'family.desc': 'Add family members to enable face recognition',
        'family.add': 'Add Family Member',
        'family.name': 'Name',
        'family.age': 'years old',
        'family.child': 'Child',
        'family.delete': 'Delete',

        // Custom Rules
        'rules.title': 'Custom Filtering Rules',
        'rules.desc': 'Customize content filtering based on your parenting philosophy',

        'rules.language.title': 'Language Restrictions',
        'rules.language.enable': 'Enable language restrictions',
        'rules.language.allowed': 'Allowed Languages',
        'rules.language.action': 'Violation Action',

        'rules.actions.title': 'Action/Behavior Restrictions',
        'rules.actions.enable': 'Enable action restrictions',
        'rules.actions.add': 'Add Action Restriction',

        'rules.audio.title': 'Audio/Sound Restrictions',
        'rules.audio.enable': 'Enable audio restrictions',
        'rules.audio.add': 'Add Audio Restriction',

        'rules.visual.title': 'Visual Style Restrictions',
        'rules.visual.enable': 'Enable visual restrictions',

        'rules.themes.title': 'Content Theme Restrictions',
        'rules.themes.enable': 'Enable theme restrictions',

        'rules.keywords.title': 'Keyword Blacklist',
        'rules.keywords.enable': 'Enable keyword filtering',
        'rules.keywords.desc': 'Blocked keywords (one per line)',

        // Notifications
        'notif.title': 'Notification Settings',
        'notif.enable': 'Enable notifications',
        'notif.telegram.title': 'Telegram Notifications',
        'notif.telegram.enable': 'Enable Telegram notifications',
        'notif.telegram.token': 'Bot Token',
        'notif.telegram.chatid': 'Chat ID',
        'notif.options.title': 'Notification Options',
        'notif.screenshot': 'Include screenshot in notification',
        'notif.blockonly': 'Notify only when blocking content',

        // Templates
        'template.title': 'Quick Configuration Templates',
        'template.desc': 'Choose a preset template to get started quickly, then customize as needed',
        'template.strict.title': 'Strict Mode',
        'template.strict.desc': 'For children aged 4-7',
        'template.strict.feat1': 'Chinese only',
        'template.strict.feat2': 'Block all violent actions',
        'template.strict.feat3': 'Block screaming and yelling',
        'template.strict.feat4': 'Very strict theme restrictions',

        'template.relaxed.title': 'Relaxed Mode',
        'template.relaxed.desc': 'For children aged 10-12',
        'template.relaxed.feat1': 'Chinese and English allowed',
        'template.relaxed.feat2': 'Only block extreme violence',
        'template.relaxed.feat3': 'Mostly warnings',
        'template.relaxed.feat4': 'More freedom',

        'template.default.title': 'Default Config',
        'template.default.desc': 'Standard configuration',
        'template.default.feat1': 'Balanced protection',
        'template.default.feat2': 'Suitable for most families',
        'template.default.feat3': 'Customizable',

        'template.use': 'Use This Template',

        // Actions
        'btn.save': 'Save Config',
        'btn.validate': 'Validate Config',
        'btn.preview': 'Preview YAML',
        'btn.copy': 'Copy to Clipboard',

        // Messages
        'msg.confirm.template': 'Load "{name}" template? Current settings will be overwritten.',
        'msg.success.save': 'Configuration saved successfully!',
        'msg.success.copy': 'Copied to clipboard!',
        'msg.error.save': 'Save failed',
        'msg.api.success': 'API connection successful!',
        'msg.api.error': 'API test failed',
    }
};

// Current language (default: English)
let currentLang = localStorage.getItem('kidguard-lang') || 'en';

// Get translation
function t(key) {
    return translations[currentLang][key] || key;
}

// Switch language
function switchLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('kidguard-lang', lang);
    updateUI();
}

// Update all UI text
function updateUI() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const text = t(key);

        if (el.tagName === 'INPUT' && el.type === 'text') {
            el.placeholder = text;
        } else {
            el.textContent = text;
        }
    });

    // Update language toggle button
    const langBtn = document.getElementById('langToggle');
    if (langBtn) {
        langBtn.textContent = currentLang === 'zh-TW' ? 'EN' : '中文';
    }
}

// Initialize i18n
document.addEventListener('DOMContentLoaded', () => {
    updateUI();
});
