---
name: local-deep-research
description: Multi-cycle deep research using locally-hosted LDR (Local Deep Research) service. Use when user asks for comprehensive research with citations, literature reviews, competitive intelligence, or any research requiring exhaustive web search with iterative question generation. Triggers on: "deep research", "research this topic", "comprehensive analysis with sources", "literature review", "investigate [topic]", "quick summary on [topic]", "detailed report on [topic]", "research in Spanish/French/etc", or when academic-deep-research is requested but using local LDR instance.
version: 1.0.2
homepage: https://github.com/eplt/local-deep-research-skill
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      bins:
        - curl
        - jq
      env:
        - LDR_BASE_URL
        - LDR_SERVICE_USER
        - LDR_SERVICE_PASSWORD
    primaryEnv: LDR_BASE_URL
    files:
      - "scripts/*"
      - "references/*"
---

# 本地深度研究技能

该技能通过与本地托管的LDR（Local Deep Research）服务进行交互，来执行多轮迭代研究，并提供完整的引用和来源追踪。

## 安装前需考虑的事项

- **LDR服务**：该脚本仅与`LDR_BASE_URL`（默认为`http://127.0.0.1:5000`）中的URL通信。请确保将其指向您控制的LDR实例，切勿指向未知或不可信的远程主机。
- **必备工具**：确保运行该技能的宿主上已安装`curl`和`jq`命令。
- **凭据**：如果您的LDR实例需要登录，请通过环境变量或本地`.env`文件设置`LDR_SERVICE_USER`和`LDR_SERVICE_PASSWORD`（或`LDR_USERNAME`/`LDR_PASSWORD`）。请使用专用的、权限较低的LDR账户（例如`openclaw_service`）。切勿将敏感信息存储在已提交的配置文件或技能目录中。
- **配置文件`.env`：如果存在`~/.config/local_deep_research/config/.env`文件，脚本会自动读取其中的配置。请确保该文件中不包含无关的敏感信息。
- **脚本审查**：该脚本使用基于表单的会话认证和CSRF保护机制进行登录，并使用临时cookie。它不会将数据发送到除配置的LDR服务之外的任何端点。在使用前，请查阅`scripts/ldr-research.sh`脚本的详细说明。为提高安全性，建议在仅允许访问LDR主机的隔离环境（如容器或虚拟机）中运行该脚本。

## 配置

### 凭据（仅限本地使用，不会被传输）

LDR使用带有CSRF保护的会话cookie认证机制（而非HTTP基本认证）。脚本会按照以下流程进行登录：首先访问登录页面，获取会话cookie和CSRF令牌，然后提交凭据并包含CSRF令牌，之后在所有API调用中重复使用该会话cookie和CSRF令牌。用户名和密码仅用于与本地LDR实例建立会话，绝不会被发送到ClawHub、GitHub或其他服务器。

**注意**：切勿将凭据放入技能的配置文件或已提交的代码中。请仅使用环境变量或本地`.env`文件来存储凭据（例如`LDR_SERVICE_USER`、`LDR_SERVICE_PASSWORD`或`LDR_USERNAME`/`LDR_PASSWORD`）。如果存在`~/.config/local_deep_research/config/.env`文件，脚本会自动读取其中的配置。建议为该技能使用专用的LDR账户（例如`openclaw_service`）。

### 所有配置选项

- `LDR_BASE_URL` — LDR服务URL（默认：`http://127.0.0.1:5000`）
- `LDR_LOGIN_URL` — 用于会话认证和CSRF保护的登录页面URL（默认：`$LDR_BASE_URL/auth/login`）
- `LDR_SERVICE_USER` 或 `LDR_USERNAME` — LDR账户用户名（仅限本地认证）
- `LDR_SERVICE_PASSWORD` 或 `LDR_PASSWORD` — LDR账户密码（仅限本地认证）
- `LDR_DEFAULT_MODE` — 默认研究模式：`quick`（快速摘要）或`detailed`（详细报告）（默认：`detailed`）
- `LDR_DEFAULT_LANGUAGE` — 报告/摘要的默认输出语言代码（例如`en`、`es`、`fr`、`de`、`zh`、`ja`）；为空表示使用LDR的默认语言
- `LDR_DEFAULT_SEARCH_tool` — 默认搜索工具：`searxng`、`auto`、`local_all`（默认：`auto`）

## 研究模式（快速摘要 vs 详细报告）

- **`quick`** — **快速摘要**：研究周期较少，输出内容简短，速度较快。适用于用户需要简洁总结或快速了解情况的情况。
- **`detailed`** — **详细报告**：进行多轮完整研究，生成包含完整引用和来源的Markdown格式报告。适用于用户需要全面分析、文献回顾或深入研究的情况。

## 功能操作

### `start_research`

一次性提交查询并立即返回研究ID。

**输入参数：**
- `query`（必填）— 研究问题或主题
- `mode`（可选）— `quick`（快速摘要）或`detailed`（详细报告）（默认值来自配置）
- `language`（可选）— 报告/摘要的输出语言（例如`en`、`es`、`fr`、`de`、`zh`、`ja`，默认值来自配置或LDR的默认设置）
- `search_tool`（可选）— `searxng`、`auto`、`local_all`（默认值来自配置）
- `iterations`（可选）— 每轮研究循环的次数（默认值：LDR的默认设置）
- `questions_periteration`（可选）— 每轮生成的问题数量

**返回值：**
```json
{
  "research_id": "uuid-string",
  "mode": "detailed",
  "search_tool": "auto",
  "submitted_at": "2026-03-10T08:00:00Z",
  "status": "queued"
}
```

**使用方法：**
```bash
# Quick Summary (faster, shorter)
scripts/ldr-research.sh start_research --query "Solid-state battery advances" --mode quick

# Detailed Report with output in Spanish
scripts/ldr-research.sh start_research \
  --query "What are the latest developments in solid-state batteries?" \
  --mode detailed \
  --language es \
  --search_tool searxng
```

### `get_status`

检查研究任务的进度。

**输入参数：**
- `research_id`（必填）— 通过`start_research`命令生成的研究任务ID

**返回值：**
```json
{
  "research_id": "uuid-string",
  "state": "pending|running|completed|failed|timeout",
  "progress": 45,
  "message": "Synthesizing sources from iteration 2...",
  "last_milestone": "Generated 12 questions from 8 sources"
}
```

**使用方法：**
```bash
scripts/ldr-research.sh get_status --research_id <uuid>
```

### `get_result`

研究完成后获取完整的报告。

**输入参数：**
- `research_id`（必填）— 研究任务ID

**返回值：**
```json
{
  "research_id": "uuid-string",
  "query": "original query",
  "mode": "detailed",
  "summary": "executive summary text",
  "report_markdown": "full markdown report",
  "sources": [
    {
      "id": 1,
      "title": "Source Title",
      "url": "https://example.com",
      "snippet": "relevant excerpt",
      "type": "web|local_doc"
    }
  ],
  "iterations": 3,
  "created_at": "2026-03-10T08:00:00Z",
  "completed_at": "2026-03-10T08:15:00Z"
}
```

**使用方法：**
```bash
scripts/ldr-research.sh get_result --research_id <uuid>
```

## 运用模式

### 一次性处理（等待完成）

对于交互式会话，用户可以按照以下步骤操作：
1. 调用`start_research`开始研究
2. 每10-30秒检查一次`get_status`的状态
3. 当状态变为“completed”时，调用`get_result`获取报告

### 异步处理（一次性提交后等待结果）

对于后台处理流程：
1. 调用`start_research`并返回研究ID给用户
2. 用户可以使用`get_status --research_id <id>`来查看任务进度
3. 研究完成后，调用`get_result`获取完整报告

## 工作流程链

研究完成后，可以按照以下步骤处理结果：
1. 调用`get_result`获取研究来源
2. 将来源数据传递给其他技能（例如`markdown-converter`、`summarize`）
3. 从来源数据中构建RAG索引或知识库

## 错误处理

### `start_research`失败

- **HTTP/网络错误** — 采用指数级退避策略重试（最多尝试3次）
- **LDR验证错误** — 向用户返回错误信息（如查询错误、参数无效）
- **认证失败** — 检查凭据是否正确设置，并向用户显示错误信息

### `get_status`/`get_result`失败

- **临时不可用** — 重试2-3次后再显示错误信息
- **研究任务未找到** — 返回“unknown research_id”错误
- **超时** — 返回包含超时原因的状态信息

## 超时设置

- **每次HTTP请求的超时时间** — 30-60秒（可配置）
- **研究总耗时** — 无客户端限制（由LDR服务管理）
- **状态检查间隔** — 建议设置为10-30秒

## 示例会话流程
```
User: "Research the latest developments in quantum computing"

Assistant: Starting deep research with LDR...
→ start_research(query="latest developments in quantum computing", mode="detailed")
→ Returns: research_id="abc-123", status="queued"

Assistant: Research started (ID: abc-123). This will take ~5-10 minutes.
I'll check the progress and let you know when it's complete.

[After polling...]

Assistant: Research complete! Here's what I found:

## Summary
[summary from get_result]

## Full Report
[report_markdown from get_result]

## Sources (12 found)
1. [Source 1 title](url)
2. [Source 2 title](url)
...
```

## 相关技能

- **academic-deep-research** — 专注于学术研究的替代方案，支持APA第7版引用格式
- **deep-research-pro** — 基于Web的深度研究服务（无需本地LDR）
- **tavily** / **searxng** — 用于快速查询的简单Web搜索工具
- **summarize** — 对LDR的输出结果进行进一步整理和总结

## 故障排除

### LDR服务未响应

1. 确认`LDR_BASE_URL`地址是否正确
2. 检查LDR服务是否正在运行：`curl http://127.0.0.1:5000/health`
3. 查看LDR服务的日志以获取错误信息

### 认证失败

1. 确保凭据仅通过环境变量或本地`.env`文件设置（例如`LDR_SERVICE_USER`、`LDR_SERVICE_PASSWORD`），切勿写入已提交的配置文件
2. LDR使用会话cookie和CSRF认证机制（而非基本认证）。脚本会首先访问登录页面，提取CSRF令牌，然后提交登录表单。如果LDR使用不同的登录路径或字段名称，请调整`LDR_LOGIN_URL`或参考脚本中的登录说明
3. 测试：使用正确的凭据运行脚本，确认是否能够成功登录；或者直接在浏览器中访问`LDR_LOGIN_URL`进行登录，以验证LDR服务是否正常运行

### 研究任务长时间处于“running”状态

1. 检查LDR服务的运行状态
2. 查看LDR服务的日志，确认是否存在卡住的作业
3. 如果超过30分钟仍未有进展，可以考虑超时处理并重新启动服务