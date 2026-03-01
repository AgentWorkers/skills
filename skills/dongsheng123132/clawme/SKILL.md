---
name: clawme
version: 1.0.0
description: 通过ClawMe Chrome扩展程序向用户的真实浏览器发送指令。可以执行填写表单、发送推文、发送电子邮件、点击链接以及提取数据等操作；用户可以在侧边面板中实时查看并确认每个操作的执行情况。与无头浏览器不同，该扩展程序是在用户自己的Chrome浏览器中运行的，并且会使用用户的登录会话。
tags: ["browser", "automation", "form-fill", "chrome-extension", "twitter", "email"]
metadata: {"openclaw":{"emoji":"🦞","primaryEnv":"CLAWME_CLIENT_TOKEN","requires":{"env":["CLAWME_CLIENT_TOKEN"]}}}
---
# ClawMe — 在用户的真实浏览器中执行操作

通过ClawMe扩展程序向用户的Chrome浏览器发送指令。用户会在侧边栏中看到每条指令，并点击“执行”来确认操作。与无头浏览器不同，ClawMe是在用户的真实浏览器中运行的，并使用用户的实际登录会话。

**设置**：用户需要安装ClawMe Chrome扩展程序，并配置后端URL和Token。

## 如何发送指令

如果可用，请使用`clawme_send`工具；否则，可以通过HTTP POST请求发送指令：
```
POST ${CLAWME_BASE_URL:-https://api.clawme.net}/v1/instructions
Headers: Content-Type: application/json, X-ClawMe-Token: ${CLAWME_CLIENT_TOKEN}
Body: {"target":"browser","instruction":{"type":"<type>","payload":{...}}}
```

## 指令类型

### compose_tweet
当用户输入“关于...发推文”或“在X平台上发布...”时使用此指令。
```json
{"type":"compose_tweet","payload":{"text":"tweet content"}}
```

### compose_email
当用户输入“给...写邮件”或“发送邮件...”时使用此指令。
```json
{"type":"compose_email","payload":{"to":"email@example.com","subject":"Subject","body":"Body text","use_gmail":true}}
```

### fill_form
当用户输入“填写表格...”或“输入我的信息...”时使用此指令。
```json
{"type":"fill_form","payload":{"url":"https://example.com/form","fields":{"#name":"John","input[name=email]":"john@example.com","select[name=country]":"US"}}}
```
支持的操作包括：输入框（input）、文本区域（textarea）、单选框（checkbox）、复选框（radio）、可编辑内容区域（例如Xiaohongshu、Medium）。可以使用CSS选择器作为字段标识符；对于当前页面，无需指定`url`字段。

### click
当用户输入“点击按钮...”或“提交表格...”时使用此指令。
```json
{"type":"click","payload":{"selector":"button[type=submit]","url":"https://example.com/form"}}
```

### extract
当用户输入“从...获取文本”或“抓取数据...”时使用此指令。
```json
{"type":"extract","payload":{"selector":".results","url":"https://example.com/search"}}
```
提取到的文本会反馈给代理服务器。

### open_url
当用户输入“打开URL...”时使用此指令。
```json
{"type":"open_url","payload":{"url":"https://example.com","in_new_tab":true}}
```

### remind
当用户需要接收提醒时使用此指令。
```json
{"type":"remind","payload":{"title":"Meeting","body":"Team standup in 5 minutes"}}
```

## 多步骤工作流程

可以通过`metaworkflow_id`和`meta.step`参数来链接多个指令：
```
POST /v1/instructions — {"target":"browser","instruction":{"type":"open_url","payload":{"url":"..."}}, "meta":{"workflow_id":"signup","step":1}}
POST /v1/instructions — {"target":"browser","instruction":{"type":"fill_form","payload":{"fields":{...}}}, "meta":{"workflow_id":"signup","step":2}}
POST /v1/instructions — {"target":"browser","instruction":{"type":"click","payload":{"selector":"button[type=submit]"}}, "meta":{"workflow_id":"signup","step":3}}
```
用户会看到一个带有进度条的工作流程卡片，并可以按顺序执行所有步骤。

## 环境变量

- `CLAWME_CLIENT_TOKEN`（必填）—— 与Chrome扩展程序中配置的Token相匹配
- `CLAWME_BASE_URL`（可选）—— 默认值为`https://api.clawme.net`，或`http://127.0.0.1:31871`（用于本地开发）