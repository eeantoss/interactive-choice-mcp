"""Internationalization resource module.

Provides centralized text resources for all kinds of languages.
Both terminal and web transports share these resources for consistent text.
"""

from __future__ import annotations

from typing import Dict

__all__ = ["get_text", "TEXTS"]

# Section: Text Resources
# Keys are organized by UI context (settings, actions, labels, messages).
# Each key maps to a dict with abbreviation entries.

TEXTS: Dict[str, Dict[str, str]] = {
    # Section: Settings Panel
    "settings.title": {
        "en": "Settings",
        "zh": "设置",
    },
    "settings.language": {
        "en": "Language",
        "zh": "语言",
    },
    "settings.language_en": {
        "en": "English",
        "zh": "英文",
    },
    "settings.language_zh": {
        "en": "Chinese",
        "zh": "中文",
    },
    "settings.interface": {
        "en": "Interaction Interface",
        "zh": "交互界面",
    },
    "settings.transport_terminal": {
        "en": "Terminal(experimental)",
        "zh": "终端(实验性)",
    },
    "settings.transport_web": {
        "en": "Web",
        "zh": "Web 浏览器",
    },
    "settings.transport_desktop": {
        "en": "Desktop Window",
        "zh": "桌面弹窗",
    },
    "settings.timeout": {
        "en": "Timeout (seconds)",
        "zh": "超时时间 (秒)",
    },
    "settings.single_submit": {
        "en": "Single Selection Auto Submit",
        "zh": "单选自动提交",
    },
    "settings.adopt_recommended_options": {
        "en": "Adopt Recommended Options",
        "zh": "采用推荐选项",
    },
    "settings.save": {
        "en": "Save",
        "zh": "保存",
    },
    "settings.cancel": {
        "en": "Cancel",
        "zh": "取消",
    },
    "settings.saved": {
        "en": "Settings saved",
        "zh": "设置已保存",
    },
    "settings.notifications": {
        "en": "Notifications",
        "zh": "通知设置",
    },
    "settings.notify_new": {
        "en": "New interaction",
        "zh": "新交互进程通知",
    },
    "settings.notify_upcoming": {
        "en": "Upcoming timeout",
        "zh": "即将超时通知",
    },
    "settings.upcoming_threshold": {
        "en": "Threshold (s)",
        "zh": "剩余时间 (秒)",
    },
    "settings.notify_timeout": {
        "en": "Timeout reached",
        "zh": "超时通知",
    },
    "settings.notify_conditions": {
        "en": "Trigger Conditions",
        "zh": "通知触发条件",
    },
    "settings.notify_trigger_mode": {
        "en": "Trigger Mode",
        "zh": "触发模式",
    },
    "settings.trigger_always": {
        "en": "Always",
        "zh": "总是通知",
    },
    "settings.trigger_background": {
        "en": "Browser lost focus",
        "zh": "浏览器失去焦点时",
    },
    "settings.trigger_tab_switch": {
        "en": "Only interaction page lost focus",
        "zh": "仅交互页面失去焦点时",
    },
    "settings.trigger_focus_lost": {
        "en": "Interaction page and browser lost focus",
        "zh": "交互页面和浏览器失去焦点时",
    },
    "desc.notify_trigger_mode": {
        "en": "When to show notifications based on window focus state.",
        "zh": "根据窗口焦点状态决定何时显示通知。",
    },
    "settings.notify_sound": {
        "en": "Notification sound",
        "zh": "通知音效",
    },
    "settings.test_sound": {
        "en": "Test",
        "zh": "测试",
    },

    # Section: Actions
    "action.submit": {
        "en": "Submit",
        "zh": "提交",
    },
    "action.submit_auto_single": {
        "en": "Auto-submit after selecting option",
        "zh": "选中选项后自动提交",
    },
    "action.cancel": {
        "en": "Cancel",
        "zh": "取消",
    },
    "action.cancel_with_annotations": {
        "en": "Cancel with annotations",
        "zh": "带备注取消",
    },
    "action.confirm": {
        "en": "Confirm",
        "zh": "确认",
    },
    "action.back": {
        "en": "Back",
        "zh": "返回",
    },
    "action.select_all": {
        "en": "Select All",
        "zh": "全选",
    },
    "action.deselect_all": {
        "en": "Deselect All",
        "zh": "取消全选",
    },

    # Section: Labels
    "label.options": {
        "en": "Options",
        "zh": "选项",
    },
    "label.selected": {
        "en": "Selected",
        "zh": "已选择",
    },
    "label.recommended": {
        "en": "AI Recommended",
        "zh": "由 AI 推荐",
    },
    "label.annotation": {
        "en": "Annotation",
        "zh": "备注",
    },
    "label.timeout_remaining": {
        "en": "Time Remaining",
        "zh": "剩余时间",
    },
    "label.started_at": {
        "en": "Started",
        "zh": "开始时间",
    },

    # Section: Status
    "status.pending": {
        "en": "Pending",
        "zh": "等待中",
    },
    "status.submitted": {
        "en": "Submitted",
        "zh": "已提交",
    },
    "status.auto_submitted": {
        "en": "Auto Submitted",
        "zh": "自动提交",
    },
    "status.cancelled": {
        "en": "Cancelled",
        "zh": "已取消",
    },
    "status.timeout": {
        "en": "Timeout",
        "zh": "已超时",
    },
    "status.error": {
        "en": "Error",
        "zh": "错误",
    },
    "status.offline": {
        "en": "Offline",
        "zh": "离线",
    },

    # Section: Status Messages
    "status_message.manual": {
        "en": "✅ Submitted successfully",
        "zh": "✅ 提交成功",
    },
    "status_message.timeout_auto_submitted": {
        "en": "⏰ Timeout: Auto-submitted.",
        "zh": "⏰ 超时：已自动提交。",
    },
    "status_message.timeout_cancelled": {
        "en": "⏰ Timeout: Cancelled.",
        "zh": "⏰ 超时：已取消。",
    },
    "status_message.timeout_reinvoke_requested": {
        "en": "⏰ Timeout: Re-invocation requested.",
        "zh": "⏰ 超时：请求重新调用。",
    },
    "status_message.cancelled": {
        "en": "🚫 Cancelled.",
        "zh": "🚫 已取消。",
    },
    "status_message.cancel_with_annotation": {
        "en": "🚫 Cancelled with annotations",
        "zh": "🚫 带备注取消",
    },
    "status_message.server_error": {
        "en": "Server error",
        "zh": "服务器错误",
    },
    "status_message.sever_offline": {
        "en": "Unable to reach MCP server, please try again",
        "zh": "无法连接到 MCP 服务器，请重试",
    },
    "status_message.interrupted": {
        "en": "⚠️ Session interrupted: Connection lost unexpectedly",
        "zh": "⚠️ 进程意外中断：连接已丢失",
    },

    # Section: Interaction List
    "list.title": {
        "en": "Interactions",
        "zh": "交互列表",
    },
    "list.all": {
        "en": "All",
        "zh": "全部",
    },
    "list.active": {
        "en": "Active",
        "zh": "进行中",
    },
    "list.completed": {
        "en": "Completed",
        "zh": "已完成",
    },
    "list.no_interactions": {
        "en": "No interactions",
        "zh": "暂无交互",
    },
    "list.loading": {
        "en": "Loading interactions...",
        "zh": "加载交互列表...",
    },

    # Section: Terminal UI
    "terminal.settings_entry": {
        "en": "⚙ Settings",
        "zh": "⚙ 设置",
    },
    "terminal.cancel_entry": {
        "en": "✕ Cancel",
        "zh": "✕ 取消",
    },
    "terminal.switch_to_web": {
        "en": "Switch to Web",
        "zh": "切换到 Web",
    },
    "terminal.navigation_hint": {
        "en": "Use ↑/↓ or j/k to navigate, Enter to select",
        "zh": "使用 ↑/↓ 或 j/k 导航，Enter 选择",
    },
    "terminal.annotation_prompt": {
        "en": "Add annotation (optional):",
        "zh": "添加备注 (可选)：",
    },
    "terminal.additional_annotation": {
        "en": "Additional annotation (optional):",
        "zh": "额外备注（可选）：",
    },

    # Section: Web Portal Settings
    "web.portal_settings": {
        "en": "Web Portal Settings",
        "zh": "Web Portal 设置",
    },
    "web.global_settings": {
        "en": "Global Settings",
        "zh": "全局设置",
    },
    "web.configuration": {
        "en": "Configuration",
        "zh": "配置",
    },
    "web.theme": {
        "en": "Theme",
        "zh": "主题",
    },
    "web.theme_light": {
        "en": "Light",
        "zh": "浅色",
    },
    "web.theme_dark": {
        "en": "Dark",
        "zh": "深色",
    },
    "web.theme_system": {
        "en": "System",
        "zh": "跟随系统",
    },

    # Section: Web Descriptions
    "desc.language": {
        "en": "Switch interface language",
        "zh": "切换界面语言",
    },
    "desc.theme": {
        "en": "Switch between light, dark, or system theme",
        "zh": "切换浅色、深色或跟随系统主题",
    },
    "desc.single_submit": {
        "en": "Automatically submit when an option is clicked",
        "zh": "选中选项后自动提交",
    },
    "desc.adpot_recommended_options": {
        "en": "Auto-select AI recommended options",
        "zh": "自动选择 AI 推荐的选项",
    },
    "desc.interface": {
        "en": "Interfaces for interactions",
        "zh": "交互界面选择",
    },
    "desc.timeout": {
        "en": "Time limit for making a choice. If no selection is made and 'Adopt Recommended Options' is enabled, recommended options will be submitted.",
        "zh": "选择的时间限制。若无选择且启用'采用推荐选项'，将提交推荐选项。",
    },

    # Section: Keyboard Hints
    "hint.navigate": {
        "en": "Navigate",
        "zh": "浏览选项",
    },
    "hint.select": {
        "en": "Select",
        "zh": "选择",
    },
    "hint.submit": {
        "en": "Submit",
        "zh": "提交",
    },
    "hint.cancel": {
        "en": "Unfocus Text Area",
        "zh": "取消文本框聚焦",
    },
    "hint.toggle_config": {
        "en": "Toggle Config",
        "zh": "展开/收起配置",
    },
    "hint.annotation": {
        "en": "Annotation",
        "zh": "备注",
    },
    "hint.placeholder": {
        "en": "Keyboard hints: ↑↓ / kj Navigate | Enter Select | Ctrl+Enter Submit | Shift+A Focus on Option Annotation | Esc Unfocus Text Area",
        "zh": "按键提示: ↑↓ / kj 浏览 | Enter 选择 | Ctrl+Enter 提交 | Shift+A 聚焦到选项备注 | Esc 取消文本框聚焦",
    },
    "hint.additional_annotation": {
        "en": "Add additional annotation here",
        "zh": "此处可添加额外备注",
    },

    # Section: Settings Additional
    "settings.timeout_action": {
        "en": "Timeout Action",
        "zh": "超时行为",
    },
    "settings.timeout_action_submit": {
        "en": "Auto-submit selected",
        "zh": "自动提交已选",
    },
    "settings.timeout_action_cancel": {
        "en": "Auto-cancel",
        "zh": "自动取消",
    },
    "settings.timeout_action_reinvoke": {
        "en": "Request re-invocation",
        "zh": "请求重新调用",
    },
    "desc.timeout_action": {
        "en": "Action to take when the timeout is reached",
        "zh": "超时后执行的操作",
    },

    # Section: Status Bar Labels
    "status.completed": {
        "en": "Completed",
        "zh": "已完成",
    },
    "label.status": {
        "en": "Session Status",
        "zh": "进程状态",
    },
    "status.connected": {
        "en": "In Progress",
        "zh": "进行中",
    },
    "status.interrupted": {
        "en": "Interrupted",
        "zh": "意外中断",
    },
    "status.connecting": {
        "en": "Connecting...",
        "zh": "连接中",
    },

    # Section: Notifications
    "notification.session.title": {
        "en": "Interactive Choice - New Session - {prompt_title}",
        "zh": "Interactive Choice - 新交互 - {prompt_title}",
    },
    "notification.session.ready": {
        "en": "Ready",
        "zh": "就绪",
    },
    "notification.timeout.upcomingTitle": {
        "en": "Timeout Approaching - {prompt_title}",
        "zh": "即将超时 - {prompt_title}",
    },
    "notification.timeout.upcomingBody": {
        "en": "Timeout in {seconds} seconds",
        "zh": "剩余 {seconds} 秒超时",
    },
    "notification.timeout.submittedTitle": {
        "en": "Auto Submitted - {prompt_title}",
        "zh": "已自动提交 - {prompt_title}",
    },
    "notification.timeout.submittedBody": {
        "en": "Your selection was automatically submitted due to timeout",
        "zh": "因超时已自动提交您的选择",
    },
    "notification.timeout.cancelledTitle": {
        "en": "Timeout Cancelled - {prompt_title}",
        "zh": "超时已取消 - {prompt_title}",
    },
    "notification.timeout.cancelledBody": {
        "en": "The interaction was cancelled due to timeout",
        "zh": "因超时交互已取消",
    },
    "notification.timeout.reachedTitle": {
        "en": "Timeout Reached - {prompt_title}",
        "zh": "已超时 - {prompt_title}",
    },
    "notification.timeout.reachedBody": {
        "en": "The interaction has timed out",
        "zh": "交互已超时",
    },
}


def get_text(key: str, lang: str = "en") -> str:
    """Get localized text for the given key.

    Args:
        key: The text resource key (e.g., 'settings.title').
        lang: The language code ('en' or 'zh'). Defaults to 'en'.

    Returns:
        The localized text, or the key itself if not found (for debugging).
    """
    entry = TEXTS.get(key)
    if entry is None:
        # Return key as fallback for debugging missing translations
        return key
    # Fallback to English if requested language is not available
    return entry.get(lang, entry.get("en", key))
