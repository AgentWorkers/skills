---
name: Monitor
slug: monitor
version: 1.0.2
description: 可以创建用于监控任何目标的工具。用户负责定义需要监控的内容，而系统则负责安排监控任务并发送警报。
changelog: Declared required binaries and optional env vars in metadata
metadata: {"clawdbot":{"emoji":"📡","requires":{"bins":["curl"],"env":{"optional":["PUSHOVER_TOKEN","PUSHOVER_USER"]}},"os":["linux","darwin","win32"]}}
---
## 数据存储

```
~/monitor/
├── monitors.json       # Monitor definitions
├── config.json         # Alert preferences
└── logs/               # Check results
    └── {name}/YYYY-MM.jsonl
```

首次使用时创建目录：`mkdir -p ~/monitor/logs`

## 功能范围

该功能：
- ✅ 将监控配置信息存储在 `~/monitor/` 目录下
- ✅ 按指定间隔执行检查
- ✅ 在状态发生变化时向用户发送警报

**执行机制：**
- 用户明确指定需要监控的内容
- 用户授予所需的权限或工具
- 该功能仅负责确定检查的频率和发送警报的方式

**注意事项：**
- 该功能不会自动访问任何服务或端点
- 该功能不会在未经用户明确指令的情况下执行检查
- 该功能不会存储用户的凭据（用户需要通过环境变量或其他功能提供凭据）

## 所需条件

**必备条件：**
- `curl` — 用于执行 HTTP 请求

**可选条件（用于警报功能）：**
- `PUSHOVER_TOKEN` / `PUSHOVER_USER` — 用于接收推送通知
- Webhook URL — 用户需要提供自己的通知端点

**如果可用，会使用以下工具：**
- `openssl` — 用于检查 SSL 证书的有效性
- `pgrep` — 用于检查进程是否正在运行
- `df` — 用于检查磁盘空间使用情况
- `nc` — 用于检查端口是否开放

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 监控类型示例 | `templates.md` |
| 警报配置 | `alerts.md` |
| 分析模板 | `insights.md` |

## 核心规则

### 1. 用户全权控制
当用户请求创建监控任务时：
1. **监控内容**：用户指定需要检查的内容
2. **检查方式**：用户选择使用哪种工具或方法
3. **检查频率**：用户设置检查的间隔时间
4. **警报设置**：用户设置警报的触发条件

**示例流程：**
```
User: "Monitor my API at api.example.com every 5 minutes"
Agent: "I'll check HTTP status. Alert you on failures?"
User: "Yes, and check SSL cert too"
→ Monitor stored with user-defined checks
```

### 2. 监控配置文件
配置文件位于 `~/monitor/monitors.json` 中：
```json
{
  "api_prod": {
    "description": "User's API health",
    "checks": [
      {"type": "http", "target": "https://api.example.com/health"},
      {"type": "ssl", "target": "api.example.com"}
    ],
    "interval": "5m",
    "alert_on": "change",
    "requires": [],
    "created": "2024-03-15"
  }
}
```

### 3. 常见的检查类型
用户可以请求以下类型的检查（或其他类型）：

| 检查类型 | 检查内容 | 使用的工具 |
|------|---------------|-----------|
| HTTP | 网页地址的状态及响应延迟 | `curl` |
| SSL | SSL 证书的有效期 | `openssl` |
| 进程 | 检查进程是否正在运行 | `pgrep` |
| 磁盘空间 | 磁盘剩余空间 | `df` |
| 端口 | 检查端口是否开放 | `nc` |
| 自定义 | 用户自定义的命令 | 用户自行指定 |

### 4. 配置确认格式
```
✅ Monitor: [description]
🔍 Checks: [what will be checked]
⏱️ Interval: [how often]
🔔 Alert: [when to notify]
🔧 Requires: [tools/access needed]
```

### 5. 状态变化时的警报处理
- 当状态从“正常”变为“异常”或从“异常”变为“正常”时触发警报
- 显示异常发生的次数
- 当系统恢复到正常状态时显示恢复提示信息
- 避免对相同状态重复发送警报

### 6. 权限管理
`requires` 字段列出了用户授予的权限：
- 无权限限制：仅执行基本检查（`curl`, `df`, `pgrep`）
- `["ssh:server1"]`：用户获得了 SSH 访问权限
- `["docker"]`：用户获得了 Docker 访问权限

该功能在执行任何操作前都会先询问用户的权限。