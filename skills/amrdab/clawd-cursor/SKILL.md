---
name: clawdcursor
version: 0.6.3
description: AI桌面代理——通过您的OpenClaw代理控制Windows或macOS上的任何应用程序。您可以将自然语言指令发送到Clawd Cursor API，它会完成所有操作：打开应用程序、点击按钮、输入文本、浏览网页、填写表单。只要您能够点击某个元素，您的代理也同样可以执行这些操作。
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
      - cd clawd-cursor && npm install && npm run setup
      - cd clawd-cursor && clawdcursor doctor
      - cd clawd-cursor && clawdcursor start
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
每个应用程序都有用户界面（UI）——Clawd Cursor为你提供了“眼睛”和“手”，让你能够使用这些界面。  

没有任务是不可能的。只要它在屏幕上，就能被完成。  

> **重要提示 — 在使用之前请先阅读此内容**  

> 你有一个通过图形用户界面（GUI）在用户机器上运行的桌面AI代理。这意味着：  
> 1. 你可以打开应用程序、点击按钮、输入文本、填写表单。  
> 2. 你可以看到屏幕上的内容（通过Clawd Cursor的截图功能）。  
> 3. 你可以与各种应用程序进行交互——浏览器、桌面应用程序、设置等。  
> 4. 你必须遵守安全规则：🟢 自动操作可以自由执行，🔴 需要用户确认的操作必须获得用户批准。  
> 5. 在访问敏感应用程序（如电子邮件、银行服务、私人消息、密码管理器）之前，你必须先询问用户。  
> 6. 如果有直接的工具可用（如文件读取、网络请求、命令行接口CLI），应优先使用这些工具，而不是依赖桌面自动化。  

> 将Clawd Cursor视为你在用户电脑上的“手”和“眼睛”——在用户的许可下使用它。  

---

## 何时使用Clawd Cursor（代理使用说明）  

当你有可用的桌面UI代理时，可以在用户要求你与其桌面进行交互时使用它，或者当其他工具无法完成任务时使用它。  

### 开发者术语解释：  
- **工具**：直接的功能（如API调用、文件系统操作、shell命令、网络请求、浏览器命令）。  
- **技能**：封装的工作流程或领域逻辑，可能调用一个或多个工具。  
- **Clawd Cursor**：一种用于执行GUI操作的技能。在OpenClaw的其他工具/技能能够完成相同任务但无需GUI时使用它。  

### Clawd Cursor的用途（示例，非限制）：  
Clawd Cursor可以执行**所有在GUI中可见且可交互的操作**（需符合安全政策）。  
- **用户请求的桌面任务**：例如“打开Gmail并发送邮件”、“查看日历”。  
- **读取网页内容**：当网络请求或浏览器工具不可用时。  
- **与桌面应用程序交互**：点击按钮、填写表单、查看结果。  
- **浏览器相关任务**：搜索、导航、填写表单（当浏览器工具不可用时）。  
- **视觉验证**：页面是否加载完成？UI显示了什么内容？  
- **跨应用程序操作**：从一个应用程序复制内容并粘贴到另一个应用程序中。  
- **设置更改**：当用户明确要求时。  

### ⚠️ 敏感应用程序政策  
在访问以下应用程序之前，**务必先询问用户**：  
- 邮件客户端（如Gmail、Outlook）  
- 银行或金融应用程序  
- 私人消息应用（如WhatsApp、Signal、Telegram）  
- 密码管理器  
- 管理面板或云控制台  

### 不要使用Clawd Cursor的情况：  
- 如果可以通过直接API调用或CLI命令更快地完成任务。  
- 任务纯粹是计算性质的（如数学运算、文本生成、代码编写）。  
- 你可以直接读取/写入文件。  
- 浏览器工具或网络请求功能可以处理该任务。  

## OpenClaw与Clawd Cursor的协作规则（避免重复）  
Clawd Cursor应被视为**OpenClaw的GUI执行层**，而不是独立的执行工具。  

### 任务执行顺序：  
1. **优先使用OpenClaw的原生工具**（文件系统操作、API调用、shell命令、原生技能）。  
2. **其次使用浏览器原生的自动化功能**（如Playwright/CDP）。  
3. **仅在需要桌面UI交互时，使用Clawd Cursor的API (`POST /task`)。  

### 实用原则：  
- 如果OpenClaw已有可靠的技能/工具可以完成任务，就使用它们。  
- 当没有API或工具可用，或者用户明确要求GUI交互时，使用Clawd Cursor。  
这样可以保证行为的一致性，降低延迟和成本，并避免OpenClaw代理与Clawd Cursor之间的逻辑重复。  

### 通用任务处理流程：  
对于“完成任务”的请求，分为三个步骤：  
1. **在OpenClaw中规划**：将任务分解为API/CLI/浏览器/GUI子任务。  
2. **优先选择效率高的方法**：API + CLI + 直接使用浏览器。  
3. **仅将剩余的GUI步骤交给Clawd Cursor处理**。  

**思考方式**：**“OpenClaw负责规划，Clawd Cursor在需要时执行GUI操作。”  

### 直接使用浏览器（快速路径）  
对于简单的页面内容读取，可以通过Playwright CDP直接连接浏览器：  
```js
const pw = require('playwright');
const browser = await pw.chromium.connectOverCDP('http://127.0.0.1:9222');
const pages = browser.contexts()[0].pages();
const text = await pages[0].innerText('body');
```  
这种方式比发送任务更快。  

| 场景 | 使用方法 | 原因 |  
|----------|-----|-----|  
| 读取页面内容/文本 | CDP直接访问 | 即时且无需额外操作 |  
| 填写表单 | 使用API (`POST /task`) | Clawd负责整个流程的规划 |  
| 检查页面是否加载 | CDP直接访问 | 只需读取标题/URL |  
| 点击复杂UI元素 | 使用API (`POST /task`) | Clawd负责整个流程的规划 |  
| 获取页面元素列表 | CDP直接访问 | 快速的DOM查询 |  
| 与桌面应用程序交互 | 使用API (`POST /task`) | CDP仅适用于浏览器操作 |  

---

## REST API参考  
基础URL：`http://127.0.0.1:3847`  

> **注意**：在Windows PowerShell中，使用`curl.exe`（带`.exe`后缀）或`Invoke-RestMethod`。裸露的`curl`命令会被别名为`Invoke-WebRequest`，其行为可能不同。  

### 预启动检查  
在首次使用前，请确认Clawd Cursor正在运行：  
```bash
curl.exe -s http://127.0.0.1:3847/health
```  
预期响应：`{"status":"ok","version":"0.6.0"}`  
如果连接失败，请**手动启动Clawd Cursor**（不要让用户操作）：  
```powershell
# Find the skill directory and start the server
Start-Process -FilePath "node" -ArgumentList "dist/index.js","start" -WorkingDirectory "<clawd-cursor-directory>" -WindowStyle Hidden
Start-Sleep 3
# Verify it's running
curl.exe -s http://127.0.0.1:3847/health
```  
Clawd Cursor的技能目录位于SKILL.md文件所在的目录中。使用该目录作为工作目录。  

### 发送任务（异步执行，立即返回结果）  
`POST /task`用于发送任务并立即返回响应。任务在后台执行。**你需要通过`/status`接口查询任务状态**：  
```bash
curl.exe -s -X POST http://127.0.0.1:3847/task -H "Content-Type: application/json" -d "{\"task\": \"YOUR_TASK_HERE\"}"
```  
（具体实现代码见PowerShell示例。）  

### 状态查询流程  
```
1. POST /task → get accepted
2. Wait 2 seconds
3. GET /status
4. If status is "idle" → done
5. If status is "waiting_confirm" → ASK THE USER, then POST /confirm based on their answer
6. If still running → wait 2 more seconds, go to step 3
7. If 60+ seconds → POST /abort and retry with clearer instructions
```  

### 确认操作安全性  
某些操作（如发送消息、删除数据）需要用户确认。**🔴 绝不要自行批准这些操作**。始终在发送请求前获取用户确认。  

### 中止任务  
```bash
curl.exe -s -X POST http://127.0.0.1:3847/abort
```  

### 查看日志（用于调试）  
```bash
curl.exe -s http://127.0.0.1:3847/logs
```  
该命令会返回最近200条日志记录。任务失败时，请检查`error`或`warn`字段。  

### 响应状态  
| 状态 | 响应内容 | 处理方式 |  
|-------|----------|------------|  
| **已接受** | `{"accepted": true, "task": "..."}` | 继续查询任务状态 |  
| **正在执行** | `{"status": "acting", "currentTask": "...", "stepsCompleted": 2}` | 继续查询 |  
| **等待确认** | `{"status": "waiting_confirm", "currentStep": "..."}` | 发送`POST /confirm`请求确认 |  
| **已完成** | `{"status": "idle"}` | 任务完成 |  
| **忙碌** | `{"error": "Agent is busy", "state": {...}` | 等待或发送`POST /abort`中止任务 |  

---

## CDP直接访问说明  
Chrome浏览器必须开启`--remote-debugging-port=9222`选项。  
### 快速检查：  
```bash
curl.exe -s http://127.0.0.1:9222/json/version
```  
如果返回JSON响应，说明Chrome已准备好配合使用。  

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

---

## 任务编写指南：  
1. **具体说明**：包含应用程序名称、URL、需要输入的文本、按钮名称等。  
2. **一次只发送一个任务**：等待任务完成后再发送下一个。  
3. **描述任务目标**：例如“向john@example.com发送关于会议的邮件”，而不是“点击‘compose’按钮，然后点击‘field’按钮”。  
4. **检查任务进度**：如果任务卡住，请检查状态。  
5. **不要在任务文本中包含凭据**：所有操作都会被记录。  

## 任务示例：  
| 目标 | 需要执行的操作 |  
|------|-------------|  
| **简单导航** | `打开Chrome浏览器并访问github.com` |  
| **读取屏幕内容** | `当前Notepad中显示的文本是什么？` |  
| **跨应用程序操作** | **从Chrome标签页复制电子邮件地址并粘贴到Outlook的“收件人”字段** |  
| **填写表单** | **在打开的Chrome标签页中填写联系表单：姓名“John Doe”，电子邮件“john@example.com”** |  
| **与应用程序交互** | **打开Spotify并播放“Discover Weekly”播放列表** |  
| **更改设置** | **打开Windows设置并开启暗黑模式** |  
| **提取数据** | **读取Chrome中Bloomberg标签页显示的股票价格** |  
| **复杂操作** | **打开YouTube，搜索“Adele Hello”，并播放第一个视频结果** |  
| **验证结果** | **在Chrome中查看Vercel控制台以确认部署是否成功** |  
| **发送邮件** | **打开Gmail，撰写邮件内容：主题“明天会议，内容：确认下午2点的会议时间”** |  
| **截图** | **截取屏幕截图** |  

## 错误处理：  
| 问题 | 解决方案 |  
|---------|----------|----|  
| 连接失败（端口3847） | 启动Clawd Cursor：`cd clawd-cursor && npm start` |  
| 连接失败（端口9222） | 通过CDP启动Chrome：`Start-Process chrome -ArgumentList "--remote-debugging-port=9222"` |  
| 代理提示“忙碌” | 查询`/status`状态；如果仍忙碌，发送`POST /abort`中止任务 |  
| 任务失败但无详细信息 | 查看`/logs`日志中的错误信息 |  
| 任务完成但结果错误** | 重新描述任务细节（包括应用程序名称、按钮文本、字段名称） |  
| 同一任务反复失败** | 将任务拆分为更小的部分（每个操作单独处理） |  
| 需要用户确认** | 发送`POST /confirm`请求，带上`{"approved": true`或`{"approved": false}`作为参数 |  
| 任务卡顿超过60秒** | 发送`POST /abort`后重新尝试，或调整任务描述 |  

## 工作原理（五层处理流程）  
| 层次 | 功能 | 执行速度 | 成本 |  
|-------|------|------|------|  
| **0层：浏览器层** | URL检测 → 直接导航 | 即时 | 无额外成本 |  
| **1层：动作路由与快捷键** | 正则表达式匹配 + UI自动化 + 键盘快捷键 | 即时 | 无额外成本 |  
| **1.5层：智能交互** | 语言模型（LLM）生成执行计划 → CDP/UIDriver执行 | 约2-5秒 | 需要一次LLM调用 |  
| **2层：辅助决策层** | UI结构分析 → 语言模型判断 | 约1秒 | 成本较低 |  
| **3层：计算机执行层** | 截图获取 → 视觉识别模型处理 | 约5-8秒 | 成本较高 |  

**注**：第1层（键盘快捷键）可以处理80%以上的任务，且无需调用LLM。视觉识别模型仅作为最后手段使用。  

## 安全等级  
| 等级 | 可执行的操作 | 行为规则 |  
|------|---------|----------|----|  
| 🟢 自动操作** | 导航、阅读、打开应用程序 | 立即执行 |  
| 🟡 预览操作** | 输入文本、填写表单 | 执行前会先记录操作日志 |  
| 🔴 需要确认的操作** | 发送消息、删除数据 | 执行前会询问用户确认 |  

## 安全性与隐私保护：  
- **网络隔离**：API仅绑定到`127.0.0.1`端口，无法从外部网络访问。  
- 截图仅保存在内存中，不会保存到磁盘（除非特别设置）。  
- 无数据传输，无分析日志，也不会发送任何数据到第三方。  
- **数据流向**：使用Ollama时完全离线处理，不涉及外部网络调用；使用云服务时，截图/文本仅发送到用户指定的服务器。  
- 用户可以控制数据流向（选择合适的云服务提供商）。  
- **代理自主控制**：自动操作（导航、阅读、打开应用程序）无需用户确认；需要确认的操作（发送消息、删除数据）会先询问用户。  

## 设置说明（用户操作指南）  
设置由用户完成。如果Clawd Cursor未运行，请手动使用相应命令启动它：  
```powershell
Start-Process -FilePath "node" -ArgumentList "dist/index.js","start" -WorkingDirectory "<skill-directory>" -WindowStyle Hidden
```  
只有在无法启动Clawd Cursor时（例如Node.js未安装或构建文件缺失）才询问用户。  
**macOS用户**：需在系统设置中启用“辅助功能”权限：**系统设置 → 隐私与安全 → 辅助功能**。  

| 提供商 | 设置方法 | 成本 |  
|----------|-------|------|  
| **Ollama（免费）** | `ollama pull <model>` | 无需额外费用（完全离线使用） |  
| **任何云服务提供商** | 设置`AI_API_KEY=your-key` | 成本因提供商而异 |  
| **OpenClaw用户** | 自动配置，无需额外设置 | 使用系统默认的云服务提供商 |  

## 性能优化  
已采取多种优化措施来降低任务执行时间和LLM API调用成本。详细信息见`perf/references/patches/`文件。  

### 优化措施示例：  
| 编号 | 优化内容 | 影响效果 |  
|------|------|--------|  
| 1 | 截图缓存** | 静态页面时减少90%的LLM调用次数 |  
| 2 | 并行处理截图和A11y模型** | 每步操作延迟减少30-40% |  
| 3 | A11y模型上下文缓存** | 减少不必要的进程启动 |  
| 4 | 截图压缩** | 削减数据大小（从120KB降至58KB） |  
| 5 | 异步调试** | 减少事件循环阻塞时间 |  
| 6 | 流式处理LLM响应** | 每次LLM调用响应时间缩短1-3秒 |  
| 7 | 简化系统提示信息** | 减少提示信息的显示次数 |  
| 8 | A11y模型过滤** | 仅显示交互式元素，限制字符长度 |  
| 9 | 合并脚本执行** | 减少进程启动次数 |  
| 10 | 任务栏缓存** | 快速处理任务栏相关操作 |  
| 11 | 延迟优化** | 总延迟减少50-150毫秒 |  

### 性能测试结果（分辨率2560x1440）  
| 测试指标 | v0.3（VNC） | v0.4（原生版本） | v0.4.1（优化版本） |  
|--------|------------|---------------|----------------------|  
| 截图获取时间 | 约850毫秒 | 约50毫秒 | 约57毫秒 |  
| 截图大小 | 约200KB | 约120KB | 约58KB |  
| A11y模型处理时间（未缓存） | 不适用 | 约600毫秒 | 约462毫秒 |  
| A11y模型处理时间（缓存后） | 不适用 | 0毫秒 | 2秒延迟 |  
| 每步操作延迟 | 不适用 | 200-1500毫秒 | 50-600毫秒 |  
| 系统提示信息显示时间 | 不适用 | 约800毫秒 | 约300毫秒 |  
| 性能优化工具**：`perf/apply-optimizations.ps1`用于应用所有优化措施；`perf/perf-test.ts`用于性能测试 |