---
name: prusalink-cli
description: "OpenClaw 技能：本地 PrusaLink CLI（基于 curl 的封装工具），支持使用 Digest 身份验证（用户名/密码）或可选的 X-Api-Key 来查询状态、上传文件或打印打印输出。"
user-invocable: true
metadata: {
  "author": "DonSqualo",
  "env": {
    "PRUSALINK_HOST": { "description": "Printer host/IP (default: printer.local).", "default": "printer.local" },
    "PRUSALINK_SCHEME": { "description": "http or https (default: http).", "default": "http" },
    "PRUSALINK_USER": { "description": "PrusaLink Digest username." },
    "PRUSALINK_PASSWORD": { "description": "PrusaLink Digest password." },
    "PRUSALINK_API_KEY": { "description": "Optional: send as X-Api-Key if your PrusaLink supports it." },
    "PRUSALINK_TIMEOUT": { "description": "curl max-time seconds (default: 10).", "default": "10" }
  },
  "openclaw": { "requires": { "bins": ["curl"] } }
}
---
# PrusaLink CLI

该技能通过 `run.sh` 脚本提供了一个基于 `curl` 的小型 PrusaLink 命令行工具（CLI）。

出于安全考虑，该技能**故意**不包含任何“任意 API 请求”命令（以防止提示注入攻击）。它仅暴露了固定且常用的接口（如状态查询、任务执行、文件上传、任务启动和任务取消等）。

## 安装到 OpenClaw 中

将此文件夹复制到：

- `~/.openclaw/skills/prusalink-cli/`

之后 OpenClaw 将能够识别并使用该技能。

## 运行

通过以下命令运行该技能：

```bash
~/.openclaw/skills/prusalink-cli/run.sh --help
```

## 认证

可以选择以下任一认证方式：

- **摘要认证（Digest Authentication）**：`PRUSALINK_USER` + `PRUSALINK_PASSWORD`（推荐）
- 或 **API 密钥（API Key）**：如果您的 PrusaLink 支持该方式，可以使用 `PRUSALINK_API_KEY`，并通过 `X-Api-Key` 头字段进行传递

**注意防止 shell 历史记录泄露：**

```bash
~/.openclaw/skills/prusalink-cli/run.sh --password-file /path/to/secret status
```

## 安全说明

- 该技能在运行时不会从网络下载或执行任何代码。
- 它仅向您配置的 `PRUSALINK_HOST` 发送 HTTP 请求。