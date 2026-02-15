---
name: codecast
description: 将 Stream 编码代理会话（如 Claude Code、Codex、Gemini CLI 等）通过 webhook 实时传输到 Discord 频道。适用于在调用编码代理时，需要实现透明、可观察的开发会话场景——避免出现“黑箱”效应。该工具能够将 Claude Code 生成的 stream-json 输出解析为格式规范的 Discord 消息，其中包含工具调用、文件操作、bash 命令及执行结果，且完全不消耗任何 AI 许可证（AI tokens）。适用于需要“将会话流式传输到 Discord”、”转发代理输出”或“使开发会话可见”的场景。
metadata: {"openclaw":{"emoji":"🎬","requires":{"anyBins":["unbuffer","python3"]}}}
---

# Codecast

将编程会话实时直播到 Discord 平台。无需消耗任何 AI 令牌。

## 设置

首次使用：请参阅 [references/setup.md](references/setup.md)，了解如何创建 Webhook、安装 unbuffer、获取机器人令牌以及进行测试。

## 使用方法

**⚠️ 必须使用 OpenClaw 的 `nohup` 命令——`exec background:true` 选项可以防止长时间运行的会话在 15-20 秒后被自动终止。**

### 通过 OpenClaw 使用（推荐）

```bash
exec command:"nohup {baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Your task here. When finished, run: openclaw system event --text \"Done: summary\" --mode now' > /tmp/codecast.log 2>&1 & echo PID:\$!"
```

### 直接使用

```bash
bash {baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Your task'
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------------|---------|
| `-w <目录>` | 工作目录 | 当前目录 |
| `-t <秒>` | 超时时间 | 1800 秒 |
| `-h <秒>` | 挂起阈值 | 120 秒 |
| `-n <名称>` | 代理显示名称 | 自动检测 |
| `-r <次数>` | 每 60 秒的发送频率 | 25 次 |
| `--thread` | 将消息发布到 Discord 的特定主题中 | 关闭 |
| `--skip-reads` | 隐藏读取工具相关的事件 | 关闭 |
| `--review <URL>` | PR 审核模式 | 无 |
| `--parallel <文件>` | 并行任务模式 | 无 |
| `--resume <目录>` | 重新播放会话记录 | 无 |

有关 PR 审核、并行任务、Discord 桥接以及 Codex 结构化输出的功能，请参阅 [references/advanced-modes.md](references/advanced-modes.md)。

## 代理启动流程（必填）

每次 OpenClaw 代理启动代码直播会话时，必须执行以下操作：

1. 使用 `nohup` 启动会话，并记录会话的 PID。
2. 将会话信息发布到开发频道，包括代理名称和工作目录。
3. 创建一个定时任务（cron job）来检测会话是否完成，并及时通知相关人员：
   ```
   cron add → every 120000ms → isolated agentTurn →
   "Run: bash {baseDir}/scripts/codecast-watch.sh <PID> <relay-dir>
   If output is STILL_RUNNING → reply HEARTBEAT_OK
   If output starts with ✅ or ❌ or ⚠️ → post the output to <invoking-channel-id>,
   then delete this cron job (cron remove <this-job-id>)"
   ```
4. 将相关信息记录到日志文件中，包括 PID、数据中转目录和定时任务的 ID。

数据中转目录会在启动时显示：`📂 Relay: /tmp/dev-relay.XXXXXX`。

**为什么需要定时任务？** `openclaw 系统事件` 只会处理主会话的状态更新，而不会自动通知正在进行的聊天会话。定时任务是确保频道能够收到代码直播完成通知的唯一可靠方式。

## 提示信息模板

在代理的提示信息中，必须添加完成通知内容：

```
<your task>

When completely finished, run: openclaw system event --text "Done: <brief summary>" --mode now
```

## 代理支持情况

| 代理类型 | 输出格式 | 支持情况 |
|-------|------------|--------|
| Claude Code | stream-json | 完全支持 |
| Codex | --json JSONL | 完全支持 |
| 任何 CLI 工具 | 原始 ANSI 格式 | 基本支持 |

## 会话跟踪信息

- **活跃会话记录**：`/tmp/dev-relay-sessions/<PID>.json`（会话结束后自动删除）
- **事件日志**：`/tmp/dev-relay.XXXXXX/stream.jsonl`（自动清理，保留 7 天）
- **交互式输入记录**：`process:submitsessionId:<id> data:"message"`

## 参考文档

- [设置指南](references/setup.md)：首次安装、Webhook 设置、机器人令牌获取
- [高级功能](references/advanced-modes.md)：PR 审核、并行任务、Discord 桥接、Codex 输出格式
- [Discord 输出格式](references/discord-output.md)：消息格式、系统架构、环境变量、故障排除方法