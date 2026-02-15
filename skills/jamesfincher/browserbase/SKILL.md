---
name: browserbase-sessions
description: 创建并管理具有身份验证持久性的Browserbase云浏览器会话。适用于用户需要自动化浏览器操作、在多次交互中保持登录状态、抓取已认证的页面或管理云浏览器实例的场景。该功能支持会话创建、基于上下文的身份验证持久化、保持连接状态的重连、验证码处理、会话录制、截图生成以及会话清理等操作。
license: MIT
metadata:
  author: custom
  version: "2.0.0"
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["python3"]
      anyBins: ["uv", "pip"]
      env: ["BROWSERBASE_API_KEY", "BROWSERBASE_PROJECT_ID"]
    primaryEnv: "BROWSERBASE_API_KEY"
---

# Browserbase 会话管理技能

通过 Browserbase 管理持久的云浏览器会话。该技能能够创建会话，确保在多次交互过程中保持身份验证信息（如 cookies 和本地存储数据），自动解决 CAPTCHA 验证问题，并记录会话以供后续查看。

## 首次设置

### 第 1 步 — 获取 Browserbase 凭据

1. 如果您还没有注册，请访问 [browserbase.com](https://www.browserbase.com/) 进行注册。
2. 转到 **设置 → API 密钥**，复制您的 API 密钥（以 `bb_live_` 开头）。
3. 转到 **设置 → 项目**，复制您的项目 ID（一个 UUID）。

### 第 2 步 — 安装依赖项

```bash
cd {baseDir}/scripts && pip install -r requirements.txt
playwright install chromium
```

或者使用 uv：

```bash
cd {baseDir}/scripts && uv pip install -r requirements.txt
uv run playwright install chromium
```

### 第 3 步 — 设置环境变量

```bash
export BROWSERBASE_API_KEY="bb_live_your_key_here"
export BROWSERBASE_PROJECT_ID="your-project-uuid-here"
```

或者通过 OpenClaw 的 `skills.entries.browserbase-sessions.env` 在 `~/.openclaw/openclaw.json` 中进行配置。

### 第 4 步 — 运行设置测试

此测试会端到端验证所有配置（包括凭据、SDK、Playwright、API 连接以及实时测试）：

```bash
python3 {baseDir}/scripts/browserbase_manager.py setup
```

如果所有步骤都通过，您应该会看到 `"status": "success"` 的输出。如果有任何步骤失败，错误信息会明确指出需要修复的问题。

## 默认设置

每个会话都使用以下默认设置来支持研究工作流程：

- **CAPTCHA 解决：开启** — Browserbase 会自动解决 CAPTCHA 验证问题，从而无需手动干预即可完成登录流程和访问受保护页面。使用 `--no-solve-captchas` 可以禁用此功能。
- **会话记录：开启** — 每个会话都会被录制为视频，您可以稍后下载以供查看或分享。使用 `--no-record` 可以禁用此功能。
- **身份验证持久化** — 使用 `--persist` 参数可以在会话之间保持登录状态。

## 可用命令

所有命令都通过管理脚本执行：

```bash
python3 {baseDir}/scripts/browserbase_manager.py <command> [options]
```

### 设置与验证

运行完整的设置测试：
```bash
python3 {baseDir}/scripts/browserbase_manager.py setup
```

### 上下文管理（用于身份验证持久化）

创建一个命名上下文以存储登录状态：
```bash
python3 {baseDir}/scripts/browserbase_manager.py create-context --name github
```

列出所有保存的上下文：
```bash
python3 {baseDir}/scripts/browserbase_manager.py list-contexts
```

删除一个上下文（按名称或 ID）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py delete-context --context-id github
```

### 会话生命周期

创建一个新的会话（默认开启 CAPTCHA 解决和录制功能）：
```bash
# Basic session
python3 {baseDir}/scripts/browserbase_manager.py create-session

# Session with saved context (persist=true saves cookies on close)
python3 {baseDir}/scripts/browserbase_manager.py create-session --context-id github --persist

# Keep-alive session for long research (survives disconnections)
python3 {baseDir}/scripts/browserbase_manager.py create-session --context-id github --persist --keep-alive --timeout 3600

# Full options
python3 {baseDir}/scripts/browserbase_manager.py create-session \
  --context-id github \
  --persist \
  --keep-alive \
  --timeout 3600 \
  --region us-west-2 \
  --proxy \
  --block-ads \
  --viewport-width 1280 \
  --viewport-height 720
```

列出所有会话：
```bash
python3 {baseDir}/scripts/browserbase_manager.py list-sessions
python3 {baseDir}/scripts/browserbase_manager.py list-sessions --status RUNNING
```

获取会话详细信息：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-session --session-id <id>
```

终止一个会话：
```bash
python3 {baseDir}/scripts/browserbase_manager.py terminate-session --session-id <id>
```

### 浏览器自动化

导航到指定 URL：
```bash
# Navigate and get page title
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://example.com"

# Navigate and extract text
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://example.com" --extract-text

# Navigate and save screenshot
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://example.com" --screenshot /tmp/page.png

# Navigate and take full-page screenshot
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://example.com" --screenshot /tmp/full.png --full-page
```

截取当前页面的截图（不进行页面导航）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py screenshot --session-id <id> --output /tmp/current.png
python3 {baseDir}/scripts/browserbase_manager.py screenshot --session-id <id> --output /tmp/full.png --full-page
```

执行 JavaScript 代码：
```bash
python3 {baseDir}/scripts/browserbase_manager.py execute-js --session-id <id> --code "document.title"
```

获取 cookies：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-cookies --session-id <id>
```

### 录像、日志与调试

下载会话录像视频（必须先终止会话）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-recording --session-id <id> --output /tmp/session.webm
```

获取会话日志：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-logs --session-id <id>
```

获取实时调试 URL（用于查看正在运行的会话）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py live-url --session-id <id>
```

## 常见工作流程

### 工作流程 1：多会话研究并保持登录状态

```bash
# 1. One-time: create a named context for the site
python3 {baseDir}/scripts/browserbase_manager.py create-context --name myapp

# 2. Start a research session (captchas auto-solved, recording on)
python3 {baseDir}/scripts/browserbase_manager.py create-session --context-id myapp --persist --keep-alive --timeout 3600

# 3. Navigate to login — captchas solved automatically
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://myapp.com/login"
# Use execute-js to fill forms and submit

# 4. Do research, take screenshots
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://myapp.com/dashboard" --extract-text
python3 {baseDir}/scripts/browserbase_manager.py screenshot --session-id <id> --output /tmp/dashboard.png

# 5. Terminate (cookies saved to context)
python3 {baseDir}/scripts/browserbase_manager.py terminate-session --session-id <id>

# 6. Download recording to share
python3 {baseDir}/scripts/browserbase_manager.py get-recording --session-id <id> --output /tmp/research.webm

# 7. Next day: new session, already logged in!
python3 {baseDir}/scripts/browserbase_manager.py create-session --context-id myapp --persist --keep-alive --timeout 3600
```

### 工作流程 2：截图记录

```bash
python3 {baseDir}/scripts/browserbase_manager.py create-session
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://docs.example.com" --screenshot /tmp/docs_home.png
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://docs.example.com/api" --screenshot /tmp/docs_api.png --full-page
python3 {baseDir}/scripts/browserbase_manager.py terminate-session --session-id <id>
```

### 工作流程 3：录制并分享操作过程

```bash
# Session recording is ON by default
python3 {baseDir}/scripts/browserbase_manager.py create-session --context-id myapp --persist
# ... do your walkthrough (navigate, click, etc.) ...
python3 {baseDir}/scripts/browserbase_manager.py terminate-session --session-id <id>
# Download the video
python3 {baseDir}/scripts/browserbase_manager.py get-recording --session-id <id> --output /tmp/walkthrough.webm
```

## 重要说明

- **CAPTCHA 解决功能默认开启。** Browserbase 会在登录流程和页面加载时自动处理 CAPTCHA 验证。使用 `--no-solve-captchas` 可以禁用此功能。
- **录制功能默认开启。** 每个会话都会被录制。使用 `get-recording` 命令在会话结束后下载录像。使用 `--no-record` 可以禁用此功能。
- **连接超时**：创建会话后有 5 分钟的连接时间，超过时间会自动终止会话。
- **保持会话连接**：即使断开连接，会话也会保持状态，但需要手动终止。
- **上下文持久化**：在执行 `terminate-session --persist` 后等待几秒钟，然后再使用相同的上下文创建新会话。
- **命名上下文**：使用 `--name` 参数为上下文指定名称（例如 `github`、`slack`），并在需要使用上下文 ID 的地方使用该名称。
- **每个网站使用单独的上下文**：为不同的登录网站使用不同的上下文。
- **避免在同一上下文中同时运行多个会话**。
- **可用区域**：us-west-2（默认）、us-east-1、eu-central-1、ap-southeast-1。
- **会话超时**：60–21600 秒（最长 6 小时）。

## 错误处理

所有命令返回 JSON 格式的输出。出现错误时，输出中会包含一个 `"error"` 键。常见错误包括：
- `APIConnectionError`：无法访问 Browserbase API
- `RateLimitError`：您的计划允许的并发会话数量超出限制
- `APIStatusError`：参数无效或身份验证失败
- 环境变量缺失：请设置 `BROWSERBASE_API_KEY` 和 `BROWSERBASEPROJECT_ID`

## 参考文档

有关完整的 API 详细信息，请参阅 `{baseDir}/references/api-quick-ref.md`。