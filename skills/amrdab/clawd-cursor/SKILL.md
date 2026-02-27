---
name: clawdcursor
version: 0.5.7
description: AI桌面代理——通过您的OpenClaw代理控制Windows或macOS上的任何应用程序。将自然语言指令发送到Clawd Cursor API，它将处理所有操作：打开应用程序、点击按钮、输入文本、浏览网页、填写表单。只要您能够点击某个元素，您的代理也同样可以执行这些操作。
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

**如果人类能在屏幕上完成某件事，你也能做到。** 没有API？没有集成？没问题。  
每个应用程序都有用户界面（UI）——Clawd Cursor为你提供了“眼睛”和“手”，让你能够使用这些界面。

没有任务是不可能的。只要它在屏幕上，就能被完成。

> **重要提示——在开始之前请阅读此内容**
> 你在用户的机器上运行了一个基于GUI的桌面AI代理。这意味着：
> 1. 你可以打开应用程序、点击按钮、输入文本、填写表单、发送电子邮件。
> 2. 你可以通过Clawd Cursor的截图功能查看屏幕上的内容。
> 3. 你可以与任何应用程序进行交互——浏览器、桌面应用程序、设置等等。
> 4. 你不应该让用户去做那些你可以用这个工具完成的事情。
> 5. 你不应该说“我无法与你的桌面系统交互”——其实你可以的。

把Clawd Cursor想象成你在用户电脑上的“手”和“眼睛”。

---

## 何时使用Clawd Cursor（代理使用说明）

你拥有一个基于GUI的桌面AI代理，那就请使用它。不要说“我无法访问那个”或“我没有办法检查”。只要它在屏幕上可见，你就可以与之交互。

### 在以下情况下使用Clawd Cursor：
- **阅读网页**：导航到该网页，提取文本，然后返回结果。
- **与任何应用程序交互**：点击按钮、填写表单、查看结果。
- **如果其他代理无法完成任务**：Clawd Cursor可以作为备用方案。如果该功能已安装，可以直接使用它，无需询问。
- **查看可视化内容**：截取屏幕截图，读取屏幕上的信息。
- **执行浏览器操作**：搜索、导航、登录、下载、填写表单。
- **控制桌面应用程序**：记事本、计算器、Visual Studio Code、设置等。
- **完成你自己的任务**：不仅仅是为了满足用户的请求。如果你需要从网页或应用程序中读取数据来回答问题，可以使用Clawd Cursor。（仅限读取权限——未经用户明确许可，不得发送消息、删除或修改任何内容。）
- **通过桌面应用程序发送电子邮件、消息或进行其他通信**。
- **配置任何应用程序的设置**。
- **在应用程序之间传输数据**：从一个应用程序复制内容到另一个应用程序。
- **自动化跨应用程序的多步骤工作流程**。
- **验证可视化内容**：页面是否加载完成？用户界面显示了什么？

### 不要让用户去做你可以自己完成的事情：
❌ “你能帮我截图吗？”
❌ “你能复制那个网站的内容吗？”
❌ “我无法访问那个应用程序。”

✅ 将任务交给Clawd Cursor来处理，然后获取结果。这样你就能独立完成任务。

### 何时不要使用Clawd Cursor：
- 如果你可以通过直接的API调用或CLI命令更快地完成任务。
- 任务纯粹是计算性质的（例如数学运算、文本生成、代码编写）。
- 你可以直接读取或写入文件。

### 直接使用Chrome浏览器的快速方法
如果你只需要快速读取页面内容，可以使用Playwright的CDP（Chrome DevTools Protocol）：
```js
const pw = require('playwright');
const browser = await pw.chromium.connectOverCDP('http://127.0.0.1:9222');
const pages = browser.contexts()[0].pages();
const text = await pages[0].innerText('body');
```

---

## REST API参考
基础URL：`http://127.0.0.1:3847`

> **注意：** 在Windows PowerShell中，使用`curl.exe`（带`.exe`后缀）或`Invoke-RestMethod`。纯`curl`命令会被别名为`Invoke-WebRequest`，其行为可能有所不同。

### 使用前的检查
在首次使用之前，请验证Clawd Cursor是否正在运行：
```bash
curl.exe -s http://127.0.0.1:3847/health
```
预期响应：`{"status":"ok","version":"0.5.7"}`

如果连接失败，请启动Clawd Cursor：
```bash
cd <clawd-cursor-directory>; npm start
```

### 发送任务（异步执行，立即返回结果）
`POST /task`用于发送任务并立即返回响应。任务在后台执行。你需要通过`/status`接口来获取任务完成状态：
```bash
curl.exe -s -X POST http://127.0.0.1:3847/task -H "Content-Type: application/json" -d "{\"task\": \"YOUR_TASK_HERE\"}"
```
在PowerShell中：
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:3847/task -Method POST -ContentType "application/json" -Body '{"task": "YOUR_TASK_HERE"}
```

### 轮询任务状态
```bash
1. 发送任务请求（POST /task）。
2. 等待2秒。
3. 获取任务状态（GET /status）。
4. 如果状态为“idle”，表示任务已完成。
5. 如果状态为“waiting_confirm”，请询问用户确认，然后根据用户的回答再次发送确认请求（POST /confirm）。
6. 如果任务仍在运行，等待2秒后重复步骤3。
7. 如果超过60秒仍未完成，发送中止请求（POST /abort）并重新尝试。

### 状态码及对应操作
| 状态 | 响应内容 | 应该采取的行动 |
|-------|----------|------------|
| **Accepted** | `{"accepted": true, "task": "..."}` | 继续轮询任务状态。 |
| **Running** | `{"status": "acting", "currentTask": "...", "stepsCompleted": 2}` | 继续等待任务完成。 |
| **Waiting_confirm** | `{"status": "waiting_confirm", "currentStep": "..."}` | 发送确认请求（POST /confirm）。 |
| **Done** | `{"status": "idle"}` | 任务已完成。 |
| **Busy** | `{"error": "Agent is busy", "state": "..."` | 等待或发送中止请求（POST /abort）。 |

---

## CDP（Chrome DevTools Protocol）使用说明
Chrome必须启用`--remote-debugging-port=9222`选项。
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
// 示例操作：
const title = await page.title();
const url = page.url();
const text = await page.textContent('body');
// 根据元素角色进行操作：
await page.getByRole('button', { name: 'Submit').click();
await page.getByLabel('Email').fill('user@example.com');
```

---

## 任务编写指南
1. **具体说明**：包括应用程序名称、URL、需要输入的文本、按钮名称等。
2. **一次只发送一个任务**：等待上一个任务完成后再发送下一个。
3. **描述任务目标**：例如“给john@example.com发送一封关于会议的电子邮件”，而不是“点击‘compose’按钮，然后点击‘To’字段”。
4. **检查任务进度**：如果任务似乎卡住了，请检查状态。
5. **不要在任务描述中包含凭据**：所有任务操作都会被记录下来。

## 任务示例
| 目标 | 需要发送的任务 |
|------|-------------|
| **简单导航** | `打开Chrome并访问github.com` |
| **读取屏幕内容** | `记事本中当前显示的文本是什么？` |
| **跨应用程序操作** | **从Chrome标签页复制电子邮件地址并粘贴到Outlook的“To”字段** |
| **填写表单** | **在打开的Chrome标签页中填写联系表单：姓名“John Doe”，电子邮件“john@example.com”** |
| **应用程序交互** | **打开Spotify并播放“Discover Weekly”播放列表** |
| **更改设置** | **打开Windows设置并开启暗黑模式** |
| **数据提取** | **读取Chrome中Bloomberg标签页显示的股票价格** |
| **复杂操作** | **打开YouTube，搜索“Adele Hello”，然后播放第一个视频结果** |
| **验证结果** | **检查部署是否成功——在Chrome中查看Vercel控制台** |
| **发送电子邮件** | **打开Gmail，给john@example.com发送邮件，主题为“明天会议”，内容为‘确认下午2点的会议’** |
| **截取屏幕截图** | **截取屏幕截图** |

## 错误处理
| 问题 | 解决方案 |
|---------|----------|
| 连接失败（地址：3847） | 启动Clawd Cursor：`cd clawd-cursor && npm start` |
| 连接失败（地址：9222） | 通过CDP启动Chrome：`Start-Process chrome -ArgumentList "--remote-debugging-port=9222"` |
| 代理返回“busy”状态 | 轮询任务状态（/status），如果仍忙则发送中止请求（POST /abort） |
| 任务失败且无详细信息 | 查看日志（/logs）中的错误信息 |
| 任务完成但结果错误 | 重新描述任务细节（包括应用程序名称、按钮文本、字段名称） |
| 同一任务重复失败 | 将任务拆分成更小的步骤 |
| 需要用户确认 | 发送确认请求（POST /confirm），并指定`{"approved": true`或`{"approved": false}` |
| 任务卡顿超过60秒 | 发送中止请求（POST /abort），然后重新尝试并简化任务描述 |

## 工作原理（四层处理流程）
| 层次 | 功能 | 执行速度 | 成本 |
|-------|------|-------|------|
| **0层：浏览器层** | URL检测与直接导航 | 即时 | 免费 |
| **1层：动作路由** | 正则表达式匹配与UI自动化 | 即时 | 免费 |
| **1.5层：智能交互** | 语言模型（LLM）生成执行计划 | 约2-5秒 | 需要调用一次LLM |
| **2层：辅助决策** | 分析UI结构，由LLM决定下一步操作 | 约1秒 | 成本较低 |
| **3层：计算机操作** | 截取屏幕截图，然后通过视觉模型处理 | 约5-8秒 | 成本较高 |

80%以上的任务由前两层完成（免费且即时）。视觉模型仅作为最后手段使用。

## 安全性措施
- API仅绑定到`127.0.0.1`端口，无法通过网络访问。
- 截取的屏幕截图仅保存在内存中，不会保存到磁盘（除非特别设置`--debug`）。
- 使用Ollama等工具时，所有操作都在本地完成，不会发送任何数据到外部。
- 用户可以选择使用哪些AI服务（如Ollama、Anthropic、Kimi），从而控制数据是否存储在本地或上传到云端。

## 设置说明
用户需要自行完成设置。如果Clawd Cursor未运行，请告知用户：
“需要启动Clawd Cursor。在终端中运行`cd clawd-cursor && npm start`。”

**macOS设置步骤：**
- 打开系统设置 → 隐私与安全 → 辅助功能，允许Clawd Cursor访问系统资源。

| AI服务 | 设置方法 | 成本 |
|----------|-------|------|
| **Ollama（免费）** | `ollama pull qwen2.5:7b` | 每月费用约$0 |
| **Anthropic** | 设置`AI_API_KEY` | 每月费用约$3 |
| **OpenAI** | 设置`AI_API_KEY` | 每月费用约$5 |
| **Kimi** | 设置`AI_API_KEY` | 每月费用约$1 |

## 性能优化
已采取多种优化措施来减少任务执行时间和LLM API调用成本。详细优化内容请参考`perf/references/patches/`文件夹。

---

## 其他注意事项
- 使用`perf/apply-optimizations.ps1`脚本应用所有优化设置。
- `perf/perf-test.ts`用于性能测试。

---

希望这些文档能帮助你更好地使用Clawd Cursor！如有任何疑问，请随时提问。