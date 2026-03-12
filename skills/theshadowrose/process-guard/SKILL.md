---
name: "ProcessGuard — Critical Process Monitor & Auto-Restart"
description: "监控关键进程，并在进程失败时自动重启。系统会跟踪CPU和内存的使用情况，通过Webhook、回调或文件等方式触发警报；同时会生成“死人开关”（dead man’s switch）心跳信号，以便在ProcessGuard本身出现故障时能够及时发现。提供HTTP仪表板进行实时监控。无需任何额外的依赖项——默认情况下仅支持CPU和内存监控功能；如需更详细的信息（如进程ID使用情况），可额外安装pidusage插件。"
author: "@TheShadowRose"
version: "2.1.3"
tags: ["process-guard", "monitor", "auto-restart", "uptime", "devops"]
license: "MIT"
---
# ProcessGuard — 关键进程监控与自动重启工具

无需人工值守，即可确保服务持续运行。只需定义进程、配置健康检查规则，其余工作交由 ProcessGuard 处理即可。

## 功能简介

- **健康检查**：支持通过 HTTP、TCP 端口、PID 文件或 shell 命令进行健康检查。
- **自动重启**：支持配置重试次数和冷却时间间隔。
- **CPU 和内存监控**：为每个进程设置阈值，并在超出阈值时发出警报（需安装 `npm install pidusage`）。
- **警报升级机制**：从警告级别升级为严重级别，并通过回调、Webhook 或 JSON 文件通知相关人员。
- **死机检测机制**：每 10 秒更新一次心跳文件，以便外部监控工具能够检测 ProcessGuard 是否发生故障。
- **HTTP 仪表盘**：提供 `/status` 端点，可获取实时 JSON 状态信息（可选）。
- **命令白名单**：可限制允许使用哪些可执行文件来执行重启或检查操作。

## 快速安装

```javascript
const { ProcessGuard } = require('./src/process-guard');

const guard = new ProcessGuard({
  processes: [
    {
      name: 'ollama',
      check: 'http://localhost:11434/api/tags',
      restart: 'ollama serve',
      maxRestarts: 5,
      cooldown: 5000
    }
  ],
  checkInterval: 30000,
  dashboardPort: 9090,
  alert: {
    onAlert: async (alert) => console.error(`ALERT: ${alert.message}`)
  }
});

guard.start();
```

请参阅 README.md 文件以获取完整文档、所有配置选项及高级使用示例。