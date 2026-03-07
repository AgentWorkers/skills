---
name: civic
description: "连接到Civic MCP，以实现100多种集成功能。"
metadata: {"openclaw":{"requires":{"env":["CIVIC_URL","CIVIC_TOKEN"],"anyBins":["mcporter","npx"]},"primaryEnv":"CIVIC_TOKEN"}}
---
# Civic MCP Bridge

> **⚠️ 免责声明：使用本工具需自行承担风险。如需官方文档，请访问 [docs.civic.com](https://docs.civic.com)。**

通过 [Civic](https://nexus.civic.com) 连接，可集成超过 100 种服务，包括 Gmail、PostgreSQL、MongoDB、Box 等。

## 设置

### 1. 获取 Civic 的登录凭据

1. 访问 [nexus.civic.com](https://nexus.civic.com) 并登录
2. 从个人设置中获取您的 **MCP URL** 和 **访问令牌**

### 2. 在 OpenClaw 中进行配置

将以下配置添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "civic": {
        "enabled": true,
        "env": {
          "CIVIC_URL": "https://nexus.civic.com/hub/mcp?accountId=YOUR_ACCOUNT_ID&profile=YOUR_PROFILE",
          "CIVIC_TOKEN": "your-access-token"
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
    "civic": {
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

当用户需要通过 Civic 与外部服务交互时，首先尝试使用 mcporter；如果 mcporter 失败，则会自动切换到 TypeScript 脚本。

### 使用 mcporter

```bash
# List tools
mcporter list civic

# Search tools
mcporter list civic | grep gmail

# Call a tool
mcporter call 'civic.google-gmail-search_gmail_messages(query: "is:unread")'
```

### 备用方案：TypeScript 脚本

```bash
# List tools
npx tsx {baseDir}/civic-tool-runner.ts --list

# Search tools
npx tsx {baseDir}/civic-tool-runner.ts --search gmail

# Get tool schema
npx tsx {baseDir}/civic-tool-runner.ts --schema google-gmail-search_gmail_messages

# Call a tool
npx tsx {baseDir}/civic-tool-runner.ts --call google-gmail-search_gmail_messages --args '{"query": "is:unread"}'
```

### 授权流程

某些工具在首次使用时需要 OAuth 认证。当您看到授权请求页面时，请：

1. 将该 URL 显示给用户
2. 用户授权后，继续执行后续操作：
   ```bash
   # mcporter
   mcporter call 'civic.continue_job(jobId: "JOB_ID")'

   # script
   npx tsx {baseDir}/civic-tool-runner.ts --call continue_job --args '{"job_id": "JOB_ID"}'
   ```

## 注意事项

- API 调用可能需要 10–15 秒（取决于服务器响应时间）
- 令牌的有效期为约 30 天，如需更新，请从 Civic 网站重新获取令牌
- Gmail 的批量请求每次最多只能发送 5–25 条消息

---