---
name: PersonalDataHub
description: 通过 PersonalDataHub 访问控制网关，可以获取个人数据（如电子邮件、问题记录等），并制定相应的处理方案（如草拟回复或发送回复）。在数据传递给处理人员之前，系统会根据数据所有者的政策对数据进行过滤、编辑和处理。
version: 0.1.0
skillKey: personaldatahub
emoji: 🔐
homepage: https://github.com/AISmithLab/PersonalDataHub
os: darwin, linux, win32
install: cd ../../ && pnpm install && pnpm build && npx pdh init "OpenClaw Agent" && npx pdh start
metadata: {}
always: false
---
# PersonalDataHub

通过PersonalDataHub访问控制网关，您可以访问来自Gmail、GitHub等来源的个人数据。数据所有者可以控制代理程序能够查看哪些信息、哪些字段是可见的、哪些内容会被隐藏，以及允许执行哪些操作。

## MCP设置（推荐）

PersonalDataHub提供了一个MCP服务器，用于发现可用的工具。请将其添加到您的Claude代码配置文件（`.claude/settings.json`）中：

```json
{
  "mcpServers": {
    "personaldatahub": {
      "command": "npx",
      "args": ["pdh", "mcp"]
    }
  }
}
```

这样就可以动态地注册特定来源的工具了——只有已连接OAuth令牌的来源才能使用这些工具。

## 工具

### read_emails
*(需要连接Gmail的OAuth)*

从Gmail中提取电子邮件。数据会根据所有者的访问控制策略进行过滤和隐藏部分内容。

**参数：**
- `purpose`（必填）——获取这些数据的原因（用于审计记录）
- `query`（可选）——Gmail搜索查询（例如：`"is:unread from:alice newer_than:7d"`）
- `limit`（可选）——返回的结果数量上限

**示例：**
```
Pull my recent unread emails about the Q4 report.
```

### draft_email
*(需要连接Gmail的OAuth)*

通过Gmail起草电子邮件。草稿会先提交给数据所有者审核——在获得批准之前不会实际发送。

**参数：**
- `to`（必填）——收件人电子邮件地址
- `subject`（必填）——电子邮件主题
- `body`（必填）——电子邮件正文
- `purpose`（必填）——执行此操作的原因（用于审计记录）
- `in_reply_to`（可选）——用于关联消息的邮件ID

### send_email
*(需要连接Gmail的OAuth)*

通过Gmail发送电子邮件。该操作会先提交给数据所有者审核——在获得批准之前不会实际发送。

**参数：**
- `to`（必填）——收件人电子邮件地址
- `subject`（必填）——电子邮件主题
- `body`（必填）——电子邮件正文
- `purpose`（必填）——执行此操作的原因（用于审计记录）
- `in_reply_to`（可选）——用于关联消息的邮件ID

### reply_to_email
*(需要连接Gmail的OAuth)*

通过Gmail回复电子邮件。回复会先提交给数据所有者审核——在获得批准之前不会实际发送。

**参数：**
- `to`（必填）——收件人电子邮件地址
- `subject`（必填）——电子邮件主题
- `body`（必填）——电子邮件正文
- `in_reply_to`（必填）——被回复邮件的ID
- `purpose`（必填）——执行此操作的原因（用于审计记录）

### search_github_issues
*(需要连接GitHub的OAuth)*

搜索GitHub上的问题。数据会根据所有者的访问控制策略进行过滤。

**参数：**
- `purpose`（必填）——获取这些数据的原因（用于审计记录）
- `query`（可选）——问题搜索查询
- `limit`（可选）——返回的结果数量上限

### search_github_prs
*(需要连接GitHub的OAuth)*

搜索GitHub上的拉取请求。数据会根据所有者的访问控制策略进行过滤。

**参数：**
- `purpose`（必填）——获取这些数据的原因（用于审计记录）
- `query`（可选）——拉取请求搜索查询
- `limit`（可选）——返回的结果数量上限

## 直接使用API

如果上述MCP工具不可用，您也可以直接通过HTTP调用PersonalDataHub API。

**配置：** 请阅读`~/.pdh/config.json`以获取`hubUrl`。

**获取数据：**
```bash
curl -X POST <hubUrl>/app/v1/pull \
  -H "Content-Type: application/json" \
  -d '{"source": "gmail", "purpose": "reason for pulling data"}'
```

**提出操作请求：**
```bash
curl -X POST <hubUrl>/app/v1/propose \
  -H "Content-Type: application/json" \
  -d '{"source": "gmail", "action_type": "draft_email", "action_data": {"to": "...", "subject": "...", "body": "..."}, "purpose": "reason for action"}'
```

## 故障排除**

如果调用失败，请检查PersonalDataHub服务器是否正在运行：
```bash
curl <hubUrl>/health
```

如果服务器未运行，请找到并启动它：
```bash
# Check where PersonalDataHub is installed
cat ~/.pdh/config.json   # look at hubDir
# Start the server
cd <hubDir> && node dist/index.js
```

## 设置

安装脚本会自动配置PersonalDataHub：
1. 安装依赖项，构建项目，初始化数据库
2. 将API地址和目录保存到`~/.pdh/config.json`中
3. 在后台启动服务器

安装完成后，打开`http://localhost:3000`，通过OAuth连接Gmail/GitHub。

代理程序会自动从`~/.pdh/config.json`中读取配置——无需手动配置。

## 查询语法（Gmail）

- `is:unread` — 未读邮件
- `from:alice` — 来自Alice的邮件
- `newer_than:7d` — 过去7天内的邮件
- `subject:report` — 主题中包含“report”的邮件
- 组合查询：`is:unread from:alice newer_than:7d`

## 重要说明

- **数据会被过滤**：所有者可以控制您能看到的字段。某些字段可能缺失或被隐藏。
- **操作需要审批**：所有出站操作（发送邮件、起草邮件等）都会先进入待审队列。必须获得所有者的批准后才能执行。
- **所有操作都会被记录**：每次数据请求和操作请求都会被记录下来，并附带操作原因。