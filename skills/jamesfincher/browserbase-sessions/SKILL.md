---
name: browserbase-sessions
description: 创建并管理具有身份验证持久性的 Browserbase 云浏览器会话。当您需要自动化浏览器操作、在多次交互之间保持登录状态、抓取已认证的页面或管理云浏览器实例时，可以使用此功能。
license: MIT
homepage: https://docs.browserbase.com
metadata: {"author":"custom","version":"2.4.0","openclaw":{"emoji":"🌐","requires":{"bins":["python3"]},"primaryEnv":"BROWSERBASE_API_KEY"}}
---

# Browserbase会话技能

通过Browserbase管理持久的云浏览器会话。该技能可以创建会话，这些会话在多次交互中保持认证状态（cookie、本地存储），自动解决CAPTCHA，并记录会话以供后续查看。

## 代理检查清单（主动处理）

- 如果缺少`BROWSERBASE_API_KEY`或`BROWSERBASE PROJECT_ID`，**请向用户询问**（并告知他们在哪里可以找到这些信息）。在配置完成之前，不要运行Browserbase命令。
- 如果由于缺少Python依赖项（如`browserbase`或`playwright`导致导入错误），请运行：
  - `python3 {baseDir}/scripts/browserbase_manager.py install`
  - 然后重试原始命令。
- 询问用户希望持久化哪些内容以及如何组织这些内容：
  - **按应用/站点划分的工作区**（隔离）：`github`、`slack`、`stripe`
  - **按任务/项目划分的工作区**（多站点工作流程）：`invoice-run`、`lead-gen`、`expense-recon`
- 工作区会持久化以下内容：
  - 通过Browserbase的**上下文**（cookie + 存储）保持登录状态
  - 打开的标签页（URL + 标题快照），以便您可以从中断的地方继续浏览
- 当用户希望浏览器在聊天轮次之间保持打开状态时，优先使用工作区命令（`create-workspace`、`start-workspace`、`resume-workspace`、`stop-workspace`），而不是原始的会话命令。
- 在需要直接操作浏览器时，优先使用以下命令（`list-tabs`、`new-tab`、`switch-tab`、`close-tab`、`click`、`type`、`press`、`wait-for`、`go-back`、`go-forward`、`reload`、`read-page`），只有在必要时才使用`execute-js`。
- 每当打开浏览器（`start-workspace`、`resume-workspace`或`create-session`）时，立即分享人类远程控制链接：
  - 优先使用命令输出中的`human_handoff.share_url`。
  - 回复用户时，优先使用`human_handoff.share_text`或`human_handoff.share_markdown`。
  - 如果缺失，则使用`human_control_url`。
  - 如果缺失，运行`live-url`并分享其`human_handoff.share_url`。
- 关闭浏览器时，使用`stop-workspace`（而不是`terminate-session`），以便保存标签页快照和认证状态。

## 优化提示的响应模式

使用简短、一致的响应，让用户始终知道下一步该做什么。

当缺少凭据时：
```text
I need your Browserbase credentials before I can open a browser.
Please provide:
1) BROWSERBASE_API_KEY
2) BROWSERBASE_PROJECT_ID
```

当打开浏览器（会话/工作区）时：
```text
Browser is ready.
<human_handoff.share_text>
I can keep working while you browse.
```

当恢复现有工作区时：
```text
Reconnected to your existing workspace.
<human_handoff.share_text>
```

当实时URL暂时不可用时：
```text
The remote-control URL is temporarily unavailable. I’ll retry now.
```

## 首次设置

### 第1步 — 获取您的Browserbase凭据

1. 如果您还没有注册，请访问[browserbase.com](https://www.browserbase.com/)。
2. 转到**设置 → API密钥**并复制您的API密钥（以`bb_live_`开头）。
3. 转到**设置 → 项目**并复制您的项目ID（一个UUID）。

如果您有API密钥但不确定使用哪个项目ID，可以列出所有项目：

```bash
export BROWSERBASE_API_KEY="bb_live_your_key_here"
python3 {baseDir}/scripts/browserbase_manager.py list-projects
```

### 第2步 — 安装依赖项

安装Python依赖项和Playwright Chromium（推荐）：

```bash
python3 {baseDir}/scripts/browserbase_manager.py install
```

手动替代方案（使用pip/uv）：

```bash
cd {baseDir}/scripts && pip install -r requirements.txt
python3 -m playwright install chromium
```

### 第3步 — 设置环境变量

```bash
export BROWSERBASE_API_KEY="bb_live_your_key_here"
export BROWSERBASE_PROJECT_ID="your-project-uuid-here"
```

或者通过`~/.openclaw/openclaw.json`（JSON5）中的`skills.entries["browserbase-sessions"].env`进行配置。因为此技能设置了`primaryEnv: BROWSERBASE_API_KEY`，您也可以使用`skills.entries["browserbase-sessions"].apiKey`作为API密钥：

```json5
{
  skills: {
    entries: {
      "browserbase-sessions": {
        enabled: true,
        apiKey: "bb_live_your_key_here",
        env: {
          BROWSERBASE_PROJECT_ID: "your-project-uuid-here"
        }
      }
    }
  }
}
```

### 第4步 — 运行设置测试

这会端到端验证所有内容（凭据、SDK、Playwright、API连接以及实时测试）：

```bash
python3 {baseDir}/scripts/browserbase_manager.py setup --install
```

如果所有步骤都通过，您应该会看到“status”: “success”。如果有任何步骤失败，错误信息会明确指出需要修复的问题。

## 默认设置

每个会话都使用以下默认设置来支持研究工作流程：

- **CAPTCHA解决：开启** — Browserbase会自动解决CAPTCHA，因此登录流程和受保护的页面无需手动干预。可以使用`--no-solve-captchas`来禁用。
- **会话记录：开启** — Browserbase会记录会话（视频保存在仪表板中；可以通过API检索rrweb事件）。可以使用`--no-record`来禁用。
- **认证持久化** — 如果您使用上下文（或工作区），认证状态将默认被持久化。可以使用`--no-persist`来禁用持久化。

## 功能与限制（明确说明）

代理可以：
- 创建/检查/终止Browserbase会话和上下文。
- 使用工作区在聊天轮次之间保持浏览器“打开”状态（保持会话活跃 + 恢复标签页）。
- 通过Browserbase上下文（`persist=true`）在会话之间保持登录状态。
- 通过重新打开最后保存的打开标签页（URL + 标题快照）来恢复浏览位置。
- 提供实时调试器URL，以便用户在代理继续工作时可以手动浏览。
- 使用交互式浏览器控制：列出/打开/切换/关闭标签页，点击/输入/按键，等待选择器/文本/URL状态，后退/前进/重新加载，以及阅读页面文本/HTML/链接。
- 截取屏幕截图，运行JavaScript，读取cookie，获取日志和rrweb记录事件。

代理无法：
- 无限期地保持会话运行（Browserbase会设置超时；最长为6小时）。
- 完整恢复浏览器的历史记录（仅恢复打开的URL）。
- 除非代理重新连接或截取屏幕截图，否则无法可靠地“看到”用户在实时调试器中执行的操作。
- 在没有用户参与的情况下绕过MFA/SSO。
- 通过API下载仪表板视频（API返回的是rrweb事件，而不是视频文件）。

## 可用命令

所有命令都通过管理器脚本执行：

```bash
python3 {baseDir}/scripts/browserbase_manager.py <command> [options]
```

### 设置与验证

安装依赖项（每个环境只需安装一次）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py install
```

运行完整的设置测试：
```bash
python3 {baseDir}/scripts/browserbase_manager.py setup --install
```

### 工作区（推荐）

工作区是在聊天过程中保持浏览器“打开”状态并稍后继续使用的推荐方式。工作区包含：
- 一个Browserbase **上下文**（持久化cookie + 本地/会话存储，因此您可以保持登录状态）
- 一个本地的**标签页快照**（URLs + 标题），以便在下一个会话中恢复标签页（注意：这仅恢复打开的URL，而不是完整的浏览历史记录）
- 当前的**活动会话ID**，以便代理可以重新连接

#### 任务工作区（多站点流程）

单个Browserbase上下文是一个浏览器配置文件，因此它可以同时让您登录到**多个站点**。对于“在站点A上执行某些操作，然后在站点B上执行某些操作”之类的工作流程，创建一个**任务工作区**并将两个站点作为标签页打开：

```bash
python3 {baseDir}/scripts/browserbase_manager.py create-workspace --name invoice-run
python3 {baseDir}/scripts/browserbase_manager.py start-workspace --name invoice-run --timeout 21600
python3 {baseDir}/scripts/browserbase_manager.py live-url --workspace invoice-run
```

如果您需要账户/cookie隔离（不同的登录，减少跨站副作用），请为每个应用/站点使用单独的工作区。

创建并启动工作区：
```bash
python3 {baseDir}/scripts/browserbase_manager.py create-workspace --name github
python3 {baseDir}/scripts/browserbase_manager.py list-workspaces
python3 {baseDir}/scripts/browserbase_manager.py start-workspace --name github --timeout 21600
# Share this field with the user immediately:
# human_handoff.share_url (fallback: human_control_url / live_urls.debugger_url)
```

注意：`start-workspace`会通过Playwright执行短暂的“预热连接”，即使用户尚未打开实时调试器，也会避免会话因5分钟的连接要求而终止。

当用户在实时调试器中浏览时，代理可以继续工作。要稍后恢复：
```bash
python3 {baseDir}/scripts/browserbase_manager.py resume-workspace --name github
```

对于长时间运行的会话（特别是当用户手动打开/关闭标签页时），请定期获取快照：
```bash
python3 {baseDir}/scripts/browserbase_manager.py snapshot-workspace --name github
```

完成操作后，始终通过工作区命令停止会话：
```bash
python3 {baseDir}/scripts/browserbase_manager.py stop-workspace --name github
```

要检查工作区保存的内容（上下文ID、活动会话ID、标签页、历史记录）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-workspace --name github
```

大多数命令都接受`--workspace <name>`而不是`--session-id`：
```bash
python3 {baseDir}/scripts/browserbase_manager.py navigate --workspace github --url "https://github.com/settings/profile"
python3 {baseDir}/scripts/browserbase_manager.py screenshot --workspace github --output /tmp/profile.png
python3 {baseDir}/scripts/browserbase_manager.py execute-js --workspace github --code "document.title"
```

### 上下文管理（用于认证持久化）

创建一个命名上下文以存储登录状态：
```bash
python3 {baseDir}/scripts/browserbase_manager.py create-context --name github
```

列出所有保存的上下文：
```bash
python3 {baseDir}/scripts/browserbase_manager.py list-contexts
```

删除上下文（按名称或ID）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py delete-context --context-id github
```

### 会话生命周期

创建新会话（默认启用CAPTCHA解决和记录）：
```bash
# Basic session
python3 {baseDir}/scripts/browserbase_manager.py create-session

# Session with saved context (persist=true by default when a context is used)
python3 {baseDir}/scripts/browserbase_manager.py create-session --context-id github

# Keep-alive session for long research (survives disconnections)
python3 {baseDir}/scripts/browserbase_manager.py create-session --context-id github --keep-alive --timeout 3600

# Full options
python3 {baseDir}/scripts/browserbase_manager.py create-session \
  --context-id github \
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

获取会话详情：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-session --session-id <id>
```

终止会话：
```bash
python3 {baseDir}/scripts/browserbase_manager.py terminate-session --session-id <id>
```

### 浏览器自动化

导航到URL：
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

管理标签页：
```bash
python3 {baseDir}/scripts/browserbase_manager.py list-tabs --session-id <id>
python3 {baseDir}/scripts/browserbase_manager.py new-tab --session-id <id> --url "https://example.org"
python3 {baseDir}/scripts/browserbase_manager.py switch-tab --session-id <id> --tab-index 1
python3 {baseDir}/scripts/browserbase_manager.py close-tab --session-id <id> --tab-url-contains "example.org"
```

与页面交互：
```bash
python3 {baseDir}/scripts/browserbase_manager.py click --session-id <id> --selector "button[type='submit']"
python3 {baseDir}/scripts/browserbase_manager.py type --session-id <id> --selector "input[name='email']" --text "user@example.com" --clear
python3 {baseDir}/scripts/browserbase_manager.py press --session-id <id> --key "Enter"
python3 {baseDir}/scripts/browserbase_manager.py wait-for --session-id <id> --selector ".dashboard-ready" --timeout-ms 45000
```

控制导航状态：
```bash
python3 {baseDir}/scripts/browserbase_manager.py go-back --session-id <id>
python3 {baseDir}/scripts/browserbase_manager.py go-forward --session-id <id>
python3 {baseDir}/scripts/browserbase_manager.py reload --session-id <id>
```

阅读当前页面：
```bash
python3 {baseDir}/scripts/browserbase_manager.py read-page --session-id <id> --max-text-chars 20000
python3 {baseDir}/scripts/browserbase_manager.py read-page --session-id <id> --include-links --max-links 30
python3 {baseDir}/scripts/browserbase_manager.py read-page --session-id <id> --include-html --max-html-chars 120000
```

截取当前页面的屏幕截图（不进行导航）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py screenshot --session-id <id> --output /tmp/current.png
python3 {baseDir}/scripts/browserbase_manager.py screenshot --session-id <id> --output /tmp/full.png --full-page
```

执行JavaScript：
```bash
python3 {baseDir}/scripts/browserbase_manager.py execute-js --session-id <id> --code "document.title"
```

获取cookie：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-cookies --session-id <id>
```

上述所有命令也都支持`--workspace <name>`，以便自动使用当前活动的工作区会话。

### 录制、日志与调试

获取rrweb记录事件（必须先终止会话）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-recording --session-id <id> --output /tmp/session.rrweb.json
```

获取会话日志：
```bash
python3 {baseDir}/scripts/browserbase_manager.py get-logs --session-id <id>
```

获取实时调试URL（用于查看正在运行的会话）：
```bash
python3 {baseDir}/scripts/browserbase_manager.py live-url --session-id <id>
# Share: human_handoff.share_url
```

## 常见工作流程

### 工作流程1：具有持久登录的多会话研究

```bash
# 1. One-time: create a workspace for the site (creates a Browserbase Context + local state)
python3 {baseDir}/scripts/browserbase_manager.py create-workspace --name myapp

# 2. Start a keep-alive session (tabs restored from last snapshot, login persisted via context)
python3 {baseDir}/scripts/browserbase_manager.py start-workspace --name myapp --timeout 3600

# 3. Open the live debugger URL so the user can log in / browse while you keep chatting
python3 {baseDir}/scripts/browserbase_manager.py live-url --workspace myapp

# 4. Do research, take screenshots (workspace auto-tracks tabs + history)
python3 {baseDir}/scripts/browserbase_manager.py navigate --workspace myapp --url "https://myapp.com/dashboard" --extract-text
python3 {baseDir}/scripts/browserbase_manager.py screenshot --workspace myapp --output /tmp/dashboard.png

# 5. When done: stop-workspace snapshots tabs + persists auth state back to the context
python3 {baseDir}/scripts/browserbase_manager.py stop-workspace --name myapp

# 6. Later: resume and pick up where you left off
python3 {baseDir}/scripts/browserbase_manager.py resume-workspace --name myapp
```

### 工作流程1b：跨多个站点的任务工作流程（持久化标签页+登录）

```bash
# 1) Create a task workspace (one browser profile that can stay logged into multiple sites)
python3 {baseDir}/scripts/browserbase_manager.py create-workspace --name lead-gen

# 2) Start it and open the live debugger so the user can log in on both sites
python3 {baseDir}/scripts/browserbase_manager.py start-workspace --name lead-gen --timeout 21600
python3 {baseDir}/scripts/browserbase_manager.py live-url --workspace lead-gen

# 3) Agent can navigate and capture state while you chat (tabs snapshot includes both Site A and Site B)
python3 {baseDir}/scripts/browserbase_manager.py navigate --workspace lead-gen --url "https://site-a.example.com" --extract-text
python3 {baseDir}/scripts/browserbase_manager.py navigate --workspace lead-gen --url "https://site-b.example.com" --extract-text

# 4) If the user is manually opening/closing tabs in the debugger, snapshot occasionally:
python3 {baseDir}/scripts/browserbase_manager.py snapshot-workspace --name lead-gen

# 5) Stop to persist auth + tabs snapshot
python3 {baseDir}/scripts/browserbase_manager.py stop-workspace --name lead-gen
```

### 工作流程2：截图文档

```bash
python3 {baseDir}/scripts/browserbase_manager.py create-session
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://docs.example.com" --screenshot /tmp/docs_home.png
python3 {baseDir}/scripts/browserbase_manager.py navigate --session-id <id> --url "https://docs.example.com/api" --screenshot /tmp/docs_api.png --full-page
python3 {baseDir}/scripts/browserbase_manager.py terminate-session --session-id <id>
```

### 工作流程3：录制并分享操作过程

```bash
# Session recording is ON by default
python3 {baseDir}/scripts/browserbase_manager.py create-session --context-id myapp
# ... do your walkthrough (navigate, click, etc.) ...
python3 {baseDir}/scripts/browserbase_manager.py terminate-session --session-id <id>
# Save rrweb recording events
# (Video is available in the Browserbase Dashboard; this fetches rrweb events)
python3 {baseDir}/scripts/browserbase_manager.py get-recording --session-id <id> --output /tmp/walkthrough.rrweb.json
```

## 重要说明

- **CAPTCHA解决默认是开启的。** Browserbase在登录流程和页面加载期间自动处理CAPTCHA。可以使用`--no-solve-captchas`来禁用。
- **记录默认是开启的。** 视频保存在Browserbase仪表板中；`get-recording`可以获取rrweb事件（主标签页）以供程序化回放。可以使用`--no-record`来禁用。
- **连接超时**：创建后有5分钟的连接时间，之后会自动终止。
- **保持会话活跃**：在断开连接后仍会保持会话状态，必须明确终止。
- **上下文持久化**：如果使用`persist=true`创建会话，则在终止后等待几秒钟再使用相同的上下文创建新会话。
- **命名上下文**：使用`--name`与`create-context`来保存友好的名称（例如`github`、`slack`）。在任何需要上下文ID的地方使用该名称。
- **工作区状态**：工作区存储在`~/.browserbase/workspaces/<name>.json`（或`BROWSERBASE_CONFIG_DIR/workspaces`）中。它们包含上下文ID、活动会话ID和最后保存的标签页快照。
- **每个站点一个上下文**：为不同的认证站点使用单独的上下文。
- **避免在同一上下文中同时进行多个会话**。
- **区域**：us-west-2（默认）、us-east-1、eu-central-1、ap-southeast-1。
- **会话超时**：60–21600秒（最长6小时）。
- **费用/限制**：您的Browserbase计划有使用限制（浏览器使用时间、代理数据、并发数）。保持会话活跃会消耗时间；终止会话并设置合理的`--timeout`值以控制费用。请查看Browserbase仪表板上的当前配额。

## 错误处理

所有命令都会返回JSON输出。出现错误时，输出中包含一个“error”键。常见错误包括：
- `APIConnectionError`：无法访问Browserbase API
- `RateLimitError`：您的计划允许的并发会话数量过多
- `APIStatusError`：参数无效或认证失败
- 缺少环境变量：设置`BROWSERBASE_API_KEY`和`BROWSERBASE_PROJECT_ID`

## 参考

有关完整的API详细信息，请阅读`{baseDir}/references/api-quick-ref.md`。