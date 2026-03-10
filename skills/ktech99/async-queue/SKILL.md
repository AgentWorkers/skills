---
name: async-queue
description: "通过一个基于文件的队列守护进程，在 OpenClaw 代理之间安排延迟或异步任务。当您需要设置定时提醒或后续处理、向代理发送延迟任务，或者将任何应在延迟后执行的工作放入队列（而非立即执行）时，请使用此方法。不适用于 cron 风格的重复性任务（请使用 openclaw cron），也不适用于需要立即执行的操作。"
version: 1.0.3
security_disclosure: |
  This skill installs a background daemon (macOS launchd) that polls a local queue file every 30s.
  It uses child_process.execSync to invoke the openclaw CLI when firing tasks.
  Files are written to ~/.openclaw/queue/ and ~/.openclaw/extensions/.
  The install.sh script must be run manually — nothing runs automatically on skill install.
  All code is open source and auditable in this skill package.
---
# 异步队列（Async Queue）

这是一个轻量级的、基于文件的任务队列系统，它可以在预定时间将延迟任务发送到任何 OpenClaw 代理节点。该系统由四个主要组件构成：

| 组件          | 功能描述                          |
|-----------------|--------------------------------------------|
| **daemon.js**     | 每 30 秒检查一次 `queue.json` 文件，并通过 `queue-wake` 插件发送待执行的任务 |
| **push.js**     | 用于通过命令行（CLI）添加带有延迟的新任务           |
| **queue-cli.js**     | 用于列出待执行的任务、按任务 ID 取消任务以及查看任务历史记录     |
| **queue-wake**     | OpenClaw 插件，负责接收来自 `daemon.js` 的任务信息，触发系统事件，并确保任务在准确的时间执行 |

---

## 安装（首次使用，macOS 系统）

执行以下操作：
1. 将 `daemon.js` 和 `push.js` 文件复制到 `~/.openclaw/queue/` 目录下。
2. 将 `queue-wake` 插件复制到 `~/.openclaw/extensions/queue-wake/` 目录下。
3. 在 `launchd` 服务中注册 `daemon.js`，使其在登录时自动启动，并在系统崩溃后自动重启。

完成上述步骤后，需要重新启动 OpenClaw 代理服务以使插件生效。

---

## 添加任务

使用以下命令行参数来添加一个任务：
```
python push.js --to=agent:main --task="执行某项操作" --delay=10s --then="执行后续任务"
```

**参数说明：**
- `--to`：代理节点的名称（例如 `main`）。也可以使用完整的会话键格式（如 `agent:main:main`）。此参数为可选；如果设置了 `queue/config.json.defaultTo`，则使用该值；否则默认使用 `marcus`。
- `--task`：任务执行的具体内容。
- `--delay`：任务延迟执行的时长，支持 `10s`、`5m`、`2h`，或绝对时间格式（例如 `HH:MM` 表示 24 小时，`H:MMam` 表示 12 小时）。
- `--then`：可选参数，用于指定在该任务执行完成后立即执行的后续任务。
- `--ttl`：任务未完成时的超时时间（以秒为单位，默认为 300 秒）。

**示例：**
```
python push.js --to=agent:main --task="发送通知" --delay=5m --then="发送确认邮件"
```

---

## 适用场景

- 当用户希望在 X 分钟/小时后收到提醒时。
- 当你需要启动一个子代理或后台任务并后续需要检查其执行情况时。
- 当某个操作需要在延迟后完成时（例如验证部署结果、提醒用户处理待办事项）。
- 当某些任务无法在当前轮次完成，需要稍后继续处理时。

**不适用场景：**
- 需要立即执行的操作（直接执行即可）。
- 需要定期重复执行的任务（使用 `openclaw cron` 更合适）。
- 需要等待用户输入才能执行的任务（直接通知用户即可）。

---

## 数据结构

`queue.json` 文件用于存储任务信息，其结构如下：
```
{
  "tasks": [
    {
      "id": "task1",
      "to": "agent:main",
      "task": "发送邮件",
      "delay": "5m",
      "then": "发送确认邮件",
      "ttl": 300
    },
    {
      // 其他任务信息
    }
  ]
}
```

**注意：** 对于计划执行数小时后的任务，建议适当增加 `ttl` 值，以防止 `daemon.js` 错过执行时机。

---

## 任务执行流程

任务从 `daemon.js` 加入队列，然后通过 `queue-wake` 插件触发，确保任务在预定时间执行。`queue-cli.js` 可用于查看任务状态和执行历史记录。

---

## 查看队列状态

可以使用相应的命令行工具或接口来查看队列中任务的详细信息。

---

## daemon.js 的运行状态（macOS）

`daemon.js` 作为后台进程运行，负责定期检查队列文件并发送任务。在 macOS 系统中，该进程会注册到 `launchd` 服务中，实现自动启动和重启功能。

---

## 安装的文件

- `~/.openclaw/queue/daemon.js`：任务调度守护进程。
- `~/.openclaw/queue/push.js`：用于添加任务的命令行工具。
- `~/.openclaw/queue/queue.json`：队列状态文件。
- `~/.openclaw/queue/daemon.log`：任务执行日志。
- `~/.openclaw/extensions/queue-wake/`：OpenClaw 插件文件。
- `~/Library/LaunchAgents/ai.openclaw.queue-daemon.plist`：`launchd` 服务配置文件。

---

## 协议说明

详细协议请参阅 `references/PROTOCOL.md`，其中包含任务队列的使用规则、超时设置指南以及常见任务模式。