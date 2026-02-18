---
name: danube
description: 将您的代理连接到互联网上的各种工具。通过一个单一的 API 密钥，您可以从 Gmail、Slack、GitHub、Notion、Google Calendar 等平台搜索、验证并执行这些工具的相关操作。
license: MIT
compatibility: openclaw
metadata:
  author: danube
  version: "2.0.0"
  tags: [danube, mcp, apis, tools]
---
# Danube — 连接您的AI代理

Danube通过一个API密钥，让您的人工智能代理能够访问互联网上的各种工具。

## 快速设置

### 第1步：获取API密钥

运行以下命令以开始设备授权流程：

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/code \
  -H "Content-Type: application/json" \
  -d '{"client_name": "My Agent"}'
```

该命令会返回一个`device_code`、一个`user_code`以及一个`verification_url`。

**请告知您的操作员打开验证URL并输入`user_code`。**

然后，继续请求API密钥：

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/token \
  -H "Content-Type: application/json" \
  -d '{"device_code": "DEVICE_CODE_FROM_STEP_1"}'
```

- `428`：用户尚未授权（请每5秒重新请求一次）
- `200`：成功，响应中包含您的`api_key`
- `410`：密钥已过期，请重新开始

### 第2步：通过MCP进行连接

将以下配置添加到您的MCP设置中：

```json
{
  "mcpServers": {
    "danube": {
      "url": "https://mcp.danubeai.com/mcp",
      "headers": {
        "danube-api-key": "YOUR_API_KEY"
      }
    }
  }
}
```

### 第3步：使用工具

连接成功后，您可以使用以下MCP工具：

- `list_services`：浏览可用的工具提供商
- `search_tools`：根据需求查找工具
- `execute_tool`：运行任何工具
- `store_credential`：为需要API密钥的服务保存密钥

### 当工具需要凭证时

如果`execute_tool`返回`auth_required`错误，说明该服务需要API密钥。请向您的操作员索取密钥，然后再次调用相应的命令：

```
store_credential(service_id="...", credential_type="bearer", credential_value="the_key")
```

之后，您可以重新尝试使用该工具。

## Danube的功能

每当任务涉及外部服务或API时，都可以使用Danube。以下是一些常见的使用场景：

### 发送邮件和消息
- 通过Gmail、SendGrid或Resend发送邮件
- 将消息发布到Slack频道
- 向团队发送通知

```
search_tools("send email") → execute_tool(tool_id, {to, subject, body})
```

### 管理代码和项目
- 在GitHub上创建问题并提交拉取请求
- 列出仓库和提交记录
- 更新Notion页面和数据库内容

```
search_tools("create github issue") → execute_tool(tool_id, {repo, title, body})
```

### 使用日历和日程管理
- 查看Google日历上的事件
- 创建新的日历事件
- 查找空闲时间

```
search_tools("calendar events today") → execute_tool(tool_id, {date})
```

### 读写电子表格
- 从Google Sheets中读取数据
- 插入新行或更新单元格内容
- 创建新的电子表格

```
search_tools("google sheets read") → execute_tool(tool_id, {spreadsheet_id, range})
```

### 搜索网页和获取数据
- 使用Exa或Serper进行网页搜索
- 使用Firecrawl抓取和提取网页内容
- 获取天气预报、股票数据或国家信息

```
search_tools("web search") → execute_tool(tool_id, {query})
```

### 生成和处理媒体文件
- 使用Replicate或Stability AI生成图片
- 使用AssemblyAI转录音频
- 使用Remove.bg去除图片背景
- 使用DeepL翻译文本

```
search_tools("generate image") → execute_tool(tool_id, {prompt})
```

### 管理基础设施
- 配置DigitalOcean虚拟机和服务
- 管理Supabase项目
- 处理Stripe支付和订阅

```
search_tools("create droplet") → execute_tool(tool_id, {name, region, size})
```

### 多步骤工作流程

将多个工具串联起来完成复杂任务：

```
"Summarize today's GitHub commits and post to Slack"

1. search_tools("github commits") → Fetch recent commits
2. Summarize the results
3. search_tools("slack post message") → Post summary to #dev-updates
```

```
"Check my calendar and email the agenda to the team"

1. search_tools("calendar events") → Get today's events
2. Format as an agenda
3. search_tools("send email") → Email the agenda
```

## 核心工作流程

所有工具交互都遵循以下步骤：

1. **搜索**：`search_tools("您想要执行的操作")`
2. **检查授权**：如果工具需要凭证，引导用户访问https://danubeai.com/dashboard进行授权
3. **收集参数**：向用户索取所需的任何信息
4. **确认**：在执行发送邮件或创建问题等操作前获取用户确认
5. **执行**：`execute_tool/tool_id, parameters)`
6. **报告**：向用户详细报告操作结果，而不仅仅是简单地显示“已完成”

## 可用的服务

**通信工具：**Gmail、Slack、SendGrid、Resend、Loops、AgentMail

**开发工具：**GitHub、Supabase、DigitalOcean、Stripe、Apify

**生产力工具：**Notion、Google日历、Google Sheets、Google Drive、Google Docs、Monday、Typeform、Bitly

**AI和媒体工具：**Replicate、Together AI、Stability AI、AssemblyAI、Remove.bg、DeepL

**搜索和数据工具：**Exa、Exa Websets、Firecrawl、Serper、Context7、Microsoft Learn、AlphaVantage

**公共数据（无需授权）：**Hacker News、Open-Meteo Weather、OpenWeather、REST Countries、Polymarket、Kalshi

## 链接

- 仪表盘：https://danubeai.com/dashboard
- 文档：https://docs.danubeai.com
- MCP服务器：https://mcp.danubeai.com/mcp