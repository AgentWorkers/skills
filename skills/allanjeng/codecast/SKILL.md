---
version: 4.1.0
name: codecast
description: 通过 Webhook 将 Stream 编码代理会话（如 Claude Code、Codex、Gemini CLI 等）实时传输到 Discord 频道。适用于在调用编码代理时，需要透明且可观察的开发会话场景——避免出现“黑箱”现象。该工具能够将 Claude Code 生成的 stream-json 输出解析为格式清晰的 Discord 消息，显示工具调用、文件操作、bash 命令及其执行结果，且不会消耗任何 AI 许可证（AI tokens）。适用于需要“将会话流式传输到 Discord”、“转发代理输出”或“使开发会话可见”的场景。
metadata: {"openclaw":{"emoji":"🎬","requires":{"anyBins":["unbuffer","python3"]}}}
---
# Codecast

将编程会话实时直播到 Discord 平台，且不会消耗任何 AI 令牌。

## 设置

首次使用：请参考 [references/setup.md](references/setup.md) 以了解如何创建 Webhook、安装 unbuffer、获取机器人令牌以及进行测试。

## 启动

使用 `exec background:true` 命令启动该工具。后台执行的会话会在代理轮换时持续运行，当进程结束时，OpenClaw 会自动触发 `notifyOnExit` 事件。

```bash
exec background:true command:"{baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Your task here'"
```

请注意响应中返回的会话 ID，您可以使用该 ID 通过 `process` 命令来监控会话状态。

### 参数选项

| 参数 | 说明 | 默认值 |
|------|------------|---------|
| `-w <dir>` | 工作目录 | 当前目录 |
| `-t <sec>` | 超时时间 | 1800 秒 |
| `-h <sec>` | 挂起阈值 | 120 秒 |
| `-n <name>` | 代理显示名称 | 自动检测 |
| `-r <n>` | 每 60 秒的发送频率 | 25 次 |
| `--thread` | 将消息发布到 Discord 线程 | 关闭 |
| `--skip-reads` | 隐藏读取工具的事件 | 关闭 |
| `--review <url>` | PR 审查模式 | 无 |
| `--parallel <file>` | 并行任务模式 | 无 |
| `--resume <dir>` | 重新播放会话 | 无 |

有关 PR 审查、并行任务、Discord 桥接以及 Codex 结构化输出的功能，请参阅 [references/advanced-modes.md](references/advanced-modes.md)。

## 代理启动流程

1. **启动后台会话** → 记录响应中返回的会话 ID 和进程 ID (PID)。
2. **向开发频道发送消息** → 公布代理名称、工作目录和当前任务。
3. **生成面包屑路径 (Breadcrumb)**，用于在会话完成后发布结果：  
   ```bash
   echo '{"channel":"<invoking-channel-id>","relayDir":"<relay-dir>","pid":<PID>}' > /tmp/codecast-pending-<PID>.json
   ```
4. **将日志记录到每日存储目录** → 包括会话 ID、中继目录和调用频道信息。

面包屑路径文件用于指示在会话完成后应向何处发布结果。系统会通过检查 PID 是否仍然存在来判断会话是否已完成。

当进程结束时，OpenClaw 的 `notifyOnExit` 事件会被触发，系统会读取中继目录下的 `stream.jsonl` 文件，并将结果发布到调用频道。

## 完成检测

OpenClaw 会自动处理完成检测：
- 默认设置：`tools.exec.notifyOnExit: true` — 进程退出时触发系统事件和心跳检测。
- 心跳检测脚本会通过 `/tmp/dev-relay-sessions/` 目录来检测已完成的会话。
- 无需使用 cron 任务来监控会话状态。

**备用提示：** 可将以下代码添加到代理的提示信息中，以提供额外的完成信号：  
```
When completely finished, run: openclaw system event --text "Done: <brief summary>" --mode now
```

## 监控

```
process poll sessionId:<id>        # Check status
process log sessionId:<id>         # View recent output
process kill sessionId:<id>        # Stop session
```

## 代理支持

| 代理类型 | 输出格式 | 支持情况 |
|-------|------------|--------|
| Claude Code | stream-json | 完全支持 |
| Codex | --json JSONL | 完全支持 |
| 任何 CLI 工具 | 原始 ANSI 格式 | 基本支持 |

## 会话跟踪

- **活跃会话**：`/tmp/dev-relay-sessions/<PID>.json`（会话结束后自动删除）
- **事件日志**：`/tmp/dev-relay.XXXXXX/stream.jsonl`（自动清理，保留 7 天）
- **交互式输入**：`process submit sessionId:<id> data:"message"`  

## 参考文档

- [设置指南](references/setup.md) — 首次安装、Webhook 设置、机器人令牌配置
- [高级功能](references/advanced-modes.md) — PR 审查、并行任务、Discord 桥接、Codex 输出格式
- [Discord 输出格式](references/discord-output.md) — 消息格式、系统架构、环境变量及故障排除方法