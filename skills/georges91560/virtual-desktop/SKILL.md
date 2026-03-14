---
name: virtual-desktop
description: 该工具为任何 OpenClaw 代理程序提供一个在 Docker 容器中运行的持久化、无头浏览器。它具备完全的自主执行能力：可以在任何平台上浏览任何网站、点击链接、输入内容、填写表单、提取数据、上传文件、提交信息以及截图——适用于各种任务。该代理程序能够分析任务需求、制定执行计划，并在内容创作、电子邮件管理、社交媒体发布、销售流程、市场研究、行政工作流程等多个领域实现自我优化。它使用的是 Playwright Chromium 技术，无需依赖 Xvfb 或 VNC，也不依赖于主机系统。用户会话信息会在每次运行过程中持续保存；所有操作都会被记录下来，这些记录通过 `.learnings/` 文件库帮助提升未来的执行效率。
version: 1.0.0
author: Georges Andronescu (Wesley Armando)
license: MIT
metadata:
  openclaw:
    emoji: "🖥️"
    security_level: L3
    always: false
    required_paths:
      read:
        - /workspace/TOOLS.md
        - /workspace/USER.md
        - /workspace/.learnings/LEARNINGS.md
        - /workspace/credentials/sessions/
      write:
        - /workspace/AUDIT.md
        - /workspace/screenshots/
        - /workspace/logs/browser/
        - /workspace/credentials/sessions/
        - /workspace/.learnings/ERRORS.md
        - /workspace/.learnings/LEARNINGS.md
        - /workspace/tasks/lessons.md
        - /workspace/memory/YYYY-MM-DD.md
    network_behavior:
      makes_requests: true
      request_targets:
        - https://*.* (Playwright headless Chromium — operator-authorized platforms only, list configured by principal at runtime)
      uses_agent_telegram: true
      telegram_usage: "Sends action confirmation and screenshots to principal via existing agent Telegram channel — no separate bot required"
    requires:
      env:
        - PLATFORM_EMAIL
        - PLATFORM_PASSWORD
      bins:
        - python3
        - playwright
    env_notes: >
      PLATFORM_EMAIL and PLATFORM_PASSWORD are generic placeholders.
      The operator sets platform-specific env vars (e.g. GOOGLE_EMAIL,
      BINANCE_EMAIL) and passes the var names as arguments to browser_control.py
      login command. The skill never reads env vars autonomously — only when
      explicitly called with named var arguments. Stored session files contain
      auth tokens scoped to the operator's own accounts only.
    primaryEnv: PLATFORM_EMAIL
---
# 虚拟桌面 — 通用执行层

## 该技能的功能

该技能为代理提供了一个在 Docker 容器中运行的持久化、无头浏览器（Playwright Chromium）。无需使用 Xvfb 或 VNC，也不依赖于主机系统。

| 功能        | 含义                                      |
|-------------|-----------------------------------------|
| **分析**      | 读取任何页面内容，提取结构化数据，监控页面变化                   |
| **规划**      | 绘制用户界面图谱，识别可操作元素（选择器），准备多步骤操作序列         |
| **执行**      | 点击、输入文本、填写表单、提交数据、上传文件、下载文件、浏览页面           |
| **自我修复**     | 在出现错误时截取屏幕截图，识别根本原因，并尝试其他方法重新执行         |
| **学习与优化**    | 在每次操作后，将用户界面模式和选择器信息保存到 `.learnings/` 文件中         |

**应用场景**：Google Workspace、社交平台、管理仪表盘、电子商务网站、表单填写、市场调研、数据提取等——任何没有提供 API 的平台。

---

## 所需的工作区结构

（相关文件结构在此处省略，具体文件内容请参考实际工作区配置。）

---

## 一次性设置

（相关配置代码在此处省略，具体配置内容请参考实际工作区设置。）

---

## 命令行接口（CLI）示例

```bash
# 检查虚拟桌面状态
python3 /workspace/skills/virtual-desktop/browser_control.py status

# 截取指定 URL 的屏幕截图
python3 browser_control.py screenshot https://example.com my_label

# 导航到指定页面并提取文本（可指定页面范围或通过选择器）
python3 browser_control.py navigate https://example.com ".article-title"

# 点击指定按钮
python3 browser_control.py click https://example.com "#submit-btn" platform_name

# 填写表单字段
python3 browser_control.py fill https://example.com "#email" "value@example.com" platform_name

# 登录并保存会话（从 `.env` 文件中读取凭据）
python3 browser_control.py login https://app.com/login EMAIL_ENV PASS_ENV "dashboard" platform_name

# 上传文件
python3 browser_control.py upload https://app.com/upload "input[type='file']" /workspace/file.pdf platform_name

# 从 JSON 文件中运行多步骤操作流程
python3 browser_control.py workflow /workspace/tasks/my_workflow.json platform_name

# 检查虚拟桌面状态
python3 browser_control.py status
```

---

## 规则与限制

- 在执行任何操作之前，必须确保代理具有相应的权限。
- `browser_control.py` 会在操作前后自动将日志记录到 `AUDIT.md` 文件中。
- 每次操作后都会自动截取屏幕截图。
- 经过身份验证的操作会自动保存会话信息。
- 禁止访问代理未明确授权的平台。
- 禁止使用未经验证或伪造的数据提交表单。
- 禁止在未经逐次操作批准的情况下执行支付操作。
- 禁止在屏幕截图、日志或 Telegram 消息中泄露凭据。
- 禁止在未得到确认的情况下重复执行可能造成破坏的操作。

---

## 异常处理规则

- 如果页面加载超时，`browser_control.py` 会自动将异常信息记录到 `ERRORS.md` 文件中，并在 `/workspace/logs/browser/YYYY-MM-DD.log` 文件中记录详细的错误追踪信息。
- 如果会话过期，系统会删除过期的会话文件并重新登录以获取新的会话。
- 如果找不到目标元素（选择器发生变化），系统会自动保存截图，并在 `.learnings/LEARNINGS.md` 文件中更新相关选择器的信息。
- 为防止被云flare 或其他反爬虫系统识别，`browser_control.py` 会设置真实的用户代理和区域设置；如果仍然被阻止，则需要在 `.env` 文件中配置代理地址。
- 在遇到未处理的异常时，系统会将完整的错误追踪信息记录到 `/workspace/logs/browser/YYYY-MM-DD.log` 文件中，并通知相关负责人。

---

## 学习与优化机制

- 每次操作后，系统会将用户界面模式和选择器信息保存到 `.learnings/` 文件中，以便后续使用。
- 系统会记录操作过程中的关键步骤和发现的内容，以便进行优化和复用。

---

## 相关技能

- `agent-shark-mindset`：用于仪表盘展示、发布结果以及生成截图证明。
- `wesley-web-operator`：在 gog CLI 或平台 API 失效时作为备用方案。
- `self-improving-agent`：用于优化 `.learnings/` 文件中的操作模式。
- `skill-combinator`：用于构建跨技能的自动化操作流程。

---

## 该技能生成的文件

- `AUDIT.md`：记录每次操作的前后日志信息（仅允许追加内容）。
- `screenshots/YYYY-MM-DD_{action}.png`：保存每次操作的屏幕截图。
- `logs/browser/YYYY-MM-DD.log`：记录异常情况及其详细追踪信息。
- `credentials/sessions/{platform}_session.json`：保存登录后的会话信息。
- `ERRORS.md`：记录操作失败时的详细错误信息。
- `LEARNINGS.md`：保存操作过程中的模式和选择器信息。
- `lessons.md`：记录任务执行过程中的关键信息。

---

## 其他说明

- 文件的生成和更新规则会在文档的相应部分详细说明。