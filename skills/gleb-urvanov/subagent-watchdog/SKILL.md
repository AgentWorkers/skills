---
name: subagent-watchdog
version: 0.1.0
description: Watchdog for OpenClaw subagent runs: enforce a completion marker by deadline and alert if missing.
---

# 子代理监控工具（Subagent Watchdog）

这是一个用于监控代理工作流程（agentic workflows）的小型可靠性工具。

## 功能说明：
- 在你创建一个带有特定 **标签** 的子代理（subagent）后，会启动一个监控定时器。
- 子代理必须生成一个 **完成标记文件**（completion marker file）。
- 如果定时器到期时该标记文件仍然不存在，监控工具会发出警报（或者以非零状态退出），以便调用者可以重新启动子代理。

## 相关文件：
- `watch.sh` — 监控工具的运行脚本
- `SUBAGENT_CONTRACT.md` — 子代理需要执行的操作说明

## 使用方法：

### 1) 在子代理的命令行中执行任务
告诉子代理执行以下操作：
- 将所有结果写入指定的项目文件中；
- 生成完成标记文件：`subagent-watchdog/state/<label>.done`

### 2) 启动监控工具
```bash
# explicit wait (seconds)
./watch.sh "my-subagent-label" 601

# or omit wait_seconds to read from ~/.openclaw/openclaw.json:
#   caliban.subagentWatchdog.maxRuntimeSeconds (+1 second)
./watch.sh "my-subagent-label"
```

## 通知机制
默认情况下，`watch.sh` 会输出失败信息，并尝试使用 OpenClaw 消息传递系统进行通知（前提是 `OPENCLAW_BIN` 和 `WATCHDOGCHAT_ID` 已被设置）。

**配置文件读取（可选）：**
- 从 `OPENCLAW_CONFIG_PATH` 或 `~/.openclaw/openclaw.json` 文件中读取 `caliban.subagentWatchdog.maxRuntimeSeconds` 的配置值。

该工具具有较高的灵活性：无论是否使用 OpenClaw 消息传递系统，都可以正常使用。