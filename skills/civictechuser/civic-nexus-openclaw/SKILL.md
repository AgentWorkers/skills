---
name: civic-nexus
description: "连接到 Civic Nexus MCP，以实现 100 多种集成功能。"
metadata: {"openclaw":{"requires":{"env":["NEXUS_URL","NEXUS_TOKEN"],"anyBins":["mcporter","npx"]},"primaryEnv":"NEXUS_TOKEN"}}
---

# Civic Nexus MCP Bridge

> **⚠️ 免责声明：请自行承担使用风险。如需官方文档，请访问 [docs.civic.com](https://docs.civic.com)。**

通过 [Civic Nexus](https://nexus.civic.com) 可实现与 100 多个服务的集成，包括 Gmail、PostgreSQL、MongoDB、Box 等。

## 设置

### 1. 获取 Nexus 的登录凭据

1. 访问 [nexus.civic.com](https://nexus.civic.com) 并登录
2. 从个人设置中获取您的 **MCP URL** 和 **访问令牌**

### 2. 在 OpenClaw 中进行配置

将以下配置添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "civic-nexus": {
        "enabled": true,
        "env": {
          "NEXUS_URL": "https://nexus.civic.com/hub/mcp?accountId=YOUR_ACCOUNT_ID&profile=YOUR_PROFILE",
          "NEXUS_TOKEN": "your-access-token"
        }
      }
    }
  }
}
```

### 3. （可选）配置 mcporter

如果您已安装了 mcporter（使用命令 `npm install -g mcporter`），请将其配置添加到 `~/.openclaw/workspace/config/mcporter.json` 文件中：

```json
{
  "mcpServers": {
    "nexus": {
      "baseUrl": "https://nexus.civic.com/hub/mcp?accountId=YOUR_ACCOUNT_ID&profile=YOUR_PROFILE",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN",
        "User-Agent": "openclaw/1.0.0"
      }
    }
  }
}
```

## 代理程序的使用说明

当用户希望通过 Nexus 与外部服务交互时，首先尝试使用 mcporter；如果 mcporter 失败，则会切换到 TypeScript 脚本。

### 使用 mcporter

```bash
# List tools
mcporter list nexus

# Search tools
mcporter list nexus | grep gmail

# Call a tool
mcporter call 'nexus.google-gmail-search_gmail_messages(query: "is:unread")'
```

### 备用方案：TypeScript 脚本

```bash
# List tools
npx tsx {baseDir}/nexus-tool-runner.ts --list

# Search tools
npx tsx {baseDir}/nexus-tool-runner.ts --search gmail

# Get tool schema
npx tsx {baseDir}/nexus-tool-runner.ts --schema google-gmail-search_gmail_messages

# Call a tool
npx tsx {baseDir}/nexus-tool-runner.ts --call google-gmail-search_gmail_messages --args '{"query": "is:unread"}'
```

### 授权流程

某些工具在首次使用时需要 OAuth 认证。当您看到授权请求 URL 时，请执行以下操作：

1. 将该 URL 显示给用户
2. 用户授权后，继续执行后续操作：
   ```bash
   # mcporter
   mcporter call 'nexus.continue_job(jobId: "JOB_ID")'

   # script
   npx tsx {baseDir}/nexus-tool-runner.ts --call continue_job --args '{"job_id": "JOB_ID"}'
   ```

## 注意事项

- API 调用可能需要 10–15 秒（取决于服务器端响应时间）
- 令牌的有效期为约 30 天，如有需要可从 Nexus 重新生成
- Gmail 的批量请求每次调用最多只能发送 5–25 条消息

---