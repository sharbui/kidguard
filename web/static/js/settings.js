// KidGuard Web UI - Settings Management

let currentConfig = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    loadConfig();
    setupEventListeners();
});

// Tab Management
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all tabs
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

            // Add active class to clicked tab
            btn.classList.add('active');
            const tabId = btn.dataset.tab;
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Event Listeners
function setupEventListeners() {
    // Confidence threshold slider
    const slider = document.getElementById('confidenceThreshold');
    if (slider) {
        slider.addEventListener('input', (e) => {
            document.getElementById('confidenceValue').textContent = e.target.value;
        });
    }
}

// Load Configuration
async function loadConfig() {
    try {
        showStatus('載入配置中...', 'loading');

        const response = await fetch('/api/config');
        const data = await response.json();

        if (data.success) {
            currentConfig = data.config;
            populateForm(currentConfig);
            showStatus(data.exists ? '配置已載入' : '使用預設配置', 'success');
        } else {
            showStatus('載入配置失敗: ' + data.error, 'error');
        }
    } catch (error) {
        showStatus('載入配置失敗: ' + error.message, 'error');
    }
}

// Populate Form with Config
function populateForm(config) {
    // Basic settings
    if (config.claude) {
        setValueById('apiKey', config.claude.api_key);
        setValueById('model', config.claude.model);
    }

    if (config.rules) {
        setValueById('maxChildAge', config.rules.max_child_age);
        setValueById('action', config.rules.action);
        setValueById('checkInterval', config.rules.check_interval);
    }

    if (config.analysis) {
        setValueById('confidenceThreshold', config.analysis.confidence_threshold);
        document.getElementById('confidenceValue').textContent = config.analysis.confidence_threshold;

        // Custom rules
        const customRules = config.analysis.custom_rules || {};

        // Language rules
        if (customRules.language) {
            setCheckedById('languageEnabled', customRules.language.enabled);
            setValueById('languageAction', customRules.language.action);

            const allowedLangs = customRules.language.allowed_languages || [];
            document.querySelectorAll('.allowed-language').forEach(cb => {
                cb.checked = allowedLangs.includes(cb.value);
            });
        }

        // Action rules
        if (customRules.actions) {
            setCheckedById('actionsEnabled', customRules.actions.enabled);
            populateBlockedActions(customRules.actions.blocked_actions || []);
        }

        // Audio rules
        if (customRules.audio) {
            setCheckedById('audioEnabled', customRules.audio.enabled);
            populateBlockedAudio(customRules.audio.blocked_audio_types || []);
        }

        // Visual rules
        if (customRules.visual) {
            setCheckedById('visualEnabled', customRules.visual.enabled);
            const blockedStyles = customRules.visual.blocked_styles || [];
            document.querySelectorAll('.blocked-visual').forEach(cb => {
                cb.checked = blockedStyles.some(s => s.type === cb.value);
            });
        }

        // Theme rules
        if (customRules.themes) {
            setCheckedById('themesEnabled', customRules.themes.enabled);
            const blockedThemes = customRules.themes.blocked_themes || [];
            document.querySelectorAll('.blocked-theme').forEach(cb => {
                cb.checked = blockedThemes.includes(cb.value);
            });
        }

        // Keyword rules
        if (customRules.keywords) {
            setCheckedById('keywordsEnabled', customRules.keywords.enabled);
            const keywords = customRules.keywords.blocked_keywords || [];
            setValueById('blockedKeywords', keywords.join('\n'));
        }
    }

    // Family members
    if (config.family) {
        populateFamilyMembers(config.family);
    }

    // Safe channels
    if (config.safe_channels) {
        populateSafeChannels(config.safe_channels);
    }

    // Notifications
    if (config.notifications) {
        setCheckedById('notificationsEnabled', config.notifications.enabled);
        setCheckedById('includeScreenshot', config.notifications.include_screenshot);
        setCheckedById('blockOnly', config.notifications.block_only);

        if (config.notifications.telegram) {
            setCheckedById('telegramEnabled', config.notifications.telegram.enabled);
            setValueById('telegramBotToken', config.notifications.telegram.bot_token);
            setValueById('telegramChatId', config.notifications.telegram.chat_id);
        }
    }
}

// Build Config from Form
function buildConfigFromForm() {
    const config = {
        claude: {
            api_key: getValueById('apiKey'),
            model: getValueById('model')
        },
        family: getFamilyMembers(),
        rules: {
            max_child_age: parseInt(getValueById('maxChildAge')),
            action: getValueById('action'),
            check_interval: parseInt(getValueById('checkInterval')),
            clip_duration: 5
        },
        safe_channels: getSafeChannels(),
        analysis: {
            block_categories: ['violence', 'horror', 'adult', 'drugs', 'gambling'],
            warn_categories: ['excessive_consumerism', 'clickbait', 'loud_content'],
            confidence_threshold: parseFloat(getValueById('confidenceThreshold')),
            custom_rules: {
                language: {
                    enabled: getCheckedById('languageEnabled'),
                    allowed_languages: getCheckedValues('.allowed-language'),
                    action: getValueById('languageAction'),
                    reason: '非家長允許的語言內容'
                },
                actions: {
                    enabled: getCheckedById('actionsEnabled'),
                    blocked_actions: getBlockedActions(),
                    action: 'block'
                },
                audio: {
                    enabled: getCheckedById('audioEnabled'),
                    blocked_audio_types: getBlockedAudio(),
                    action: 'block'
                },
                visual: {
                    enabled: getCheckedById('visualEnabled'),
                    blocked_styles: getBlockedVisuals(),
                    action: 'block'
                },
                themes: {
                    enabled: getCheckedById('themesEnabled'),
                    blocked_themes: getCheckedValues('.blocked-theme'),
                    action: 'block'
                },
                keywords: {
                    enabled: getCheckedById('keywordsEnabled'),
                    blocked_keywords: getValueById('blockedKeywords').split('\n').filter(k => k.trim()),
                    action: 'block'
                }
            }
        },
        notifications: {
            enabled: getCheckedById('notificationsEnabled'),
            telegram: {
                enabled: getCheckedById('telegramEnabled'),
                bot_token: getValueById('telegramBotToken'),
                chat_id: getValueById('telegramChatId')
            },
            include_screenshot: getCheckedById('includeScreenshot'),
            block_only: getCheckedById('blockOnly')
        },
        privacy: {
            delete_clips: true,
            anonymize_logs: false,
            local_only: true
        },
        logging: {
            level: 'INFO',
            file: 'logs/kidguard.log',
            max_size_mb: 10,
            backup_count: 5
        }
    };

    return config;
}

// Save Configuration
async function saveConfig() {
    try {
        showStatus('保存配置中...', 'loading');

        const config = buildConfigFromForm();

        const response = await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const data = await response.json();

        if (data.success) {
            showStatus('✓ 配置已成功保存！', 'success');
            currentConfig = config;
        } else {
            showStatus('✗ 保存失敗: ' + data.error, 'error');
        }
    } catch (error) {
        showStatus('✗ 保存失敗: ' + error.message, 'error');
    }
}

// Validate Configuration
async function validateConfig() {
    try {
        showStatus('驗證配置中...', 'loading');

        const config = buildConfigFromForm();

        const response = await fetch('/api/config/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const data = await response.json();

        if (data.success) {
            if (data.valid) {
                let message = '✓ 配置驗證通過！';
                if (data.warnings.length > 0) {
                    message += '\n\n警告:\n' + data.warnings.map(w => '⚠ ' + w).join('\n');
                }
                alert(message);
                showStatus('配置驗證通過', 'success');
            } else {
                let message = '✗ 配置驗證失敗:\n\n';
                message += data.errors.map(e => '✗ ' + e).join('\n');
                if (data.warnings.length > 0) {
                    message += '\n\n警告:\n' + data.warnings.map(w => '⚠ ' + w).join('\n');
                }
                alert(message);
                showStatus('配置驗證失敗', 'error');
            }
        }
    } catch (error) {
        showStatus('驗證失敗: ' + error.message, 'error');
    }
}

// Preview Configuration as YAML
function previewConfig() {
    const config = buildConfigFromForm();
    const yaml = formatYAML(config);

    document.getElementById('previewYaml').textContent = yaml;
    document.getElementById('previewModal').classList.add('active');
}

// Format object as YAML
function formatYAML(obj, indent = 0) {
    let yaml = '';
    const spaces = '  '.repeat(indent);

    for (const [key, value] of Object.entries(obj)) {
        if (value === null || value === undefined) continue;

        if (typeof value === 'object' && !Array.isArray(value)) {
            yaml += `${spaces}${key}:\n`;
            yaml += formatYAML(value, indent + 1);
        } else if (Array.isArray(value)) {
            yaml += `${spaces}${key}:\n`;
            value.forEach(item => {
                if (typeof item === 'object') {
                    yaml += `${spaces}  -\n`;
                    yaml += formatYAML(item, indent + 2);
                } else {
                    yaml += `${spaces}  - ${item}\n`;
                }
            });
        } else {
            yaml += `${spaces}${key}: ${typeof value === 'string' ? `"${value}"` : value}\n`;
        }
    }

    return yaml;
}

// Load Template
async function loadTemplate(templateName) {
    if (!confirm(`確定要載入「${templateName}」模板嗎？目前的設定將被覆蓋。`)) {
        return;
    }

    try {
        showStatus('載入模板中...', 'loading');

        const response = await fetch('/api/config/templates');
        const data = await response.json();

        if (data.success && data.templates[templateName]) {
            currentConfig = data.templates[templateName];
            populateForm(currentConfig);
            showStatus('✓ 模板已載入', 'success');

            // Switch to basic tab
            document.querySelector('[data-tab="basic"]').click();
        } else {
            showStatus('✗ 模板不存在', 'error');
        }
    } catch (error) {
        showStatus('✗ 載入模板失敗: ' + error.message, 'error');
    }
}

// Test Claude API
async function testClaudeAPI() {
    const apiKey = getValueById('apiKey');

    if (!apiKey) {
        alert('請先輸入 API Key');
        return;
    }

    try {
        showStatus('測試 API 連接中...', 'loading');

        const response = await fetch('/api/test/claude', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey })
        });

        const data = await response.json();

        if (data.success) {
            alert('✓ API 連接成功！\n\n' + data.response);
            showStatus('API 測試成功', 'success');
        } else {
            alert('✗ API 測試失敗:\n\n' + data.error);
            showStatus('API 測試失敗', 'error');
        }
    } catch (error) {
        alert('✗ API 測試失敗:\n\n' + error.message);
        showStatus('API 測試失敗', 'error');
    }
}

// Family Members Management
function populateFamilyMembers(members) {
    const list = document.getElementById('familyMembersList');
    list.innerHTML = '';

    members.forEach((member, index) => {
        const item = document.createElement('div');
        item.className = 'list-item';
        item.innerHTML = `
            <div class="list-item-content">
                <strong>${member.name}</strong> - ${member.age} 歲
                ${member.is_child ? '<span style="color: var(--primary-color);">👶 兒童</span>' : ''}
            </div>
            <div class="list-item-actions">
                <button class="btn-remove" onclick="removeFamilyMember(${index})">刪除</button>
            </div>
        `;
        list.appendChild(item);
    });
}

function addFamilyMember() {
    const name = prompt('請輸入姓名:');
    if (!name) return;

    const age = parseInt(prompt('請輸入年齡:'));
    if (!age || age < 1) return;

    const isChild = confirm('這是兒童嗎？（需要保護）');

    if (!currentConfig.family) currentConfig.family = [];

    currentConfig.family.push({
        name,
        age,
        is_child: isChild
    });

    populateFamilyMembers(currentConfig.family);
}

function removeFamilyMember(index) {
    if (confirm('確定要刪除此家庭成員嗎？')) {
        currentConfig.family.splice(index, 1);
        populateFamilyMembers(currentConfig.family);
    }
}

function getFamilyMembers() {
    return currentConfig.family || [];
}

// Safe Channels Management
function populateSafeChannels(channels) {
    const list = document.getElementById('safeChannelsList');
    list.innerHTML = '';

    channels.forEach((channel, index) => {
        const item = document.createElement('div');
        item.className = 'list-item';
        item.innerHTML = `
            <div class="list-item-content">
                <strong>${channel.name}</strong><br>
                <small style="color: var(--text-light);">ID: ${channel.id}</small>
            </div>
            <div class="list-item-actions">
                <button class="btn-remove" onclick="removeSafeChannel(${index})">刪除</button>
            </div>
        `;
        list.appendChild(item);
    });
}

function addSafeChannel() {
    const id = prompt('請輸入 YouTube 頻道 ID:');
    if (!id) return;

    const name = prompt('請輸入頻道名稱:');
    if (!name) return;

    if (!currentConfig.safe_channels) currentConfig.safe_channels = [];

    currentConfig.safe_channels.push({ id, name });
    populateSafeChannels(currentConfig.safe_channels);
}

function removeSafeChannel(index) {
    if (confirm('確定要刪除此安全頻道嗎？')) {
        currentConfig.safe_channels.splice(index, 1);
        populateSafeChannels(currentConfig.safe_channels);
    }
}

function getSafeChannels() {
    return currentConfig.safe_channels || [];
}

// Blocked Actions Management
function populateBlockedActions(actions) {
    const list = document.getElementById('blockedActionsList');
    list.innerHTML = '';

    actions.forEach((action, index) => {
        const item = document.createElement('div');
        item.className = 'list-item';
        item.innerHTML = `
            <div class="list-item-content">
                <strong>${action.type}</strong> - ${action.description}<br>
                <small style="color: var(--text-light);">關鍵字: ${action.keywords.join(', ')}</small>
            </div>
            <div class="list-item-actions">
                <button class="btn-remove" onclick="removeBlockedAction(${index})">刪除</button>
            </div>
        `;
        list.appendChild(item);
    });
}

function addBlockedAction() {
    const type = prompt('動作類型（例如：砍擊揮砍）:');
    if (!type) return;

    const description = prompt('詳細描述:');
    if (!description) return;

    const keywords = prompt('關鍵字（用逗號分隔）:');
    if (!keywords) return;

    const action = {
        type,
        description,
        keywords: keywords.split(',').map(k => k.trim()),
        severity: 'high'
    };

    if (!currentConfig.analysis) currentConfig.analysis = {};
    if (!currentConfig.analysis.custom_rules) currentConfig.analysis.custom_rules = {};
    if (!currentConfig.analysis.custom_rules.actions) currentConfig.analysis.custom_rules.actions = { enabled: true, blocked_actions: [] };

    currentConfig.analysis.custom_rules.actions.blocked_actions.push(action);
    populateBlockedActions(currentConfig.analysis.custom_rules.actions.blocked_actions);
}

function removeBlockedAction(index) {
    if (confirm('確定要刪除此動作限制嗎？')) {
        currentConfig.analysis.custom_rules.actions.blocked_actions.splice(index, 1);
        populateBlockedActions(currentConfig.analysis.custom_rules.actions.blocked_actions);
    }
}

function getBlockedActions() {
    if (!currentConfig.analysis?.custom_rules?.actions?.blocked_actions) return [];
    return currentConfig.analysis.custom_rules.actions.blocked_actions;
}

// Similar functions for audio
function populateBlockedAudio(audioTypes) {
    const list = document.getElementById('blockedAudioList');
    list.innerHTML = '';

    audioTypes.forEach((audio, index) => {
        const item = document.createElement('div');
        item.className = 'list-item';
        item.innerHTML = `
            <div class="list-item-content">
                <strong>${audio.type}</strong> - ${audio.description}<br>
                <small style="color: var(--text-light);">關鍵字: ${audio.keywords.join(', ')}</small>
            </div>
            <div class="list-item-actions">
                <button class="btn-remove" onclick="removeBlockedAudio(${index})">刪除</button>
            </div>
        `;
        list.appendChild(item);
    });
}

function addBlockedAudio() {
    const type = prompt('聲音類型（例如：尖叫）:');
    if (!type) return;

    const description = prompt('詳細描述:');
    if (!description) return;

    const keywords = prompt('關鍵字（用逗號分隔）:');
    if (!keywords) return;

    const audio = {
        type,
        description,
        keywords: keywords.split(',').map(k => k.trim()),
        severity: 'high'
    };

    if (!currentConfig.analysis) currentConfig.analysis = {};
    if (!currentConfig.analysis.custom_rules) currentConfig.analysis.custom_rules = {};
    if (!currentConfig.analysis.custom_rules.audio) currentConfig.analysis.custom_rules.audio = { enabled: true, blocked_audio_types: [] };

    currentConfig.analysis.custom_rules.audio.blocked_audio_types.push(audio);
    populateBlockedAudio(currentConfig.analysis.custom_rules.audio.blocked_audio_types);
}

function removeBlockedAudio(index) {
    if (confirm('確定要刪除此聲音限制嗎？')) {
        currentConfig.analysis.custom_rules.audio.blocked_audio_types.splice(index, 1);
        populateBlockedAudio(currentConfig.analysis.custom_rules.audio.blocked_audio_types);
    }
}

function getBlockedAudio() {
    if (!currentConfig.analysis?.custom_rules?.audio?.blocked_audio_types) return [];
    return currentConfig.analysis.custom_rules.audio.blocked_audio_types;
}

function getBlockedVisuals() {
    const checked = getCheckedValues('.blocked-visual');
    return checked.map(type => ({ type, severity: 'high' }));
}

// Utility Functions
function getValueById(id) {
    const el = document.getElementById(id);
    return el ? el.value : '';
}

function setValueById(id, value) {
    const el = document.getElementById(id);
    if (el) el.value = value || '';
}

function getCheckedById(id) {
    const el = document.getElementById(id);
    return el ? el.checked : false;
}

function setCheckedById(id, checked) {
    const el = document.getElementById(id);
    if (el) el.checked = !!checked;
}

function getCheckedValues(selector) {
    return Array.from(document.querySelectorAll(selector))
        .filter(cb => cb.checked)
        .map(cb => cb.value);
}

function showStatus(message, type) {
    const statusBar = document.getElementById('statusBar');
    const statusText = document.getElementById('statusText');

    statusText.textContent = message;

    // Reset classes
    statusBar.className = 'status-bar';

    // Add type class
    if (type === 'error') statusBar.classList.add('alert-error');
    else if (type === 'success') statusBar.classList.add('alert-success');
    else if (type === 'warning') statusBar.classList.add('alert-warning');
}

function toggleSection(header) {
    const section = header.parentElement;
    section.classList.toggle('collapsed');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function copyToClipboard() {
    const text = document.getElementById('previewYaml').textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert('已複製到剪貼板！');
    });
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
}
