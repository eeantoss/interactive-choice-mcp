# 修复并发调用和前端体验问题

## 日期
2026-01-26

## 问题描述
1. **并发调用问题**：A调用后B调用不了，出现 `timeout_cancelled`
2. **前端体验问题**：输入限制太多，滚动条太短，输入框高度联动
3. **新增需求**：桌面弹窗模式

## 解决方案

### 方案1：增强会话隔离和错误恢复
- 优化 `_cleanup_loop` 只清理已完成的会话，不影响活跃会话
- 在 `create_session` 中添加会话ID冲突检测
- 在 `safe_handle` 中增加重试逻辑（最多2次重试）
- 优化 WebSocket 连接管理，连接问题不影响会话状态
- **跨进程会话支持**：添加 `/api/session` API端点，允许外部进程创建会话

### 方案A：优化现有布局
- 将 `option-note` 从固定宽度改为弹性宽度 (flex: 1 1 120px)
- 调整 `.config-content` 的高度和滚动条样式
- 移除固定高度和overflow限制，拉伸备注时整个页面跟着扩展

### 桌面弹窗模式（PyWebView）
- 添加 `pywebview` 依赖
- 创建 `src/desktop/` 模块
- 支持在配置中选择"桌面弹窗"模式
- 使用原生窗口显示Web界面

## 修改的文件
1. `src/web/frontend/styles/layout.css` - 滚动条和侧边栏高度
2. `src/web/frontend/styles/components.css` - 输入框样式
3. `src/web/frontend/styles/base.css` - prompt容器样式
4. `src/web/server.py` - 会话清理、创建逻辑、跨进程支持
5. `src/web/session.py` - 会话过期判断和广播方法
6. `src/core/orchestrator.py` - 错误处理、重试逻辑、桌面模式支持
7. `src/core/models.py` - 添加 TRANSPORT_DESKTOP 常量
8. `src/desktop/__init__.py` - 桌面模块入口
9. `src/desktop/window.py` - PyWebView窗口实现
10. `src/web/templates.py` - 添加桌面选项
11. `src/infra/i18n.py` - 添加桌面模式国际化文本
12. `pyproject.toml` - 添加 pywebview 依赖

## 测试结果
- 104个单元测试全部通过
