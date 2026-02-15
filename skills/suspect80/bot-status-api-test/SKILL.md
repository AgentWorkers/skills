---
name: bot-status-api
description: "部署一个轻量级的状态检查 API，该 API 可用于展示您的 OpenClaw 机器人的运行状态、服务连接情况、定时任务（cron jobs）、技能（skills）、系统指标等信息。您可以在设置监控仪表板、健康检查端点（health endpoint）或 OpenClaw 代理的状态页面时使用该 API。该 API 支持通过配置文件（config）来检查任何类型的服务（例如 HTTP 请求、CLI 命令、文件检查等）。完全无依赖项，仅依赖 Node.js 运行环境。"
---

# Bot状态API

这是一个可配置的HTTP服务，用于以JSON格式公开您的OpenClaw机器人的运行状态。该服务专为集成到仪表板、监控系统以及提升系统透明度而设计。

## 提供的功能

- **机器人核心信息**：在线状态、使用的模型、上下文信息、运行时间、心跳信号发送频率
- **服务检查**：对任何HTTP端点、命令行工具或文件路径进行健康检查
- **电子邮件**：来自himalaya、gog等邮件服务的未读邮件数量
- **Cron作业**：直接从OpenClaw的`cron/jobs.json`文件中读取Cron作业信息
- **Docker容器**：通过Portainer API监控Docker容器的健康状况
- **开发服务器**：通过进程匹配自动检测正在运行的开发服务器
- **技能信息**：列出已安装且可使用的OpenClaw技能
- **系统指标**：从`/proc`文件系统中获取CPU、RAM和磁盘使用情况等系统指标

## 设置步骤

### 1. 复制服务相关文件

将`server.js`、`collectors/`文件夹以及`package.json`文件复制到您指定的位置。

### 2. 创建`config.json`配置文件

将`config.example.json`文件复制到`config.json`中，并根据需要进行自定义：

```json
{
  "port": 3200,
  "name": "MyBot",
  "workspace": "/path/to/.openclaw/workspace",
  "openclawHome": "/path/to/.openclaw",
  "cache": { "ttlMs": 10000 },
  "model": "claude-sonnet-4-20250514",
  "skillDirs": ["/path/to/openclaw/skills"],
  "services": [
    { "name": "myservice", "type": "http", "url": "http://...", "healthPath": "/health" }
  ]
}
```

### 服务检查类型

| 类型 | 描述 | 配置参数 |
|------|-------------|--------|
| `http` | 获取指定URL的内容，并检查是否返回HTTP 200状态码 | `url`, `healthPath`, `method`, `headers`, `body` |
| `command` | 运行shell命令，并检查命令是否成功执行（返回0码） | `command`, `timeout` |
| `file-exists` | 检查指定路径是否存在 | `path` |

### 3. 运行服务

```bash
node server.js
```

### 4. 将服务设置为系统服务（使用systemd）

```ini
# ~/.config/systemd/user/bot-status.service
[Unit]
Description=Bot Status API
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/bot-status
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=5
Environment=PORT=3200
Environment=HOME=/home/youruser
Environment=PATH=/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=default.target
```

### 5. 从OpenClaw获取关键运行数据

机器人应定期将其运行状态数据写入工作目录下的`heartbeat-state.json`文件中：

```json
{
  "vitals": {
    "contextPercent": 62,
    "contextUsed": 124000,
    "contextMax": 200000,
    "model": "claude-opus-4-5",
    "updatedAt": 1770304500000
  }
}
```

请将上述内容添加到您的`HEARTBEAT.md`文件中，以确保机器人能在每次发送心跳信号时更新该文件。

## API端点

| 端点 | 描述 |
|----------|-------------|
| `GET /status` | 提供完整的机器人状态信息（数据会缓存） |
| `GET /health` | 返回简单的{"status":"ok"}响应 |

## 架构特点

- **无依赖项**：仅使用Node.js内置模块（`http`, `fs`, `child_process`）
- **非阻塞式处理**：所有shell命令均使用异步执行（`exec`），避免阻塞主线程
- **后台更新**：数据缓存会定期更新，请求总是从缓存中即时返回（响应时间约10毫秒）
- **配置驱动**：所有配置信息都存储在`config.json`文件中，无硬编码值