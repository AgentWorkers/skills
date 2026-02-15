---
name: openclaw-persistent-memory
version: 0.1.0
description: 持久内存系统——自动上下文捕获与语义搜索
author: Jason Brashear / Titanium Computing
repository: https://github.com/webdevtodayjason/openclaw_memory
metadata:
  openclaw:
    requires:
      bins: ["openclaw-persistent-memory"]
    install:
      - id: node
        kind: node
        package: openclaw-persistent-memory
        bins: ["openclaw-persistent-memory"]
        label: "Install OpenClaw Persistent Memory (npm)"
---

# OpenClaw 持久化内存系统

OpenClaw 是一个持久化内存系统，它利用 SQLite 和 FTS5 技术在会话之间自动捕获用户的相关信息。

## 主要特性

- 🧠 **自动捕获**：每次用户做出响应后，重要的观察结果会自动被保存下来。
- 🔍 **自动回忆**：在每次用户收到提示时，相关的记忆内容会被自动呈现给用户。
- 💾 **SQLite + FTS5**：支持对所有保存的记忆内容进行快速的全文搜索。
- 🛠️ **工具**：提供了 `memory_search`、`memory_get`、`memory_store` 和 `memory_delete` 等实用工具。
- 📊 **渐进式展示**：通过高效的方式逐步向用户展示记忆内容。

## 设置步骤

1. **安装 npm 包：**
   ```bash
   npm install -g openclaw-persistent-memory
   ```

2. **启动工作进程服务：**
   ```bash
   openclaw-persistent-memory start
   ```

3. **安装 OpenClaw 扩展程序：**
   ```bash
   # Copy extension to OpenClaw extensions directory
   cp -r node_modules/openclaw-persistent-memory/extension ~/.openclaw/extensions/openclaw-mem
   cd ~/.openclaw/extensions/openclaw-mem && npm install
   ```

4. **配置 OpenClaw（在 `~/.openclaw/openclaw.json` 文件中配置）：**
   ```json
   {
     "plugins": {
       "slots": {
         "memory": "openclaw-mem"
       },
       "allow": ["openclaw-mem"],
       "entries": {
         "openclaw-mem": {
           "enabled": true,
           "config": {
             "workerUrl": "http://127.0.0.1:37778",
             "autoCapture": true,
             "autoRecall": true
           }
         }
       }
     }
   }
   ```

5. **重启 OpenClaw 服务器：**

## 提供的工具

| 工具 | 功能描述 |
|------|-------------|
| `memory_search` | 通过自然语言查询记忆内容。 |
| `memory_get` | 根据 ID 获取特定的记忆内容。 |
| `memory_store` | 保存重要信息。 |
| `memory_delete` | 根据 ID 删除记忆内容。 |

## API 端点

工作进程运行在 `http://127.0.0.1:37778` 上：

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/api/health` | GET | 获取系统健康状态。 |
| `/api/stats` | GET | 查看数据库统计信息。 |
| `/api/search` | POST | 执行全文搜索。 |
| `/api/observations` | GET | 列出最近的观察结果。 |
| `/api/observations/:id` | GET | 获取指定 ID 的观察结果。 |
| `/api/observations/:id` | DELETE | 删除指定 ID 的观察结果。 |
| `/api/observations/:id` | PATCH | 更新指定 ID 的观察结果。 |

## 故障排除

### 工作进程未运行
```bash
curl http://127.0.0.1:37778/api/health
# If fails, restart:
openclaw-persistent-memory start
```

### 自动回忆功能未生效
- 检查 OpenClaw 日志：`tail ~/.openclaw/logs/*.log | grep openclaw-mem`
- 确保 `plugins.slots.memory` 的值设置为 `"openclaw-mem"`
- 在配置更改后重启 OpenClaw 服务器。