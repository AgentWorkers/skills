---
name: vibesurf
description: 当用户请求浏览网站、自动化浏览器操作、填写表单、提取网页数据、搜索网络信息或与外部应用程序交互时，请使用此功能。这是主要的入口点，它会引导用户查阅详细的参考指南。
homepage: https://github.com/vibesurf-ai/VibeSurf
metadata:
  moltbot:
    requires:
      env: ["VIBESURF_ENDPOINT"]
    primaryEnv: "VIBESURF_ENDPOINT"
---

# VibeSurf - 浏览器自动化

通过 VibeSurf 控制真实的浏览器。有关详细的使用方法，请参阅相应的参考指南。

> **🚨 VIBESURF 状态**
>
> 检查 VibeSurf 是否正在运行：
> ```bash
> curl $VIBESURF_ENDPOINT/health
> ```
> - ✅ **HTTP 200** → 可以继续使用 VibeSurf 的功能
> - ❌ **连接被拒绝** → 请用户运行 `vibesurf`（切勿自行运行该命令）
>
> 默认端点：`http://127.0.0.1:9335`

## 如何调用 VibeSurf API

VibeSurf 提供了三个核心的 HTTP 端点：

### 1. 列出可用操作
```bash
GET $VIBESURF_ENDPOINT/api/tool/search?keyword={optional_keyword}
```
返回所有可用的 VibeSurf 操作。

### 2. 获取操作参数
```bash
GET $VIBESURF_ENDPOINT/api/tool/{action_name}/params
```
返回该操作的参数 JSON 架构。

### 3. 执行操作
```bash
POST $VIBESURF_ENDPOINT/api/tool/execute
Content-Type: application/json

{
  "action_name": "action_name_here",
  "parameters": {
    // action-specific parameters
  }
}
```

**工作流程：**
1. 查找所需操作 → 获取操作名称
2. 获取参数架构 → 查看必填/可选参数
3. 执行操作 → 使用参数调用相应功能

> **⚠️ 参数错误处理**
>
> 如果对参数不确定，请在执行任何操作之前务必先调用 `GET /api/tool/{action_name}/params`。

---

## 需要查阅的参考文档

| 任务类型 | 参考文档 | 操作名称 |
|-----------|----------------|-------------|
| AI 网页搜索 | [references/search.md](references/search.md) | `skill_search` |
| 从 URL 获取内容（以 Markdown 格式） | [references/fetch.md](references/fetch.md) | `skill_fetch` |
| 提取列表/表格 | [references/js_code.md](references/js_code.md) | `skill_code` |
| 提取页面内容 | [references/crawl.md](references/crawl.md) | `skill_crawl` |
| 页面摘要 | [references/summary.md](references/summary.md) | `skill_summary` |
| 股票/金融数据 | [references/finance.md](references/finance.md) | `skill_finance` |
| 热门新闻 | [references/trend.md](references/trend.md) | `skill_trend` |
| 截图 | [references/screenshot.md](references/screenshot.md) | `skill_screenshot` |
| 精确的浏览器控制 | [references/browser.md](references/browser.md) | `browser.*` 操作 |
| 任务导向的自动化（子代理） | [references/browser-use.md](references/browser-use.md) | `execute_browser_use_agent` |
| 社交媒体平台 API | [references/website-api.md](references/website-api.md) | `call_website_api` |
| 预构建的工作流程 | [references/workflows.md](references/workflows.md) | `execute_workflow` |
| Gmail/GitHub/Slack | [references/integrations.md](references/integrations.md) | `execute_extra_tool` |
| LLM 配置文件 | [references/config-llm.md](references/config-llm.md) | `/api/config/llm-profiles/*` |
| MCP 服务器配置 | [references/config-mcp.md](references/config-mcp.md) | `/api/config/mcp-profiles/*` |
| VibeSurf 密钥/工作流程 | [references/config-vibesurf.md](references/config-vibesurf.md) | `/api/vibesurf/*` |
| Composio 工具包 | [references/config-composio.md](references/config-composio.md) | `/api/composio/*` |
| 安排工作流程 | [references/config-schedule.md](references/config-schedule.md) | `/api/schedule/*` |
| 文件上传/下载 | [references/file.md](references/file.md) | `/api/files/*` |
| 语音/自动语音识别（ASR）配置 | [references/config-voice.md](references/config-voice.md) | `/api/voices/*` |

---

## 配置参考

| 配置任务 | 参考文档 | 使用场景 |
|-------------|-----------|-------------|
| 添加/切换 LLM | [references/config-llm.md](references/config-llm.md) | 管理 AI 模型配置（如 OpenAI、Anthropic 等） |
| 添加 MCP 服务器 | [references/config-mcp.md](references/config-mcp.md) | 配置 MCP 以集成其他工具 |
| VibeSurf API 密钥 | [references/config-vibesurf.md](references/config-vibesurf.md) | 设置 API 密钥，导入/导出工作流程 |
| 启用 Gmail/GitHub 等功能 | [references/config-composio.md](references/config-composio.md) | 配置 Composio 工具包和 OAuth |
| 安排工作流程 | [references/config-schedule.md](references/config-schedule.md) | 设置基于 Cron 的自动化任务 |
| 语音/ASR 配置 | [references/config-voice.md](references/config-voice.md) | 配置语音识别设置 |

**注意：** 配置完 Composio 或 MCP 工具后，可通过 [references/integrations.md](references/integrations.md) 使用它们（工具名称格式为：`cpo.{toolkit}.{action}` 或 `mcp.{server}.{action}`）。

---

## 决策流程

```
Browser/Web Task
│
├─ Need to search for information/bug/issue? → Read [references/search.md](references/search.md) [PREFERRED]
│  Examples: "Search for solutions to [bug name]", "Find latest info about [topic]"
│
├─ Need to fetch URL content directly? → Read [references/fetch.md](references/fetch.md)
│  Examples: "Fetch content from [URL]", "Get documentation at [URL]", "Read this webpage"
│
├─ Need to open website? → Read [references/browser.md](references/browser.md)
│  Examples: "Open documentation site", "Go to [URL]", "Check this page"
│
├─ Need to extract data?
│  ├─ Lists/tables/repeated items? → Read [references/js_code.md](references/js_code.md)
│  └─ Main content? → Read [references/crawl.md](references/crawl.md)
│
├─ Need summary? → Read [references/summary.md](references/summary.md)
│
├─ Stock/finance data? → Read [references/finance.md](references/finance.md)
│
├─ Trending news? → Read [references/trend.md](references/trend.md)
│
├─ Screenshot? → Read [references/screenshot.md](references/screenshot.md)
│
├─ Need precise control or step-by-step operations? → Read [references/browser.md](references/browser.md)
│  Examples: "Click the button", "Type in the field", "Scroll down"
│
├─ Complex task-oriented automation? → Read [references/browser-use.md](references/browser-use.md)
│  Examples: "Fill out this form", "Extract data from multiple pages"
│
├─ Platform API (XiaoHongShu/Youtube/etc)? → Read [references/website-api.md](references/website-api.md)
│
├─ External app (Gmail/Google Calendar/GitHub)? → Read [references/integrations.md](references/integrations.md)
│
├─ Pre-built workflow? → Read [references/workflows.md](references/workflows.md)
│
└─ Need to configure LLM/MCP/VibeSurf/Composio/Schedule/Voice? → Read config-* references
   - LLM profiles → [references/config-llm.md](references/config-llm.md)
   - MCP servers → [references/config-mcp.md](references/config-mcp.md)
   - VibeSurf key/workflows → [references/config-vibesurf.md](references/config-vibesurf.md)
   - Composio key/toolkits → [references/config-composio.md](references/config-composio.md)
   - Schedule workflows → [references/config-schedule.md](references/config-schedule.md)
   - Voice/ASR profiles → [references/config-voice.md](references/config-voice.md)
```

---

## 快速参考

| 目标 | 参考文档 | 操作 |
|------|----------------|--------|
| 搜索网页 | [references/search.md](references/search.md) | `skill_search` |
| 从 URL 获取内容 | [references/fetch.md](references/fetch.md) | `skill_fetch` |
| 提取价格/产品信息 | [references/js_code.md](references/js_code.md) | `skill_code` |
| 提取页面主要内容 | [references/crawl.md](references/crawl.md) | `skill_crawl` |
| 页面摘要 | [references/summary.md](references/summary.md) | `skill_summary` |
| 股票数据 | [references/finance.md](references/finance.md) | `skill_finance` |
| 热门话题 | [references/trend.md](references/trend.md) | `skill_trend` |
| 截图 | [references/screenshot.md](references/screenshot.md) | `skill_screenshot` |
| 点击/导航/输入 | [references/browser.md](references/browser.md) | `browser.click`, `browser.navigate` 等 |
| 任务导向的自动化 | [references/browser-use.md](references/browser-use.md) | `execute_browser_use_agent` |
| 社交媒体平台 API | [references/website-api.md](references/website-api.md) | `call_website_api` |
| 发送邮件 | [references/integrations.md](references/integrations.md) | `execute_extra_tool` |
| 运行工作流程 | [references/workflows.md](references/workflows.md) | `execute_workflow` |
| 配置 LLM 配置文件 | [references/config-llm.md](references/config-llm.md) | `/api/config/llm-profiles/*` |
| 配置 MCP 服务器 | [references/config-mcp.md](references/config-mcp.md) | `/api/config/mcp-profiles/*` |
| 配置 VibeSurf 密钥 | [references/config-vibesurf.md](references/config-vibesurf.md) | `/api/vibesurf/verify-key` |
| 启用 Composio 工具包 | [references/config-composio.md](references/config-composio.md) | `/api/composio/toolkits` |
| 安排工作流程 | [references/config-schedule.md](references/config-schedule.md) | `/api/schedule/*` |
| 上传/下载文件 | [references/file.md](references/file.md) | `/api/files/*` |
| 配置语音/ASR | [references/config-voice.md](references/config-voice.md) | `/api/voices/*` |

---

## 常见请求模式

| 请求 | 参考文档 | 操作 |
|---------|----------------|--------|
| “搜索 X” | [references/search.md](references/search.md) | `skill_search` |
| “从 [URL] 获取内容” | [references/fetch.md](references/fetch.md) | `skill_fetch` |
| “提取所有价格” | [references/js_code.md](references/js_code.md) | `skill_code` |
| “总结页面内容” | [references/summary.md](references/summary.md) | `skill_summary` |
| “获取 AAPL 的股票信息” | [references/finance.md](references/finance.md) | `skill_finance` |
| “当前热门话题是什么” | [references/trend.md](references/trend.md) | `skill_trend` |
| “截图” | [references/screenshot.md](references/screenshot.md) | `skill_screenshot` |
| “导航并点击” | [references/browser.md](references/browser.md) | `browser.navigate`, `browser.click` |
| “填写表单” | [references/browser-use.md](references/browser-use.md) 或 [references/browser.md](references/browser.md) | `execute_browser_use_agent` 或手动操作 |
| “获取小红书帖子” | [references/website-api.md](references/website-api.md) | `call_website_api` |
| “发送邮件” | [references/integrations.md](references/integrations.md) | `execute_extra_tool` |
| “运行视频下载” | [references/workflows.md](references/workflows.md) | `execute_workflow` |
| “配置 LLM” | [references/config-llm.md](references/config-llm.md) | `/api/config/llm-profiles` |
| “添加 MCP 服务器” | [references/config-mcp.md](references/config-mcp.md) | `/api/config/mcp-profiles` |
| “设置 VibeSurf API 密钥” | [references/config-vibesurf.md](references/config-vibesurf.md) | `/api/vibesurf/verify-key` |
| “启用 Gmail/GitHub” | [references/config-composio.md](references/config-composio.md) | `/api/composio/toolkits` |
| “安排工作流程” | [references/config-schedule.md](references/config-schedule.md) | `/api/schedule/*` |
| “上传/下载文件” | [references/file.md](references/file.md) | `/api/files/*` |
| “配置语音/ASR” | [references/config-voice.md](references/config-voice.md) | `/api/voices/*` |
| “将语音转换为文本” | [references/config-voice.md](references/config-voice.md) | `/api/voices/asr` |

---

## 错误处理

| 错误 | 解决方案 |
|-------|----------|
| VibeSurf 未运行 | **检查状态：** `curl $VIBESURF_ENDPOINT/health`<br>**如果未运行**：通知用户运行 `vibesurf`<br>**切勿**自行运行该命令 |
| 不知道该参考文档在哪里 | 查阅上面的决策流程表 |
| 操作未找到 | 调用 `GET /api/tool/search` 以列出所有可用操作 |
| 参数错误 | 调用 `GET /api/tool/{action_name}/params` 以查看参数架构 |
| `browser-use` 失败或卡住 | 回退到 [references/browser.md](references/browser.md)：使用 `get_browser_state` → `browser.{action}` → 重复尝试 |
| LLM/爬取/摘要功能出错 | **原因**：未配置 LLM 配置文件<br>**解决方案**：先阅读 [references/config-llm.md](references/config-llm.md) 以添加 LLM 配置 |
| 集成工具未找到 | **原因**：Composio/MCP 未配置<br>**解决方案**：先阅读 [references/config-composio.md](references/config-composio.md) 或 [references/config-mcp.md] 以启用相关工具 |

---

## 获取浏览器状态

> **🔍 检查当前浏览器状态**
>
> 当用户询问当前页面内容或浏览器状态时（例如：“当前页面显示什么？”，“打开了哪些标签页？”，“浏览器显示的是什么？”），请查阅 [references/browser.md](references/browser.md) 并使用 `get_browser_state` 操作。
>
> 当您不清楚用户当前在浏览器中查看的内容时，此功能非常有用。

---

## `browser` 与 `browser-use` 的区别

**两者都可以完成相同的浏览器任务——它们是互补的：**

| 方法 | 适用场景 | 工作原理 |
|----------|----------|--------------|
| **browser-use** ([references/browser-use.md](references/browser-use.md)) | 复杂、耗时的任务 | 任务导向的子代理：描述目标及期望结果，代理会自动确定操作步骤 |
| **browser** ([references/browser.md](references/browser.md)) | 精确的控制 | 逐步手动控制：每个操作都清晰可见 |
| **混合使用** | 最具可靠性 | 先尝试使用 `browser-use`，如果失败则切换到 `browser` |

**当 `browser-use` 失败时的回退方案：**
```
browser-use fails or gets stuck
→ Read references/browser.md
→ get_browser_state (inspect page)
→ browser.{action} (perform action)
→ get_browser_state (verify & plan next)
→ repeat until complete
```

---

## 资源

- **GitHub**: https://github.com/vibesurf-ai/VibeSurf
- **参考文档**：详细指南请参见 `references/` 文件夹

---

## API 参数故障排除

如果在调用 VibeSurf 端点时遇到参数错误，可以访问交互式的 API 文档：

```
http://127.0.0.1:9335/docs
```

例如：`http://127.0.0.1:9335/docs#/config/create_mcp_profile_api_config_mcp_profiles_post`

> **注意：** 这是一种 **备用** 方法。在大多数情况下，阅读相应的 `references/*.md` 文件（例如 [references/config-mcp.md](references/config-mcp.md)）应该能提供足够的指导。只有当技能文档无法解决问题或需要检查特定的请求/响应架构时，才需要参考 `/docs` 端点。