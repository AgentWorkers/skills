---
name: clawdcursor
version: 0.6.0
description: AI桌面代理——通过您的OpenClaw代理控制Windows或macOS上的任何应用程序。将自然语言指令发送到Clawd Cursor API，它将处理所有操作：打开应用程序、点击按钮、输入文本、浏览网页、填写表单。只要您能点击某个元素，您的代理也能执行相同的操作。
homepage: https://clawdcursor.com
source: https://github.com/AmrDab/clawd-cursor
privacy: >
  Screenshots and UI data stay on the user's machine. If using Ollama (local), zero data leaves the host.
  If using a cloud provider (Anthropic, OpenAI, Kimi), screenshots/text are sent to that provider's API
  only — never to third-party servers or skill authors. The user controls which provider is used.
  The REST API binds to 127.0.0.1 only and is not network-accessible.
metadata:
  openclaw:
    # Note: bins check removed — OpenClaw's hasBinary() doesn't handle Windows
    # PATHEXT (.exe/.cmd), causing false "missing" on Windows even when node is
    # installed. Since install requires npm (which implies node), the check is
    # redundant. See: https://github.com/openclaw/openclaw/issues/TBD
    requires: {}
    install:
      - git clone https://github.com/AmrDab/clawd-cursor.git
      - cd clawd-cursor && npm install && npm run build
      - cd clawd-cursor && npx clawd-cursor doctor
      - cd clawd-cursor && npm start
    privacy:
      - Screenshots processed by user's own configured AI provider only
      - With Ollama, fully offline — no external API calls
      - With cloud providers, data goes only to user's chosen API endpoint
      - REST API binds to 127.0.0.1 only — not network accessible
notes:
  - In OpenClaw, this skill inherits the active agent's AI provider + API key.
  - Standalone CLI mode can still use AI_API_KEY / provider-specific env vars or Ollama.
---
# Clawd Cursor

**如果人类能在屏幕上完成某项操作，你也能做到。** 没有API？没有集成？没问题。  
每个应用程序都已经有用户界面（UI）——Clawd Cursor为你提供了“眼睛”和“手”，让你能够使用这些界面。  

没有任务是不可能的。只要它在屏幕上，就能被完成。  

> **重要提示 — 在使用之前请先阅读此内容**  

> 你的桌面AI代理通过用户机器上的GUI运行。这意味着：  
> 1. 你可以打开应用程序、点击按钮、输入文本、填写表单。  
> 2. 你可以看到屏幕上的内容（通过Clawd Cursor的截图功能）。  
> 3. 你可以与各种应用程序进行交互——浏览器、桌面应用程序、设置等。  
> 4. 你必须遵守安全规则：🟢 自动操作可以自由执行，🔴 需要用户确认的操作必须获得用户批准。  
> 5. 在访问敏感应用程序（如电子邮件、银行服务、私信、密码管理器）之前，你必须先询问用户。  
> 6. 如果有直接的工具可用（如文件读取、网络请求、命令行接口CLI），应优先使用它们。  

> 将Clawd Cursor视为你在用户电脑上的“手”和“眼睛”——在用户的许可下使用它。  

---

## 何时使用Clawd Cursor（代理使用说明）  
当你有可用的桌面UI代理时，可以在用户要求你与他们的桌面进行交互，或者没有其他工具能够完成任务时使用它。  

### Clawd Cursor的用途：  
- **根据用户请求执行桌面任务**：例如“打开Gmail并发送邮件”、“查看我的日历”  
- **阅读网页**：当网络请求或浏览器工具不可用时  
- **与桌面应用程序交互**：点击按钮、填写表单、查看结果  
- **浏览器任务**：搜索、导航、填写表单（当浏览器工具不可用时）  
- **视觉验证**：页面是否加载完成？UI显示了什么内容？  
- **跨应用程序的工作流程**：从一个应用程序复制内容并粘贴到另一个应用程序  
- **设置更改**：当用户明确要求时  

### ⚠️ 敏感应用程序政策  
在访问以下应用程序之前，**务必先询问用户**：  
- 电子邮件客户端（如Gmail、Outlook）  
- 银行或金融应用程序  
- 私人消息应用（如WhatsApp、Signal、Telegram）  
- 密码管理器  
- 管理面板或云控制台  

### 不要使用Clawd Cursor的情况：  
- 如果可以通过直接API调用或CLI命令更快地完成任务  
- 任务纯粹是计算性质的（如数学运算、文本生成、代码编写）  
- 你可以直接读取或写入文件  
- 浏览器工具或网络请求可以完成任务  

### 直接使用浏览器（快速途径）  
如果只需要快速获取页面内容，可以通过Playwright CDP直接连接Chrome：  
```js
const pw = require('playwright');
const browser = await pw.chromium.connectOverCDP('http://127.0.0.1:9222');
const pages = browser.contexts()[0].pages();
const text = await pages[0].innerText('body');
```  
这种方式比发送任务更快。  

| 场景 | 使用方式 | 原因 |  
|----------|-----|-----|  
| 阅读页面内容/文本 | CDP直接访问 | 即时且免费 |  
| 填写网页表单 | REST API | Clawd负责多步骤规划 |  
| 检查页面是否加载 | CDP直接访问 | 只需读取标题/URL |  
| 点击复杂的UI流程 | REST API | Clawd负责规划 |  
| 获取页面元素列表 | CDP直接访问 | 快速的DOM查询 |  
| 与桌面应用程序交互 | REST API | CDP仅适用于浏览器环境 |  

---

## REST API参考  
基础URL：`http://127.0.0.1:3847`  

> **注意：** 在Windows PowerShell中，使用`curl.exe`（带.exe后缀）或`Invoke-RestMethod`。裸露的`curl`被别名为`Invoke-WebRequest`，其行为可能不同。  

### 预启动检查  
在首次执行任务之前，请验证Clawd Cursor是否正在运行：  
```bash
curl.exe -s http://127.0.0.1:3847/health
```  
预期响应：`{"status":"ok","version":"0.6.0"}`  

如果连接失败，请**手动启动Clawd Cursor**（不要询问用户）：  
```powershell
# Find the skill directory and start the server
Start-Process -FilePath "node" -ArgumentList "dist/index.js","start" -WorkingDirectory "<clawd-cursor-directory>" -WindowStyle Hidden
Start-Sleep 3
# Verify it's running
curl.exe -s http://127.0.0.1:3847/health
```  
技能目录位于SKILL.md文件所在的目录中。请使用该目录作为工作目录。  

### 发送任务（异步执行 — 立即返回结果）  
`POST /task`用于发送任务，并立即返回响应。任务在后台执行。**你需要定期调用 `/status` 来获取任务完成状态。**  
```bash
curl.exe -s -X POST http://127.0.0.1:3847/task -H "Content-Type: application/json" -d "{\"task\": \"YOUR_TASK_HERE\"}"
```  
（具体命令在PowerShell中的实现见上文。）  

### 调用模式  
```
1. POST /task → get accepted
2. Wait 2 seconds
3. GET /status
4. If status is "idle" → done
5. If status is "waiting_confirm" → ASK THE USER, then POST /confirm based on their answer
6. If still running → wait 2 more seconds, go to step 3
7. If 60+ seconds → POST /abort and retry with clearer instructions
```  
（具体调用模式见上文。）  

### 检查任务状态  
```bash
curl.exe -s http://127.0.0.1:3847/status
```  
（具体调用方法见上文。）  

### 确认需要用户批准的操作  
某些操作（如发送消息、删除数据）需要用户确认。**🔴 绝不要自行批准这些操作。** 在发送`POST /confirm`请求之前，务必询问用户。这些机制是为了保护用户安全，请勿绕过。  
```bash
curl.exe -s -X POST http://127.0.0.1:3847/confirm -H "Content-Type: application/json" -d "{\"approved\": true}"
```  

### 中止任务  
```bash
curl.exe -s -X POST http://127.0.0.1:3847/abort
```  
（具体中止命令见上文。）  

### 查看日志（用于调试）  
```bash
curl.exe -s http://127.0.0.1:3847/logs
```  
（查看日志的方法见上文。）  

### 响应状态  
| 状态 | 响应内容 | 应该采取的措施 |  
|-------|----------|------------|  
| **已接受** | `{"accepted": true, "task": "..."}` | 继续等待任务完成 |  
| **正在执行** | `{"status": "acting", "currentTask": "...", "stepsCompleted": 2}` | 继续等待 |  
| **等待确认** | `{"status": "waiting_confirm", "currentStep": "..."}` | 发送`POST /confirm`请求 |  
| **已完成** | `{"status": "idle"}` | 任务已完成 |  
| **忙碌** | `{"error": "Agent is busy", "state": {...}}` | 等待或发送`POST /abort`请求中止任务 |  

---

## CDP直接访问  
Chrome必须以`--remote-debugging-port=9222`参数运行。  
### 快速检查：  
```bash
curl.exe -s http://127.0.0.1:9222/json/version
```  
如果返回JSON响应，说明Chrome已准备好使用。  

### 通过Playwright连接：  
```javascript
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const context = browser.contexts()[0];
const page = context.pages()[0];

// Read page content
const title = await page.title();
const url = page.url();
const text = await page.textContent('body');

// Click by role
await page.getByRole('button', { name: 'Submit' }).click();

// Fill a field
await page.getByLabel('Email').fill('user@example.com');

// Read specific elements
const buttons = await page.$$eval('button', els => els.map(e => e.textContent));
```  
（具体连接方法见上文。）  

---

## 任务编写指南  
1. **具体说明**：包括应用程序名称、URL、需要输入的文本、按钮名称等。  
2. **一次只发送一个任务**：等待上一个任务完成后再发送下一个。  
3. **描述任务目标，而非具体的点击操作**：例如“向john@example.com发送关于会议的邮件”，而不是“点击‘compose’按钮，然后点击‘to’字段”。  
4. **检查任务进度**：如果任务似乎卡住了，请检查状态。  
5. **不要在任务文本中包含凭据**：所有操作都会被记录下来。  

## 任务示例  
| 目标 | 需要执行的操作 |  
|------|-------------|  
| **简单导航** | `打开Chrome并访问github.com` |  
| **读取屏幕内容** | `Notepad中当前显示的文本是什么？` |  
| **跨应用程序操作** | **从Chrome标签页复制电子邮件地址并粘贴到Outlook的“To”字段** |  
| **填写表单** | **在打开的Chrome标签页中填写联系表单：姓名“John Doe”，电子邮件“john@example.com”** |  
| **与应用程序交互** | **打开Spotify并播放“Discover Weekly”播放列表** |  
| **更改设置** | **打开Windows设置并开启暗黑模式** |  
| **提取数据** | **读取Chrome中Bloomberg标签页显示的股票价格** |  
| **复杂浏览器操作** | **打开YouTube，搜索“Adele Hello”，并播放第一个视频结果** |  
| **验证** | **检查部署是否成功——在Chrome中查看Vercel控制台** |  
| **发送邮件** | **打开Gmail，向john@example.com发送邮件，主题：明天会议，正文：确认下午2点的会议** |  
| **截图** | **截取屏幕截图** |  

## 错误处理  
| 问题 | 解决方案 |  
|---------|----------|----|  
| 连接失败（端口：3847） | 启动Clawd Cursor：`cd clawd-cursor && npm start` |  
| 连接失败（端口：9222） | 通过CDP启动Chrome：`Start-Process chrome -ArgumentList "--remote-debugging-port=9222"` |  
| 代理显示“忙碌”状态 | 调用 `/status` 等待代理空闲，或发送`POST /abort`中止任务 |  
| 任务失败但无详细信息 | 查看`/logs`日志中的错误信息 |  
| 任务完成但结果错误 | 重新描述任务细节（包括应用程序名称、按钮文本、字段名称等） |  
| 同一任务反复失败 | 将任务拆分为更小的部分（每个任务单独处理） |  
| 需要用户确认 | 发送`POST /confirm`请求，带上`{"approved": true`或`{"approved": false}`参数 |  
| 任务卡顿超过60秒 | 发送`POST /abort`请求，然后尝试更简洁的描述方式 |  

## 工作原理——四层处理流程  
| 层次 | 功能 | 执行速度 | 成本 |  
|-------|------|------|------|  
| **0层：浏览器层** | URL检测 → 直接导航 | 即时 | 免费 |  
| **1层：动作路由器** | 正则表达式 + UI自动化 | 即时 | 免费 |  
| **1.5层：智能交互** | 由大型语言模型（LLM）生成计划 → CDP/UIDriver执行 | 约2-5秒 | 需要一次LLM调用 |  
| **2层：辅助决策层** | UI结构分析 → 语言模型决定下一步操作 | 约1秒 | 成本较低 |  
| **3层：计算机操作层** | 截取屏幕截图 → 视觉模型处理 | 约5-8秒 | 成本较高 |  

80%以上的任务由第0层和第1层处理（即时且免费）。视觉模型仅作为最后的解决方案使用。  

## 安全等级  
| 安全等级 | 操作类型 | 行为方式 |  
|------|---------|----------|------|  
| 🟢 自动操作 | 导航、阅读、打开应用程序 | 立即执行 |  
| 🟡 预览操作 | 输入文本、填写表单 | 执行前会记录日志 |  
| 🔴 需要用户确认的操作 | 发送消息、删除数据 | 在执行前会询问用户 |  

## 安全性与隐私保护  
- **网络隔离**：API仅绑定到`127.0.0.1`端口——无法从外部网络访问。验证方法：`netstat -an | findstr 3847`应显示`127.0.0.1:3847`  
- 截图仅保存在内存中，不会保存到磁盘（除非特别设置）。  
- 不会发送任何遥测数据或进行分析。  
- **数据流**：  
  - 使用Ollama时：完全离线处理，不发送任何外部网络请求。  
  - 使用云服务时：截图/文本仅发送到用户指定的API服务器，不会泄露给技能开发者或第三方。  
- **OpenClaw用户**：凭据信息会从本地配置文件中自动获取，不会存储在技能目录中。  
- 用户可以控制数据流向：用户可以选择使用哪种云服务。Ollama提供完全的隐私保护。  

## 代理自主控制  
- **自动操作**（导航、阅读、打开应用程序）会自动执行。  
- **需要用户确认的操作**（输入文本、填写表单）会在执行前记录日志。  
- **需要用户确认的操作**（发送消息、删除数据）在执行前会询问用户。  
- 代理在访问敏感应用程序（如电子邮件、银行服务、私信应用）时必须获得用户批准。  
- 代理绝不能自行批准这些操作。  

## 设置说明（用户操作指南）  
设置由用户完成。如果Clawd Cursor未运行，请使用相应的工具手动启动它：  
```powershell
Start-Process -FilePath "node" -ArgumentList "dist/index.js","start" -WorkingDirectory "<skill-directory>" -WindowStyle Hidden
```  
只有在无法启动Clawd Cursor时（例如Node.js未安装或构建文件缺失）才需要询问用户。  
```bash
git clone https://github.com/AmrDab/clawd-cursor.git
cd clawd-cursor
npm install && npm run build
npx clawd-cursor doctor    # auto-detects and configures everything
npm start                  # starts on port 3847
```  
（具体设置步骤因操作系统不同而异。）  

**macOS用户**：需要在系统设置中的“隐私与安全”选项中允许访问辅助功能。  
| 提供商 | 设置方法 | 成本 |  
|----------|-------|------|  
| **Ollama（免费）** | `ollama pull <model>` | 无需额外费用（完全离线使用） |  
| **任何云服务** | 设置`AI_API_KEY=your-key` | 根据服务提供商不同而异 |  
| **OpenClaw用户** | 自动配置，无需额外设置 | 使用已配置的云服务即可。 |  

## 性能优化  
已采取多种优化措施来减少任务执行时间和LLM API调用成本。详细信息请参考`perf/references/patches/`文件。  

### 应用过的优化措施：  
| 编号 | 优化内容 | 效果 |  
|---|------|--------|  
| 1 | 截图缓存 | 静态页面时减少90%的LLM调用次数 |  
| 2 | 并行截图处理 | 每步操作延迟减少30-40% |  
| 3 | A11y上下文缓存（TTL为2秒） | 避免不必要的进程创建 |  
| 4 | 截图压缩 | 削减52%的数据量（从120KB压缩至58KB） |  
| 5 | 异步日志记录 | 减少94%的事件循环阻塞 |  
| 6 | 流式处理LLM响应 | 每次LLM调用响应时间缩短1-3秒 |  
| 7 | 简化系统提示信息 | 减少约60%的提示信息显示次数 |  
| 8 | A11y上下文过滤 | 仅显示交互式元素，限制字符长度为3000个 |  
| 9 | 合并脚本执行 | 将多个脚本合并为一个执行 |  
| 10 | 任务栏缓存 | 缓存任务栏相关操作，减少等待时间 |  
| 11 | 延迟优化 | 任务执行时间减少50-150毫秒 |  

## 性能测试（分辨率2560x1440）  
| 测试指标 | v0.3（VNC） | v0.4（原生版本） | v0.4.1（优化版本） |  
|--------|------------|---------------|----------------------|  
| 截图获取时间 | 约850毫秒 | 约50毫秒 | 约57毫秒 |  
| 截图大小 | 约200KB | 约120KB | 约58KB |  
| A11y上下文处理时间 | 未缓存时约600毫秒 | 缓存后约462毫秒 |  
| A11y上下文处理时间（缓存后） | 0毫秒 | 2秒后缓存生效 |  
| 每步操作延迟 | 未缓存时约200-1500毫秒 | 缓存后约50-600毫秒 |  
| 系统提示信息显示次数 | 未缓存时约800次 | 缓存后约300次 |  
| 性能优化工具**：  
  - `perf/apply-optimizations.ps1`：应用所有优化措施  
  - `perf/perf-test.ts`：用于性能测试的脚本 |