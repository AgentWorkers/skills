---
name: claude-code-task
description: "在后台运行 Claude Code 任务，并自动交付结果。适用于编码任务、代码库中的研究、文件生成以及复杂的自动化操作。在 Claude Code 运行期间，无需消耗任何 OpenClaw 代币。"
---
# Claude Code 任务（异步）

在后台运行 Claude Code — 运行期间不消耗任何 OpenClaw 令牌。结果会自动发送到 WhatsApp 或 Telegram。

## 重要提示：Claude Code 是一个通用 AI 代理

Claude Code 不仅仅是一个编码工具，它是一个功能强大的 AI 代理，具备网页搜索、文件访问和深度推理能力。你可以用它来完成任何复杂的任务：

- **研究** — 网页搜索、内容合成、竞争分析、用户体验报告
- **编码** — 创建工具、脚本、API、重构代码库
- **分析** — 读取和分析文件、数据、日志、源代码
- **内容创作** — 编写文档、演示文稿、报告、摘要
- **自动化** — 需要文件系统访问的复杂多步骤工作流程

使用提示语的方式，就像与聪明的人类交流一样 — 专注于你需要什么，而不是如何去做。

**不适用场景：**
- 快速问题（直接回答即可）
- 需要实时交互的任务

## 快速入门

## Telegram 线程安全（必须遵守）

对于 Telegram 线程的运行，`run-task.py` 被设计为要么正确路由，要么立即失败。

- 仅使用 `--session "agent:main:main:thread:<THREAD_ID>"`
- **切勿** 对于线程任务使用 `agent:main:telegram:user:<id>`
- 如果路由元数据不一致（线程/会话 UUID/目标不匹配），脚本会以 `❌ Invalid routing` 退出
- 默认情况下，主聊天室的 Telegram 联系会被阻止；有意覆盖需要同时设置：
  - `--allow-main-telegram`
  - `ALLOW_MAIN_TELEGRAM=1`

这是有意为之：**快速中止 > 静默的错误路由**

⚠️ **务必通过 nohup 运行** — 执行超时（2 分钟）会终止进程！

⚠️ **切勿将任务文本直接放入 shell 命令中** — 引号、特殊字符和换行符会导致参数解析错误。始终先将提示语保存到文件中，然后使用 `$(cat file)`。

### WhatsApp

```bash
# Step 1: Save prompt to a temp file
write /tmp/cc-prompt.txt with your task text

# Step 2: Launch with $(cat ...)
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:whatsapp:group:<JID>" \
  --timeout 900 \
  > /tmp/cc-run.log 2>&1 &
```

`--session` 关键字（例如 `agent:main:whatsapp:group:120363425246977860@g.us`）用于自动检测 WhatsApp 目标。

### Telegram（线程安全默认设置）

```bash
# ALWAYS use the current thread session key from context:
# agent:main:main:thread:<THREAD_ID>
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 900 \
  > /tmp/cc-run.log 2>&1 &
```

> **切勿** 对于线程测试/运行使用 `agent:main:telegram:user:<id>`。
> 这会路由到主聊天室，可能导致消息偏离原始线程。

### Telegram 线程模式（1:1 私人消息线程）

当在 Telegram 线程模式下使用 Marvin 时，每个线程都有自己的会话关键字，例如 `agent:main:main:thread:369520`。

**故障安全路由（新功能）：** `run-task.py` 现在强制执行严格的线程路由。
- 如果 `--session` 包含 `:thread:<id>`，脚本 **将拒绝启动**，除非确定了 Telegram 目标和线程会话 UUID。
- 它会尝试从 `sessions_list` 中自动解析缺失的值。
- 如果会话不活跃且 API 未返回，它会回退到本地会话文件：`~/.openclaw/agents/main/sessions/*-topic-<thread_id>.jsonl`。
- 如果提供的 `--notify-session-id` 与会话关键字不匹配，它会退出并显示错误。
- 结果：错误路由的启动/心跳消息会在 Claude 启动前被阻止。

使用 `--notify-session-id` 来唤醒特定的线程会话：

```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:369520" \
  --timeout 900 \
  > /tmp/cc-run.log 2>&1 &
```

当 `--session` 关键字包含 `:thread:<id>` 时，所有 5 种通知类型都会路由到 DM 线程 ✅

- `--notify-session-id` — 可选覆盖。通常会从会话元数据/文件中自动解析。
- `--notify-thread-id` — 可选覆盖。通常从 `--session` 中自动提取。
- `--reply-to-message-id` — 可选调试字段；避免用于 DM 线程路由。
- `--validate-only` — 仅解析路由并退出（不运行 Claude）。使用此选项可以安全地验证线程启动参数。

- `--notify-channel` — 可选覆盖（`telegram`/`whatsapp`）
- `--notify-target` — 可选覆盖，用于聊天 ID/JID
- `--timeout` — 最大运行时间（以秒为单位，默认为 7200 = 2 小时）
- 始终将 stdout/stderr 重定向到日志文件

### 为什么使用基于文件的提示语？
研究/复杂的提示语可能包含单引号、双引号、Markdown、反引号 — 这些都会导致 shell 参数解析错误。将提示语保存到文件中，然后使用 `$(cat ...)` 可以避免所有引号问题。

## 聊天室检测

`detect_channel()` 函数决定了通知的发送位置：

1. **CLI 覆盖优先** — 如果同时提供了 `--notify-channel` 和 `--notify-target`，则优先使用这些设置
2. **WhatsApp 自动检测** — 如果会话关键字包含 `@g.us`（WhatsApp 组 JID），则使用 WhatsApp
3. **没有目标** — 如果两者都不适用，则会静默跳过通知

```python
def detect_channel(session_key):
    if NOTIFY_CHANNEL_OVERRIDE and NOTIFY_TARGET_OVERRIDE:
        return NOTIFY_CHANNEL_OVERRIDE, NOTIFY_TARGET_OVERRIDE
    jid = extract_group_jid(session_key)
    if jid:
        return "whatsapp", jid
    return None, None
```

## 工作原理

```
┌─────────────┐     nohup      ┌──────────────┐
│    Agent     │ ──────────────▶│  run-task.py  │
│  (OpenClaw)  │                │  (detached)   │
└─────────────┘                └──────┬───────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │  Claude Code  │  ← runs on Max subscription ($0 API)
                               │  (-p mode)    │
                               └──────┬───────┘
                                      │
                          ┌───────────┼───────────┐
                          ▼           ▼           ▼
                    Every 60s    On complete   On error/timeout
                    ┌────────┐  ┌──────────┐  ┌──────────────┐
                    │ ⏳ ping │  │ ✅ result │  │ ❌/⏰/💥 error│
                    │ silent │  │ channel  │  │   channel    │
                    └────────┘  └──────────┘  └──────────────┘
```

### WhatsApp 通知流程：
1. **心跳信号**（每 60 秒一次）→ 直接发送到 WhatsApp （信息性通知，不会唤醒代理）
2. **最终结果** → 直接发送到 WhatsApp （人类用户立即看到）+ `sessions_send` （代理被唤醒）
3. 代理通过 `sessions_send` 接收到 `[CLAUDE_CODE_RESULT]` → 处理后 → 通过 `message(send)` 发送到 WhatsApp 组
4. 人类用户可以看到：原始结果 + 代理的分析/下一步操作

### Telegram 通知流程（DM 线程模式 — 完整流程）：
1. 🚀 **发送通知** → 线程 ✅（静默；使用 HTML；`<blockquote expandable>` 格式显示提示语）→ 通过 `send_telegram_direct`
2. ⏳ **心跳信号**（每 60 秒一次）→ 线程 ✅（静默；使用纯文本）→ 通过 `send_telegram_direct`
3. 📡 **Claude Code 进度更新** → 线程 ✅（在磁盘上的 Python 脚本 `/tmp/cc-notify-{pid}.py`；通过 `CC` 调用该文件；前缀为 `"📡 🟢 CC: "`）
4. ✅/❌/⏰/💥 **结果通知** → 线程 ✅（使用 HTML；`<blockquote expandable>` 格式显示结果）→ 通过 `send_telegram_direct`
5. 🤖 **代理总结** → 主聊天室 ⚠️（已知限制：`openclaw agent --session-id` 生成的消息没有 `currentThreadTs`；这是可以接受的）

`send_telegram_direct()` 是所有针对线程的通知的核心机制。它直接调用 `apiTelegram.org` 并使用 `message_thread_id` — 完全绕过了 OpenClaw 的消息工具（该工具无法从会话上下文之外路由到 DM 线程）。

**备用方案** — 如果代理唤醒失败（会话被锁定/繁忙）：在直接发送后设置 `already_sent=True`，因此不会重复发送通知。

### 关键细节：Telegram 与 WhatsApp 的通知方式

**WhatsApp：** 直接发送原始结果（人类用户立即看到）+ `sessions_send` 唤醒代理进行分析。

**Telegram：** 结果通过 `send_telegram_direct` 发送 → 然后通过 `openclaw agent --session-id` 唤醒代理（不使用 `--deliver`）。代理通过 `message(action=send)` 发送响应，并回复 `NO_REPLY`。这样可以避免重复通知。

**为什么不对 Telegram 使用 `sessions_send`？** 由于架构设计的原因，`sessions_send` 被 `/tools/invoke` 的拒绝列表所阻止。`openclaw agent` CLI 可以绕过这一限制。

## 可靠性特性

### 超时（默认 2 小时）
- `--timeout 7200` → 超过 7200 秒后：发送 SIGTERM → 等待 10 秒 → 发送 SIGKILL
- 超时通知会包含工具调用次数和最后的活动记录
- 部分输出会保存到文件中

### 防崩溃机制
- 整个主程序都包裹在 `try/except` 中 → 发生崩溃时总会发送通知
- 无论发生什么故障，都会尝试发送聊天室通知和代理唤醒

### PID 跟踪
- PID 会被写入 `skills/claude-code-task/pids/`
- 启动时会清理过时的 PID
- 可以通过 `ls skills/claude-code-task/pids/` 查看正在运行的任务

### 静默模式（仅限 Telegram）
Telegram 支持静默通知（无声音）。这适用于后台/信息性消息：
- 心跳信号 → `silent=True`
- 启动通知 → `silent=True`
- 最终结果 → `silent=False`（默认设置，需要用户注意）

WhatsApp 不支持静默模式 — 对于 WhatsApp，这个标志会被忽略。

### Telegram DM 线程与论坛组

Telegram 有两种不同的线程模型。`run-task.py` 的关键区别在于如何将消息路由到线程。

**外部脚本的核心问题：**
- OpenClaw 的 `message` 工具的 `threadId` 参数是 **Discord 特有的** — 对于 Telegram 被忽略
- 目标格式 `"chatId:topic:threadId"` 被消息工具的目标解析器拒绝
- 会话自动路由（`currentThreadTs`）仅在活动会话中有效 — 外部脚本没有会话上下文
- **解决方案：** `send_telegram_direct()` 完全绕过了消息工具；直接使用 `apiTelegram.org` 和 `message_thread_id`

**DM 线程模式**（机器人-用户私人聊天线程）：
- 所有通知都使用 `send_telegram_direct(chat_id, text, thread_id=..., parse_mode=...)` ✅
- `thread_id` 从会话关键字 `*:thread:<id>` 中自动提取
- 启动和完成时：`parse_mode="HTML"`，并使用 `<blockquote expandable>` 格式显示提示语/结果
- 心跳信号和任务中间更新：`parse_mode=None`（纯文本，避免 Markdown 解析错误）
- **`parse_mode="Markdown"` 的陷阱**：完成消息中包含 `**text**（CommonMark 格式）会导致 Telegram 的 MarkdownV1 抛出 400 错误 — 这会导致消息无法送达
- **`replyTo` 的陷阱**：结合 `replyTo` 和 `message_thread_id` 会导致 Telegram 拒绝请求 → 回退时消息会发送到主聊天室
- 代理总结：`openclaw agent --session-id <uuid>` 用于唤醒线程会话；响应会发送到主聊天室（合成消息中没有 `currentThreadTs`；这是已知的问题）

**Claude Code 进度更新：**
- **切勿在任务提示语中嵌入机器人令牌或 curl 命令** — Claude Code 会将这些视为提示语注入
- `run-task.py` 在启动 Claude Code 之前会将 `/tmp/cc-notify-{pid}.py` 写到磁盘
- 任务提示语前会加上 `[Automation context: ... python3 /tmp/cc-notify-{pid}.py 'msg' ...]`
- Claude Code 会调用该文件（合法的本地脚本格式，不会触发安全警告）
- 脚本会自动在所有消息前加上 `"📡 🟢 CC: "`；在 `finally` 块中清理这些内容

### 通知类型

| 事件 | 表情符号 | WhatsApp 通知方式 | Telegram 通知方式 | 是否为 DM 线程？ |
|-------|-------|-------------------|-------------------|------------|
| 启动 | 🚀 | send_channel (Markdown) | send_telegram_direct (HTML, 静默) | ✅ message_thread_id |
| 心跳信号 | ⏳ | send_channel (Markdown) | send_telegram_direct (纯文本, 静默) | ✅ message_thread_id |
| 任务中间更新 | 📡 | — | /tmp/cc-notify-{pid}.py (Bot API, 静默) | ✅ message_thread_id |
| 成功 | ✅ | send_channel + sessions_send | send_telegram_direct (HTML) + openclaw agent | ✅ message_thread_id |
| 错误 | ❌ | send_channel + sessions_send | send_telegram_direct (HTML) + openclaw agent | ✅ message_thread_id |
| 超时 | ⏰ | send_channel + sessions_send | send_telegram_direct (HTML) + openclaw agent | ✅ message_thread_id |
| 崩溃 | 💥 | send_channel + sessions_send | send_telegram_direct (HTML) + openclaw agent | ✅ message_thread_id |
| 代理总结 | 🤖 | — | openclaw agent 唤醒 | ⚠️ 主聊天室（没有线程上下文） |

## Claude Code 标志

- `-p "task"` — 打印模式（非交互式，输出结果）
- `--dangerously-skip-permissions` — 不显示确认提示
- `--verbose --output-format stream-json` — 实时跟踪心跳信号

### 为什么不使用 exec/pty？
- `exec` 的默认超时为 2 分钟 → 会导致长时间运行的任务被终止
- 即使使用 `pty:true`，输出中也包含转义码，难以解析
- `nohup` + `-p` 模式：干净、分离、可靠

### Git 要求
Claude Code 需要一个 Git 仓库。如果缺少仓库，`run-task.py` 会自动初始化。

## Python 3.9 兼容性

`run-task.py` 使用了 `typing` 中的 `Optional[X]`（而不是 `X | None`），以确保与 Python 3.9 兼容。这种联合语法（`X | None`）需要 Python 3.10 或更高版本。

```python
# Correct (3.9+)
from typing import Optional
def foo(x: Optional[str]) -> Optional[str]: ...

# Would break on 3.9
def foo(x: str | None) -> str | None: ...
```

## 完整的端到端测试（参考）

当你需要一次性验证 **整个流程** 时，请使用此方法：
- 在源线程中发送通知
- 超过 60 秒后发送心跳信号
- Claude 在任务中间更新进度（📡 🟢 CC）
- 在源线程中显示最终结果
- 尝试唤醒代理并显示总结

### 通过标准
1. 启动消息出现在同一线程中（带有可展开的提示语）
2. 至少在 60 秒后出现一个心跳信号
3. 至少出现一次任务中间的更新（通过 `/tmp/cc-notify-<pid>.py`）
4. 最终结果出现在同一线程中（带有可展开的结果提示语）
5. 尝试唤醒代理（`openclaw agent --session-id ...`），并且不会重复显示最终结果

### 标准的完整测试提示语格式
- 保持提示语 **简洁**（大约 10 行），以便进行常规测试
- 确保提示语长度 **超过 4500 个字符**，以验证 Telegram 中的提示语截断/折叠行为
- 强制运行时间超过 60 秒（`sleep 70`），以触发心跳信号
- 明确指示 Claude 至少调用两次通知脚本
- 包含一个简短的结构化报告，以便于验证输出

### 标准的启动方式（最小模式）
```bash
cat > /tmp/cc-full-test-prompt.txt << 'EOF'
# ~10 lines, but total >4500 chars:
# 1) notify script now
# 2) create test file with repeated text (to exceed 4500 chars)
# 3) sleep 70 + notify script again
# 4) run several shell commands
# 5) return short structured report
EOF

python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-full-test-prompt.txt)" \
  --project /tmp/cc-e2e-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --validate-only

nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-full-test-prompt.txt)" \
  --project /tmp/cc-e2e-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 900 \
  > /tmp/cc-full-test.log 2>&1 &
```

### 验证文件
- 包装日志：`/tmp/cc-full-test.log`
- Claude 输出：`/tmp/cc-YYYYMMDD-HHMMSS.txt`
- 会话注册信息存储在 `~/.openclaw/claude_sessions.json` 中

## 示例

### WhatsApp：创建一个工具
```bash
nohup python3 {baseDir}/run-task.py \
  -t "Create a Python CLI tool that converts markdown to HTML with syntax highlighting. Save as convert.py" \
  -p ~/projects/md-converter \
  -s "agent:main:whatsapp:group:120363425246977860@g.us" \
  > /tmp/cc-run.log 2>&1 &
```

### Telegram：研究代码库（线程安全）
```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 1800 \
  > /tmp/cc-run.log 2>&1 &
```

### Telegram 线程模式：研究代码库
```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:369520" \
  --timeout 1800 \
  > /tmp/cc-run.log 2>&1 &
# thread_id auto-extracted from session key
# target + session UUID auto-resolved from API/local session files
```

### Telegram 线程模式：Claude Code 的任务中间更新

`run-task.py` 会在启动 Claude Code 之前自动创建一个磁盘上的通知脚本，这样就可以在发送进度更新时避免在提示语中显示机器人令牌（这会触发安全拒绝）：

```bash
# Just write a normal task prompt — run-task.py handles the rest
cat > /tmp/cc-prompt.txt << 'EOF'
STEP 1: Write analysis to /tmp/report.txt (600+ words)...

After step 1, send a progress notification using the script from the
automation context above: python3 /tmp/cc-notify-<PID>.py "Step 1 done."

STEP 2: Write summary to /tmp/summary.txt...
EOF

nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 1800 \
  > /tmp/cc-run.log 2>&1 &
# run-task.py writes /tmp/cc-notify-{pid}.py before launch
# Prepends "[Automation context: use python3 /tmp/cc-notify-{pid}.py 'msg']" to task
# Claude Code calls the file; prefix "📡 🟢 CC: " auto-added; file cleaned up on exit
```

> ⚠️ **切勿在任务提示语中嵌入机器人令牌或 curl 命令** — Claude Code 会正确地将硬编码的令牌和外部 API 调用识别为提示语注入，并拒绝这些行为。请使用上述的磁盘脚本模式。

> **快速参考：从 Telegram DM 线程启动（最小模式）**
> ```bash
> # 1) Validate routing first (no Claude run)
> python3 {baseDir}/run-task.py \
>   --task "probe" \
>   --project ~/projects/x \
>   --session "agent:main:main:thread:<THREAD_ID>" \
>   --validate-only
>
> # 2) Real launch (only 3 required params)
> nohup python3 {baseDir}/run-task.py \
>   --task "$(cat /tmp/prompt.txt)" \
>   --project ~/projects/x \
>   --session "agent:main:main:thread:<THREAD_ID>" \
>   --timeout 900 \
>   > /tmp/cc-run.log 2>&1 &
> ```
> - 必需参数：`--task`、`--project`、`--session`
- 安全性：默认情况下，不包含 `:thread:<id>` 的请求会被阻止（`❌ Unsafe routing blocked`）
- 如果需要故意发送到 Telegram 主聊天室，请设置 `--allow-main-telegram` 并设置环境变量 `ALLOW_MAIN_TELEGRAM=1`
- `THREAD_ID` 会从会话关键字中自动提取
- 目标和会话 UUID 会自动解析（先通过 API，然后回退到本地会话文件）
- 如果路由不一致或未解析，脚本会在运行前以 `❌ Invalid routing` 退出
- `run-task` 的所有通知（启动/心跳信号/结果）都会留在源线程中 ✅

### 延长超时的长时间任务
```bash
nohup python3 {baseDir}/run-task.py \
  -t "Refactor the entire auth module to use JWT tokens" \
  -p ~/projects/backend \
  -s "agent:main:whatsapp:group:120363425246977860@g.us" \
  --timeout 3600 \
  > /tmp/cc-run.log 2>&1 &
```

## 成本

- Claude Code 的使用费用为每月 200 美元（不包括 API 令牌）
- Claude Code 运行期间不消耗任何 OpenClaw API 费用
- 唯一的费用是消息发送和代理的简要响应时间

## 会话恢复

Claude Code 的会话可以恢复，以便继续之前的对话。这适用于以下情况：
- 在之前的研究基础上进行后续任务
- 在超时或中断后继续执行
- 需要上下文的多步骤工作流程

### 如何恢复

当任务完成时，会话 ID 会自动捕获并保存到注册表（`~/.openclaw/claude_sessions.json`）中。

要恢复会话，请使用 `--resume` 标志：

```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-prompt.txt)" \
  --project ~/projects/my-project \
  --session "SESSION_KEY" \
  --resume <session-id> \
  > /tmp/cc-run.log 2>&1 &
```

### 会话标签

使用 `--session-label` 为会话分配易于人类阅读的名称，以便于追踪：

```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/cc-prompt.txt)" \
  --project ~/projects/my-project \
  --session "SESSION_KEY" \
  --session-label "Research on Jackson Berler" \
  > /tmp/cc-run.log 2>&1 &
```

### 列出最近的会话

代理可以读取会话注册表来找到最近的会话：

```python
# Python code (for agent automation)
from session_registry import list_recent_sessions, find_session_by_label

# List sessions from last 72 hours
recent = list_recent_sessions(hours=72)
for session in recent:
    print(f"{session['session_id']}: {session['label']} ({session['status']})")

# Find session by label (fuzzy match)
session = find_session_by_label("Jackson")
if session:
    print(f"Found: {session['session_id']}")
```

或者手动检查注册表：

```bash
cat ~/.openclaw/claude_sessions.json
```

### 何时恢复 vs 从头开始

**何时恢复：**
- 当你需要之前的对话上下文时
- 在之前的研究/分析基础上继续工作时
- 在中断后继续执行
- 需要进一步澄清或进行下一步操作时

**何时从头开始：**
- 当任务完全不相关时
- 之前的会话是探索性的/实验性的
- 你希望重新开始
- 之前的会话上下文可能导致混淆

### 恢复失败处理

如果会话 ID 无效或过期：
- 会向聊天室发送错误消息，并建议重新开始
- 进程会干净地退出（不会保留部分工作）
- 详细信息可以在 `/tmp/cc-run.log` 中查看

常见的恢复失败原因：
- 会话过期（Claude Code 有会话保留限制）
- 无效的会话 ID（输入错误、格式错误）
- 会话来自不同的项目/上下文

### 示例工作流程

**步骤 1：初步研究**
```bash
# Save prompt
write /tmp/research-prompt.txt with "Research the codebase architecture for project X"

# Launch task (Telegram thread-safe example)
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/research-prompt.txt)" \
  --project ~/projects/project-x \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --session-label "Project X architecture research" \
  > /tmp/cc-run.log 2>&1 &
```

**步骤 2：检查结果并找到会话 ID**
```bash
# Session ID printed in stderr: "📝 Session registered: <id>"
tail /tmp/cc-run.log

# Or read from registry
cat ~/.openclaw/claude_sessions.json | grep "Project X"
```

**步骤 3：后续实施**
```bash
# Save follow-up prompt
write /tmp/implement-prompt.txt with "Based on your research, implement the authentication module"

# Resume session
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/implement-prompt.txt)" \
  --project ~/projects/project-x \
  --session "SESSION_KEY" \
  --resume <session-id-from-step-1> \
  --session-label "Project X auth implementation" \
  > /tmp/cc-run2.log 2>&1 &
```

## 文件

```
skills/claude-code-task/
├── SKILL.md              # This file
├── run-task.py           # Async runner with notifications
├── session_registry.py   # Session metadata storage
└── pids/                 # PID files for running tasks (auto-managed)
```