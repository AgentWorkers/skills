---
name: clawd-cursor
version: 0.5.4
description: AI桌面代理——通过您的OpenClaw代理控制Windows或macOS上的任何应用程序。将自然语言指令发送到Clawd Cursor API，它会处理所有操作：打开应用程序、点击按钮、输入文本、浏览网页、填写表单。只要您能点击某个元素，您的代理也能执行相应的操作。
homepage: https://clawdcursor.com
source: https://github.com/AmrDab/clawd-cursor
privacy: >
  Screenshots and UI data stay on the user's machine. If using Ollama (local), zero data leaves the host.
  If using a cloud provider (Anthropic, OpenAI, Kimi), screenshots/text are sent to that provider's API
  only — never to third-party servers or skill authors. The user controls which provider is used.
  The REST API binds to 127.0.0.1 only and is not network-accessible.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
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
credentials:
  - name: AI_API_KEY
    sensitivity: high
    description: API key for AI provider (Anthropic, OpenAI, or Kimi). Not needed if using Ollama locally.
    required: false
---
# Clawd Cursor

**如果人类能在屏幕上完成某项操作，你也能做到。** 没有API？没有集成？没问题。  
每个应用程序都有用户界面（UI）——Clawd Cursor为你提供了“眼睛”和“手”，让你能够使用这些界面。

没有任务是不可能的。只要它在屏幕上显示，就能被你操作。

> **重要提示 — 在使用之前请阅读此内容**

> 你的用户机器上运行着一个基于GUI的桌面AI代理。这意味着：
> 1. 你可以打开应用程序、点击按钮、输入文本、填写表单、发送邮件。
> 2. 你可以通过Clawd Cursor的截图功能查看屏幕上的内容。
> 3. 你可以与任何应用程序进行交互——浏览器、桌面应用程序、设置等等。
> 4. 你不应该让用户去做那些你可以用这个工具完成的事情。
> 5. 你不应该说“我无法与你的桌面系统交互”——其实你可以的。

可以把Clawd Cursor想象成你在用户电脑上的“手”和“眼睛”。

---

## 何时使用Clawd Cursor（代理使用说明）

你有一个基于GUI的桌面AI代理可以使用。**就用它吧**。不要说“我无法访问那个”或“我没有办法查看”。只要它在屏幕上显示，你就可以与之交互。

### 在以下情况下使用Clawd Cursor：
- **阅读网页**：导航到该网页，提取文本。
- **与任何应用程序交互**：点击按钮、填写表单、查看结果。
- **查看可视化内容**：截取屏幕截图，读取屏幕上的信息。
- **执行浏览器操作**：搜索、导航、登录、下载、填写表单。
- **控制桌面应用程序**：记事本、计算器、VS Code、设置等。
- **完成你自己的任务**：不仅仅是响应用户请求。如果你需要从网页或应用程序中获取数据来回答问题，可以使用Clawd Cursor。
- **通过桌面应用程序发送邮件、消息或进行其他通信**。
- **配置任何应用程序的设置**。
- **在应用程序之间传输数据**：从一个应用程序复制数据到另一个应用程序。
- **自动化跨应用程序的多步骤工作流程**。
- **验证可视化内容**：页面是否加载完成？用户界面显示了什么？

### 不要让用户去做你可以自己完成的事情。
❌ “你能帮我截取那个页面的截图吗？”
❌ “你能复制那个网站的内容吗？”
❌ “我无法访问那个应用程序。”

✅ 将任务发送给Clawd Cursor，然后获取结果。这样你就独立完成了任务。

### 在以下情况下不要使用Clawd Cursor：
- 如果你可以通过直接的API调用或CLI命令来完成任务（速度更快）。
- 任务纯粹是计算性质的（例如数学计算、文本生成、代码编写）。
- 你可以直接读取或写入文件。

### 直接使用Chrome的CDP（快速途径）

如果你只需要快速读取页面内容，可以使用Playwright的CDP功能：
```js
const pw = require('playwright');
const browser = await pw.chromium.connectOverCDP('http://127.0.0.1:9222');
const pages = browser.contexts()[0].pages();
const text = await pages[0].innerText('body');
```

---

## REST API参考

基础URL：`http://127.0.0.1:3847`

> **注意：** 在Windows PowerShell中，使用`curl.exe`（带`.exe`后缀）或`Invoke-RestMethod`。裸露的`curl`命令会被别名为`Invoke-WebRequest`，其行为可能有所不同。

### 预检

在开始第一个任务之前，请验证Clawd Cursor是否正在运行：
```bash
curl.exe -s http://127.0.0.1:3847/health
```
预期响应：`{"status":"ok","version":"0.5.4"}`

如果连接失败，请启动Clawd Cursor：
```bash
cd <clawd-cursor-directory>; npm start
```

### 发送任务（异步执行 — 立即返回结果）

`POST /task`用于发送任务，并立即返回响应。任务会在后台执行。**你需要通过`/status`接口来获取任务完成状态**：
```bash
curl.exe -s -X POST http://127.0.0.1:3847/task -H "Content-Type: application/json" -d "{\"task\": \"YOUR_TASK_HERE\"}"
```
在PowerShell中：
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:3847/task -Method POST -ContentType "application/json" -Body '{"task": "YOUR_TASK_HERE"}
```

### 轮询状态

```bash
1. 发送任务 → 等待响应。
2. 等待2秒。
3. 获取任务状态（`/status`接口）。
4. 如果状态为“idle”，则任务已完成。
5. 如果状态为“waiting_confirm”，则发送`/confirm`请求（内容为`{"approved": true}`）。
6. 如果任务仍在运行，等待2秒后再次尝试。
7. 如果超过60秒仍未完成，发送`/abort`请求并重新尝试。

### 检查状态

```bash
curl.exe -s http://127.0.0.1:3847/status
```

### 确认需要审批的操作

某些操作（如发送消息、删除数据）需要用户确认：
```bash
curl.exe -s -X POST http://127.0.0.1:3847/confirm -H "Content-Type: application/json" -d "{\"approved\": true}"
```

### 中断任务

```bash
curl.exe -s -X POST http://127.0.0.1:3847/abort
```

### 查看日志（用于调试）

```bash
curl.exe -s http://127.0.0.1:3847/logs
```
该命令会返回最近的200条日志记录。如果任务失败，请检查日志中是否有错误或警告信息。

### 响应状态及对应操作

| 状态 | 响应内容 | 应该采取的措施 |
|-------|----------|------------|
| **Accepted** | `{"accepted": true, "task": "..."}` | 继续轮询任务状态。 |
| **Running** | `{"status": "acting", "currentTask": "...", "stepsCompleted": 2}` | 继续轮询。 |
| **Waiting-confirm** | `{"status": "waiting_confirm", "currentStep": "..."}` | 发送`/confirm`请求以确认操作。 |
| **Done** | `{"status": "idle"}` | 任务已完成。 |
| **Busy** | `{"error": "Agent is busy", "state": "...}` | 等待或发送`/abort`请求中断任务。 |

---

## CDP直接使用说明

Chrome必须开启`--remote-debugging-port=9222`选项才能使用CDP功能。

### 快速检查：
```bash
curl.exe -s http://127.0.0.1:9222/json/version
```
如果返回JSON数据，说明Chrome已准备好使用CDP。

### 通过Playwright连接：

```javascript
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const context = browser.contexts()[0];
const page = context.pages()[0];

// 获取页面内容
const title = await page.title();
const url = page.url();
const text = await page.textContent('body');

// 根据角色点击按钮
await page.getByRole('button', { name: 'Submit').click();

// 填写表单字段
await page.getByLabel('Email').fill('user@example.com');

// 获取页面元素
const buttons = await page.$$eval('button', els => els.map(e => e.textContent);
```

---

## 任务编写指南

1. **具体说明**：包括应用程序名称、URL、需要输入的文本、按钮名称等。
2. **一次只发送一个任务**：等待上一个任务完成后再发送下一个。
3. **描述任务目标，而不是具体的操作步骤**。例如，应该说“给john@example.com发送一封关于会议的邮件”，而不是“点击‘compose’按钮，然后点击‘To’字段”。
4. **检查任务状态**：如果任务似乎卡住了，请检查进度。
5. **不要在任务描述中包含敏感信息**：所有操作都会被记录下来。

## 任务示例

| 目标 | 需要执行的操作 |
|------|-------------|
| **简单导航** | 打开Chrome并访问github.com |
| **读取屏幕内容** | “记事本中当前显示的文本是什么？” |
| **跨应用程序操作** | 从Chrome标签页复制电子邮件地址并粘贴到Outlook的“To”字段 |
| **填写表单** | 在打开的Chrome标签页中，填写联系表单：姓名“John Doe”，电子邮件“john@example.com” |
| **与应用程序交互** | 打开Spotify并播放“Discover Weekly”播放列表 |
| **更改设置** | 打开Windows设置并开启暗黑模式 |
| **提取数据** | 读取Chrome中Bloomberg标签页显示的股票价格 |
| **复杂操作** | 打开YouTube，搜索“Adele Hello”，并播放第一个搜索结果 |
| **验证操作** | 在Chrome中查看Vercel仪表板以确认部署是否成功 |
| **发送邮件** | 打开Gmail，给john@example.com发送邮件，主题为“明天会议”，内容为“确认下午2点的会议” |
| **截取屏幕截图** | 截取屏幕截图 |

## 错误处理

| 问题 | 解决方案 |
|---------|----------|
| 连接失败（地址：3847） | 启动Clawd Cursor：`cd clawd-cursor && npm start` |
| 连接失败（地址：9222） | 使用CDP启动Chrome：`Start-Process chrome -ArgumentList "--remote-debugging-port=9222"` |
| 代理显示“busy”状态 | 轮询`/status`接口；如果状态仍为“busy”，则发送`/abort`请求 |
| 任务失败且没有详细信息 | 查看日志中的错误信息 |
| 任务完成但结果错误 | 重新描述任务细节（包括应用程序名称、按钮文本、字段名称等） |
| 同一任务反复失败 | 将任务拆分为多个小任务 |
| 需要确认操作 | 发送`/confirm`请求，内容为`{"approved": true}`或`{"approved": false}` |
| 任务超过60秒未完成 | 发送`/abort`请求，然后尝试重新发送任务，同时提供更详细的描述 |

---

## 工作原理（四层处理流程）

| 层次 | 功能 | 执行速度 | 成本 |
|-------|------|------|------|
| **0层：浏览器层** | URL检测和直接导航 | 即时 | 免费 |
| **1层：动作路由层** | 正则表达式匹配和UI自动化 | 即时 | 免费 |
| **1.5层：智能交互层** | 通过大型语言模型（LLM）生成操作计划，然后通过CDP/UIDriver执行 | 约2-5秒 | 需要调用一次LLM |
| **2层：辅助决策层** | 分析UI结构，由LLM决定下一步操作 | 约1秒 | 成本较低 |
| **3层：计算机执行层** | 截取屏幕截图，然后通过视觉模型处理 | 约5-8秒 | 成本较高 |

80%以上的任务可以通过前两层（免费且即时完成）。视觉模型仅在必要时使用。

## 安全性措施

- API仅绑定到`127.0.0.1`端口，无法通过网络访问。验证方法：`netstat -an | findstr 3847`应显示`127.0.0.1:3847`。
- 截取的屏幕截图仅保存在内存中，不会保存到磁盘（除非特别设置`--debug`）。
- 使用Ollama时，所有操作都在本地完成，不会发送任何网络请求。
- 即使使用Anthropic、OpenAI或Kimi等云服务，截图和文本数据也仅发送给相应的API，不会泄露给第三方。
- 用户可以自行选择使用哪些云服务，从而控制数据的使用方式（是否保存在本地或发送到云端）。

## 设置说明（用户操作）

设置由用户完成。如果Clawd Cursor未运行，请告知用户：
“需要启动Clawd Cursor。在终端中运行`cd clawd-cursor && npm start`。”

```bash
git clone https://github.com/AmrDab/clawd-cursor.git
cd clawd-cursor
npm install && npm run build
npx clawd-cursor doctor    # 自动检测并配置所有设置
npm start                  # 在端口3847上启动服务
```

**macOS用户：** 需要为终端设置访问权限：系统设置 → 隐私与安全 → 访问辅助功能。

| 服务提供商 | 设置方法 | 成本 |
|----------|-------|------|
| Ollama（免费） | `ollama pull qwen2.5:7b` | 每月费用$0 |
| Anthropic | 设置`AI_API_KEY=sk-ant-...` | 每月费用约$3 |
| OpenAI | 设置`AI_API_KEY=sk-...` | 每月费用约$5 |
| Kimi | 设置`AI_API_KEY=sk-...` | 每月费用约$1 |