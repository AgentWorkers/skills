---
name: autofillin
description: 使用 Playwright 浏览器自动化工具实现的自动化网页表单填写和文件上传功能。该功能支持登录信息的持久化保存、表单的自动检测、文件的上传，并在提交前等待用户的手动确认。
version: 1.2.0
trigger: autofillin
author: leohan123123
tags: automation, form, upload, browser, playwright, mcp
---

# AutoFillIn - 浏览器表单自动化技能

**触发命令**: `autofillin`

这是一个智能的自动化技能，能够自动填写网页表单、将文件/文件夹上传到正确的位置，并处理包含持久登录功能的多字段提交。

## v1.2.0 的新功能

- **错误处理增强**：提供了更详细的错误信息，实现了优雅的错误恢复机制。
- **配置整合**：将 `mcp-config` 文件合并到了 `SKILL.md` 中。
- **稳定性提升**：改进了端口冲突处理和进程管理机制。
- **跨平台兼容性优化**：提升了 Windows 和 Linux 系统的兼容性。

## 更新日志

| 版本 | 更新内容 |
|---------|---------|
| v1.2.0 | 错误处理增强，配置整合，稳定性提升 |
| v1.1.0 | 增加了对 Playwright 的支持，实现了会话持久化，支持文件夹上传 |
| v1.0.0 | 首次发布，包含 Chrome 调试模式 |

## 主要功能

- 可以导航到任何网页表单的 URL。
- 自动填充文本字段、文本区域和下拉菜单。
- 将文件/文件夹上传到表单中的正确位置。
- 通过浏览器存储实现持久登录。
- 提交前会等待用户手动确认。
- 支持多文件上传，并能精确控制文件上传的位置。
- 具有优雅的错误处理机制。

## 快速设置

```bash
# 1. Install Playwright browsers
npx playwright install chromium

# 2. First-time login (saves session for reuse)
npx playwright open --save-storage=~/.playwright-auth.json "https://your-target-site.com"
# Login manually in the browser that opens, then close it

# 3. Future runs will auto-login using saved session
npx playwright open --load-storage=~/.playwright-auth.json "https://your-target-site.com"
```

## MCP 配置

请将以下配置添加到您的 MCP 设置中（例如：Claude Code、OpenCode 等）：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-playwright"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/"]
    }
  }
}
```

### 用于 shell 集成的环境变量

```bash
export CHROME_DEBUG_PORT=9222
export CHROME_USER_DATA_DIR="$HOME/.chrome-autofillin"
```

## 浏览器自动化选项

### 选项 1：Playwright CLI（推荐用于需要 OAuth 认证的网站）

```bash
# First login - saves session
npx playwright open --save-storage=~/.playwright-auth.json "https://molthub.com/upload"

# Subsequent uses - loads saved session
npx playwright open --load-storage=~/.playwright-auth.json "https://molthub.com/upload"
```

**优点**：
- 不会受到 Google/GitHub OAuth 的“不安全浏览器”限制。
- 跨次运行时保持会话状态。
- 与 MCP 的浏览器工具兼容。

### 选项 2：Chrome 调试模式（适用于非 OAuth 网站）

```bash
# Start Chrome with debug port
./scripts/start-chrome.sh "https://example.com/form"

# With your default Chrome profile (keeps existing logins)
./scripts/start-chrome.sh --use-default-profile "https://example.com/form"
```

**注意**：使用自定义 `--user-data-dir` 参数的 Chrome 调试模式可能会被 Google OAuth 禁用。对于需要 Google/GitHub 登录的网站，请使用 Playwright。

## 使用示例

### 基本表单填写

```
autofillin https://example.com/form
- Fill "Name" field with "John Doe"
- Fill "Email" field with "john@example.com"
- Upload resume.pdf to file input
```

### 使用 MoltHub 技能进行文件上传

```
autofillin https://molthub.com/upload

Form Data:
- Slug: autofillin
- Display name: AutoFillIn - Browser Form Automation Skill
- Version: 1.2.0
- Tags: automation, browser, form, playwright, mcp
- Changelog: v1.2.0 - Enhanced error handling, consolidated config

Upload:
- Folder: ~/clawd/skills/autofillin/

[WAIT FOR MANUAL CONFIRMATION TO PUBLISH]
```

### 带有位置映射的多文件上传

```
autofillin https://example.com/document-upload

Files to upload:
- Position 1 (ID Document): ~/documents/id_card.pdf
- Position 2 (Proof of Address): ~/documents/utility_bill.pdf
- Position 3 (Photo): ~/photos/headshot.jpg

[WAIT FOR MANUAL CONFIRMATION]
```

## 工作流程

```
1. BROWSER SETUP
   - Check for saved session (~/.playwright-auth.json)
   - Launch Playwright Chromium with session
   - Or prompt for one-time login if no session exists

2. NAVIGATION & LOGIN
   - Navigate to target URL
   - Detect if login is required
   - If login needed: Fill username, prompt for password, save session

3. PAGE ANALYSIS
   - Take accessibility snapshot
   - Identify all form fields
   - Map field labels to input elements

4. AUTO-FILL PHASE
   - Fill text fields using fill() or fill_form()
   - Select dropdown options
   - Upload files/folders via upload_file()

5. CONFIRMATION PHASE
   - Display summary of filled data
   - WAIT FOR MANUAL CONFIRMATION
   - User reviews and clicks Submit/Publish
```

## 使用的 MCP 工具

| 工具 | 用途 |
|------|---------|
| take_snapshot | 获取页面的访问结构树（DOM 树） |
| fill | 填写单个表单字段 |
| fill_form | 同时填写多个表单字段 |
| upload_file | 上传文件或文件夹 |
| browser_click | 点击按钮 |
| evaluate_script | 运行 JavaScript 代码 |
| navigate_page | 导航到指定 URL |

## 凭据管理

### 安全存储（推荐）

```bash
# Use macOS Keychain
security add-generic-password -a "github" -s "autofillin" -w "your-password"
security find-generic-password -a "github" -s "autofillin" -w

# Use Linux secret-tool
secret-tool store --label="autofillin-github" service autofillin username github

# Use Windows Credential Manager
cmdkey /add:autofillin-github /user:github /pass:your-password
```

## 会话持久化

会话数据保存在 `~/.playwright-auth.json` 文件中，包括 cookies、localStorage 和 sessionStorage 的内容。

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| “不安全浏览器”提示 | 受 Google OAuth 限制 | 使用 Playwright 替代 Chrome 调试模式 |
| 需要登录 | 会话过期 | 使用 `--save-storage` 参数运行脚本 |
| 元素未找到 | 页面内容已更改 | 重新获取页面的访问结构树 |
| 上传失败 | 文件类型错误 | 检查文件路径是否正确 |
| 端口已被占用 | 另有一个 Chrome 实例正在运行 | 脚本会自动终止冲突的进程 |
| 未找到 Chrome | Chrome 未安装 | 运行 `setup-env.sh` 脚本进行配置 |

## 故障排除

### Chrome 无法以调试模式启动
```bash
# Check if port is in use
lsof -i:9222

# Kill existing processes
pkill -f "remote-debugging-port=9222"

# Retry
./scripts/start-chrome.sh "https://example.com"
```

### 会话无法持久化
```bash
# Verify auth file exists
ls -la ~/.playwright-auth.json

# Re-authenticate
npx playwright open --save-storage=~/.playwright-auth.json "https://target-site.com"
```

### 文件上传失败
- 确保文件路径是绝对路径。
- 检查文件权限：`ls -la /path/to/file`
- 对于文件夹上传，请确认文件路径包含 `webkitdirectory` 属性。

## 本技能包含的文件

```
autofillin/
├── SKILL.md              # This documentation (includes MCP config)
└── scripts/
    ├── setup-env.sh      # Environment setup (cross-platform)
    ├── start-chrome.sh   # Chrome debug launcher
    └── autofillin.sh     # Main orchestrator with error handling
```

## 作者

- GitHub: [@leohan123123](https://github.com/leohan123123)

## 许可证

MIT