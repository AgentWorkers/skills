---
name: codex-cli-task
description: "在后台异步运行 OpenAI Codex CLI，并自动将结果发送到 Telegram/WhatsApp。适用于编码、代码重构、代码库研究、文件生成以及复杂的多步骤自动化任务。不适用于快速的一次性查询或实时交互式任务。该工具具备严格的安全性机制（线程安全）以及端到端（E2E）的操作验证工作流程。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires":
          {
            "bins": ["codex", "python3"],
            "pythonModules": ["requests"],
            "config": ["gateway.auth.token", "gateway.tools.allow", "tools.sessions.visibility"],
          },
        "config": { "stateDirs": ["~/.openclaw"] },
      },
  }
---
# Codex代码任务（异步）

在后台运行OpenAI Codex CLI——任务执行期间不消耗任何OpenClaw令牌。结果会自动发送到WhatsApp或Telegram。

## 重要提示：Codex是一个通用AI代理

Codex不仅仅是一个编码工具。在`codex exec`模式下，它是一个具有文件访问权限、shell执行能力、可选网络搜索功能以及深度推理能力的通用AI代理。

你可以使用它来：
- **进行研究**：进行网络搜索、内容合成、竞争分析、编写用户体验报告
- **编码**：创建工具、脚本、API、重构代码库
- **分析**：读取和分析文件、数据、日志、源代码
- **内容生成**：编写文档、报告、摘要
- **自动化**：执行需要文件系统访问的复杂多步骤工作流程

向它发出指令时，就像与一个智能人类交流一样使用自然语言，重点是要完成什么任务，而不是如何完成任务。

**不适用于：**
- 简单的问题
- 需要实时互动的任务

## 快速入门

## “运行测试”在此任务中的含义（非常重要）

当用户请求如下内容时：
- “прогони все тесты”
- “run tests”
- “проверь что всё работает”

这意味着要**运行`run-task.py`的完整端到端（E2E）操作验证流程**，包括路由和通知功能。

默认情况下，这**不**仅指简单的`pytest`/`unittest`测试。

**所需行为：**
1. 首先运行路由验证（`--validate-only`）。
2. 通过`nohup`启动烟雾测试（smoke test）/端到端场景，并使用基于文件的提示进行操作。
3. 通过正常的异步流程等待任务完成，而不是在同一轮次中阻塞。
4. 根据端到端的标准报告任务是否成功：包括路由、心跳信号、任务中途更新以及任务完成后的通知。

请参考**[references/testing-protocol.md]**文档以及下面的**完整端到端测试（参考）**部分。

## 异步边界规则（强制要求）

`run-task.py`是一个异步编排工具。

成功启动`nohup`后，正确的行为是：
1. 发送一个简短的启动确认信息（包含进程ID/日志/会话信息）。
2. **立即停止当前轮次的操作**。
3. 只有在相同会话中收到唤醒/完成事件时，才继续执行后续操作。

**不要**在同一轮次中持续等待Codex任务完成。
**不要**在没有用户明确要求实时监控的情况下进行轮询和总结。

**错误做法：**
- ❌ 启动`run-task.py`后继续响应，仿佛任务会在这轮次中完成。

**正确做法：**
- ✅ 启动`run-task.py` → 确认启动 → 停止 → 等待唤醒事件。

## 启动确认机制（强制要求）

在获得**确认启动成功的证据**之前，**切勿**声称任务已经启动。

**所需的确认证据包括：**
1. `nohup`命令返回了进程ID。
2. 进程仍在运行（`ps -p <PID>`）。
3. 运行日志中包含`🔧 Starting OpenAI Codex...`或类似的启动标记。
4. 对于通过Telegram线程执行的任务，路由已经过验证（`--validate-only`）。

如果启动失败并显示`❌ Invalid routing`错误：
- 通过`sessions_list`解决问题。
- 如有需要，使用明确的路由/会话参数重新运行任务。
- 重新检查确认证据。
- 确认无误后，再发送启动确认信息。

## 启动前的计划说明（强制要求）

在启动Codex之前，需要在聊天中发布一个简短的计划：
- 你打算如何完成任务。
- 你期望这次任务的结果是什么。
- 你有哪些假设需要澄清。
- 你是否需要分阶段进行任务，还是只需要一次完成。

如果需要分阶段进行任务，请明确说明这是“第一阶段”，以及什么信号将决定进入第二阶段。

## Telegram线程安全（必须遵守）

对于通过Telegram线程执行的任务，`run-task.py`的设计是：要么正确路由，要么立即失败。

### 启动前的必经步骤

首先确定**当前的运行会话键**，然后使用该键来启动任务：
- 通过`sessions_list`或运行时上下文获取当前会话键。
- 如果会话键是`agent:main:main:thread:<THREAD_ID>`，则直接在`--session`参数中使用它。
- **切勿**从`chat_id`或发送者信息中推导出`--session`参数。

### 规则：
- 对于线程任务，仅使用`--session "agent:main:main:thread:<THREAD_ID>"`。
- **切勿**对线程任务使用`agent:main:telegram:user:<id>`。
- 如果路由元数据不一致，脚本会以`❌ Invalid routing`错误退出。
- 默认模式是`--telegram-routing-mode auto`。
- 使用`--telegram-routing-mode thread-only`强制只进行线程操作。
- 使用`--telegram-routing-mode allow-non-thread`或`--allow-main-telegram`强制进行非线程操作。

**注意：** 必须通过`nohup`启动任务，因为否则执行超时会导致进程终止。

**注意：** **切勿** 将任务文本直接放入shell命令中**，请先将提示信息保存到文件中，然后使用`$(cat file)`来执行命令。

### WhatsApp

```bash
# Step 1: Save prompt to a temp file
write /tmp/codex-prompt.txt with your task text

# Step 2: Launch with $(cat ...)
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:whatsapp:group:<JID>" \
  --timeout 900 \
  > /tmp/codex-run.log 2>&1 &
```

### Telegram（线程安全，默认设置）

```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 900 \
  > /tmp/codex-run.log 2>&1 &
```

> **切勿** 对于线程测试/执行任务，使用`agent:main:telegram:user:<id>`。

### Telegram线程模式（一对一私信）

当在Telegram中使用线程模式时，每个线程都有其自己的会话键，例如`agent:main:main:thread:369520`。

**新的故障安全机制：** `run-task.py`现在强制执行严格的线程路由规则：
- 如果`--session`参数中包含`:thread:<id>`，除非同时解析出Telegram目标和线程会话UUID，否则脚本将拒绝启动。
- 脚本会尝试从`sessions_list`中自动解析缺失的值。
- 如果会话不活跃且API无法返回，脚本会回退到本地会话文件：`~/.openclaw/agents/main/sessions/*-topic-<thread_id>.jsonl`。
- 如果提供的`--notify-session-id`与会话键不匹配，脚本会退出并显示错误。
- 结果：如果路由错误，启动或心跳信号会直接发送到主聊天频道。

使用`--notify-session-id`来唤醒特定的线程会话：
```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:369520" \
  --timeout 900 \
  > /tmp/codex-run.log 2>&1 &
```

当`--session`参数中包含`:thread:<id>`时，所有5种通知类型都会发送到私信线程：
- `--notify-session-id`——可选的覆盖参数，通常会从会话元数据或文件中自动解析。
- `--notify-thread-id`——可选的覆盖参数，通常会从`--session`参数中自动提取。
- `--reply-to-message-id`——可选的调试字段，用于私信线程的路由。
- `--validate-only`——仅用于验证路由并退出（不执行Codex任务）。使用此参数可以安全地验证线程启动参数。
- `--notify-channel`——可选的通道提示（`telegram`/`whatsapp`），目标会话会自动从会话元数据中解析。
- `--timeout`——最大运行时间（以秒为单位，默认为7200秒，即2小时）。
- `--completion-mode`——可选的旧版提示参数（默认为`single`，如果需要迭代则使用`iterate`）。
- `--max-iterations`——在使用迭代模式时的可选参数，用于控制迭代次数。
- `--trace-live`——在聊天/线程中输出实时技术跟踪信息（调试模式）。
- 始终将标准输出/标准错误输出重定向到日志文件。

### 为什么使用基于文件的提示？

研究或复杂的提示可能包含单引号、双引号、Markdown格式或反引号，这些都会影响shell命令的解析。将提示信息保存到文件中，然后通过`$(cat ...)`来执行命令，可以避免所有与引号相关的问题。

## 通道检测

`detect_channel()`函数用于确定通知发送的目标通道：
1. **确定性自动解析**——目标会话会从会话元数据或会话键中自动解析。
2. **WhatsApp自动检测**——如果会话键包含`@g.us`（WhatsApp群组JID），则使用WhatsApp通道。
3. **如果Telegram目标无法解析，立即失败**——脚本会以`❌ Invalid routing`错误退出，而不会无声地发送错误通知。

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
│    Agent    │ ──────────────▶│  run-task.py  │
│ (OpenClaw)  │                │  (detached)   │
└─────────────┘                └──────┬───────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │    Codex      │
                               │ codex exec    │
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

### WhatsApp通知流程

- 每60秒发送一次心跳信号 → 直接发送到WhatsApp。
- 最终结果 → 直接发送到WhatsApp，并通过`sessions_send`发送。
- 代理接收完成结果后进行处理 → 然后发送总结信息。

### 迭代继续模式（唤醒机制）

`--completion-mode`是一个可选参数，用于指示行为：
- `single`：执行一次任务 → 发送总结信息 → 停止。
- `iterate`：执行一次任务 → 发送总结信息 → 在仍有未完成的部分时继续执行下一次迭代。

在`iterate`模式下：
- 对Codex的结果做出简要反应。
- 评估任务是否完成。
- 如果还有未完成的部分：说明下一步的修复措施，并执行下一次迭代。
- 如果任务已完成：报告最终结果并停止。

### 确定性唤醒机制（防止重复）

- 每次任务都会携带`run_id`和`wake_id`。
- `run-task.py`会在`/tmp/codex-orchestrator-state-<hash>.json`文件中保存每个项目的状态。
- 重复或过时的唤醒请求会被跳过。

### 不允许无声启动（始终开启）

- **禁止**无声启动（即使在调试模式下也不允许）。
- 在唤醒时，代理必须先发送一个可见的决策信息：
  - `[TRACE][AGENT][WAKE_RECEIVED] ...`
  - `[TRACE][AGENT][DECISION] continue|stop ...`
- 只有在发送了这个可见的决策信息后，才能启动下一次Codex任务。

### Telegram通知流程（私信线程模式）

1. 🚀 **启动通知** → 线程收到通知 → （无声；使用`send_telegram_direct`发送；包含`Resume: <session-id|new>`）
2. ⏳ **心跳信号**（每60秒一次） → 线程收到通知 → （无声；使用`send_telegram_direct`发送）
3. 📡 **Codex任务中途更新** → 线程收到通知 → （通过`/tmp/codex-notify-{pid}.py`文件；Codex会在文件前缀中添加`📡 🟢 Codex: `）
4. ✅/❌/⏰/💥 **结果通知** → 线程收到通知 → （使用`send_telegram_direct`发送；结果以`<blockquote expandable>`格式显示在聊天中）

`send_telegram_direct()`是所有针对线程的目标通知的核心机制。它直接调用`apiTelegram.org`，并使用`message_thread_id`参数，从而绕过了OpenClaw的消息工具（该工具无法从外部会话上下文直接发送通知到私信线程）。

**备用方案**：如果代理唤醒失败（例如会话被锁定或忙碌），`already_sent=True`会被设置，以防止重复通知。

### 关键细节：WhatsApp与Telegram的通知方式

**WhatsApp：** 直接发送原始结果（用户可以立即看到），然后通过`sessions_send`唤醒代理进行后续处理。
**Telegram：** 结果首先通过`send_telegram_direct`发送，然后通过`openclaw agent --session-id --deliver`唤醒代理，以便在聊天中显示后续操作。这是为了实现“同一个代理，同一个对话”的效果。

**为什么不对Telegram使用`sessions_send`？** 由于架构设计的原因，`sessions_send`在HTTP `/tools/invoke`的拒绝列表中被禁止使用。`openclaw agent` CLI可以绕过这个限制。

### Telegram私信线程与论坛群组

Telegram有两种不同的线程模型。对于`run-task.py`来说，关键在于如何将消息路由到正确的线程：
- OpenClaw的`message`工具的`threadId`参数是**Discord专用的**，在Telegram中无效。
- 目标格式`"chatId:topic:threadId"`会被消息工具的目标解析器拒绝。
- 会话自动路由功能仅在活跃的会话中有效——外部脚本没有会话上下文。
- **解决方案：** `send_telegram_direct()`直接调用`apiTelegram.org`，并使用`message_thread_id`参数。

**私信线程模式（机器人-用户私聊）：**
- 所有通知都使用`send_telegram_direct(chat_id, text, thread_id=..., parse_mode=...)`。
- `thread_id`会从会话键`*:thread:<id>`中自动提取。
- 启动和完成操作都使用`parse_mode="HTML"`格式，并在提示中添加`<blockquote expandable>`标签。
- 心跳信号和任务中途更新都使用`parse_mode=None`格式（纯文本，以避免Markdown解析错误）。
- **注意`parse_mode="Markdown"`的情况**：如果消息包含`**text`（CommonMark格式），Telegram可能会因为Markdown解析问题而拒绝接收。
- **`replyTo`参数的注意事项**：结合`replyTo`和`message_thread_id`可能会导致Telegram无法正确接收消息或路由错误。
- 代理的后续回复会通过`openclaw agent --session-id <uuid> --deliver`发送到聊天中，以便用户在聊天中看到相同的对话内容。

**论坛群组：**
- 使用`send_telegram_direct()`方法；`message_thread_id`是论坛主题的标准格式。
- `send_telegram_direct()`方法可以从会话键`*:thread:<id>`中自动提取。

**Codex任务中的注意事项：**
- **不要**在任务提示中嵌入机器人令牌或curl命令。
- `run-task.py`会在启动Codex之前将提示信息保存到`/tmp/codex-notify-{pid}.py`文件中。
- 任务提示前会加上`[Automation context: ... python3 /tmp/codex-notify-{pid}.py 'msg' ...]`。
- Codex会像执行本地脚本一样调用这个文件。
- 脚本会在所有消息前自动添加`📡 🟢 Codex: `前缀`。

## 可靠性特性

### 超时设置（默认2小时）
- `--timeout 7200`：超过7200秒后，发送SIGTERM信号，等待10秒后发送SIGKILL信号。
- 超时通知会包含工具调用次数和最后一次活动信息，并发送到指定通道。
- 部分输出会被保存到文件中。

### 防崩溃机制
- 使用`try/except`语句包围整个主程序，确保在任何失败情况下都会发送崩溃通知。
- 无论发生什么错误，都会尝试通过通道通知和代理唤醒机制进行通知。

### 进程ID跟踪
- 进程ID会被写入`skills/codex-cli-task/pids/`文件中。
- 过期的进程ID会在启动时被清除。
- 可以通过`ls skills/codex-cli-task/pids/`查看正在运行的任务。

### 静音模式（仅适用于Telegram）
Telegram支持静音通知（无声音提示）。

当前政策：**所有Codex通知在Telegram中都是静音的**：
- 心跳信号 → `silent=True`。
- 启动通知 → `silent=True`。
- 任务中途更新（`📡 🟢 Codex`） → `silent=True`。
- 最终结果 → `silent=True`。
- 唤醒通知 → `silent=True`。

WhatsApp不支持静音模式。

### 通知类型

| 事件 | 表情符号 | WhatsApp通知方式 | Telegram通知方式 | 是否通过私信线程发送？ |
|-------|-------|-------------------|-------------------|------------|
| 启动 | 🚀 | 使用`send_channel`（Markdown格式） | 使用`send_telegram_direct`（HTML格式，静音） | ✅ 使用`message_thread_id` |
| 心跳信号 | ⏳ | 使用`send_channel`（Markdown格式） | 使用`send_telegram_direct`（纯文本，静音） | ✅ 使用`message_thread_id` |
| Codex任务中途更新 | 📡 | 不发送通知 | 通过`/tmp/codex-notify-{pid}.py`文件发送（Bot API，静音） | ✅ 使用`message_thread_id` |
| 成功 | ✅ | 使用`send_channel`和`sessions_send` | 使用`send_telegram_direct`（HTML格式） | ✅ 使用`message_thread_id` |
| 错误 | ❌ | 使用`send_channel`和`sessions_send` | 使用`send_telegram_direct`（HTML格式） | ✅ 使用`message_thread_id` |
| 超时 | ⏰ | 使用`send_channel`和`sessions_send` | 使用`send_telegram_direct`（HTML格式） | ✅ 使用`message_thread_id` |
| 崩溃 | 💥 | 使用`send_channel`和`sessions_send` | 使用`send_telegram_direct`（HTML格式） | ✅ 使用`message_thread_id` |
| 代理后续回复 | 🤖 | 不发送通知 | 使用`openclaw agent --deliver`唤醒代理 | ✅ 在聊天中显示 |

## Codex CLI参数

- `exec "task"`：非交互式执行任务。
- `resume <session-id> "task"`：继续之前的Codex任务会话。
- `--dangerously-bypass-approvals-and-sandbox`：不显示确认提示。
- `--experimental-json --output-last-message`：实时跟踪任务进度并捕获最终输出。
- `--full-auto`：更安全的自动化模式（可选）。

### 为什么不使用`exec/pty`？
- `exec`命令有2分钟的默认超时设置，可能会导致长时间运行的任务被终止。
- 即使使用`pty:true`，输出中也包含转义字符，难以解析。
- 使用`nohup`和分离的运行进程：更加干净、可靠。

### Git要求

Codex需要一个Git仓库。如果缺少仓库，`run-task.py`会自动初始化。

## Python 3.9兼容性

`run-task.py`使用了`typing`模块中的`Optional[X]`（而不是`X | None`），以确保与Python 3.9兼容。`X | None`这种联合语法需要Python 3.10及以上版本。

```python
# Correct (3.9+)
from typing import Optional
def foo(x: Optional[str]) -> Optional[str]: ...

# Would break on 3.9
def foo(x: str | None) -> str | None: ...
```

## 完整的端到端测试（参考）

当你需要一次性验证**整个流程**时，可以使用这个方法：
- 在源线程中发送启动通知。
- 60秒后发送心跳信号。
- 在源线程中发送Codex任务的中途更新。
- 发送代理的完成结果。
- 发送包含总结信息的唤醒通知。

### 成功的标准

1. 启动消息会在相同的线程中显示（带有可展开的提示信息）。
- 至少在60秒后发送一次心跳信号。
- 至少发送一次任务中途更新（通过`/tmp/codex-notify-<pid>.py`文件）。
- 最终结果会在相同的线程中显示（带有可展开的提示信息）。
- 代理的后续操作会通过`openclaw agent --session-id ... --deliver`发送，并在聊天中显示。

### 标准的完整测试提示格式

- 为了常规测试，保持提示信息简洁。
- 强制设置运行时间超过60秒（使用`sleep 70`），以触发心跳信号。
- 明确指示Codex至少调用两次通知脚本。
- 包含一个结构化的报告，以便于验证输出结果。

### 交互式测试规则（时间限制）

对于`iterate`模式下的测试，只执行一次迭代。
- 第一阶段：故意设置不完整的输出。
- 第二阶段：完成剩余的工作。
- 停止在这里。

**原因：** 这样可以验证迭代过程，而不会使常规测试变成一个复杂的多步骤任务。

### 可见性规则（强制要求）

在“✅ OpenAI Codex completed”和下一个“🚀 OpenAI Codex started”之间，必须在聊天中显示一条用户可见的分析信息：
- 代理必须首先说明完成了哪些工作、还有哪些部分未完成，以及是否继续/停止。
- 只有在显示了这条信息后，才能启动下一次任务。

### 标准的启动流程（最小化模式）

```bash
cat > /tmp/codex-full-test-prompt.txt << 'EOF'
# 1) notify script now
# 2) create test file
# 3) sleep 70 + notify again
# 4) run several shell commands
# 5) return short structured report
EOF

python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-full-test-prompt.txt)" \
  --project /tmp/codex-e2e-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --validate-only

nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-full-test-prompt.txt)" \
  --project /tmp/codex-e2e-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 900 \
  > /tmp/codex-full-test.log 2>&1 &
```

### 验证结果文件

- 引擎日志：`/tmp/codex-full-test.log`
- Codex输出：`/tmp/codex-YYYYMMDD-HHMMSS.txt`
- 会话注册信息保存在`~/.openclaw/codexsessions.json`文件中。

## 长时间运行的任务指导

如果预计Codex任务会运行超过1分钟，请明确要求Codex在运行过程中发送中间进度更新。

**推荐的语句：**
- “开始任务时发送进度更新”。
- “在达到重要里程碑后发送另一次更新”。
- “如果任务超过60秒，至少发送一次心跳信号格式的更新”。

对于通过Telegram线程安全的任务，更新应使用注入的自动化脚本`/tmp/codex-notify-<pid>.py`。

### 标准的启动流程（最小化模式）

```bash
cat > /tmp/codex-full-test-prompt.txt << 'EOF'
# ~10 lines
# 1) use notify helper now
# 2) create a test artifact
# 3) sleep 70 + notify again
# 4) run several shell commands
# 5) return short structured report
EOF

python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-full-test-prompt.txt)" \
  --project /tmp/codex-e2e-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --validate-only

nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-full-test-prompt.txt)" \
  --project /tmp/codex-e2e-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 900 \
  > /tmp/codex-full-test.log 2>&1 &
```

## 示例

### WhatsApp：创建工具

```bash
nohup python3 {baseDir}/run-task.py \
  -t "Create a Python CLI tool that converts markdown to HTML with syntax highlighting. Save as convert.py" \
  -p ~/projects/md-converter \
  -s "agent:main:whatsapp:group:120363425246977860@g.us" \
  > /tmp/codex-run.log 2>&1 &
```

### Telegram：研究代码库（线程安全）

```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 1800 \
  > /tmp/codex-run.log 2>&1 &
```

### Telegram线程模式：Codex任务中的中途更新

`run-task.py`会在启动Codex之前自动创建一个本地通知脚本，这样Codex就可以在提示中不显示机器人令牌的情况下发送进度更新。

```bash
cat > /tmp/codex-prompt.txt << 'EOF'
STEP 1: Write analysis to /tmp/report.txt.

After step 1, send a progress notification using the script from the
automation context above.

STEP 2: Write summary to /tmp/summary.txt.
EOF

nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-prompt.txt)" \
  --project ~/projects/my-project \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --timeout 1800 \
  > /tmp/codex-run.log 2>&1 &
```

> **切勿** 在任务提示中嵌入机器人令牌或原始的curl命令。

> **快速参考：从Telegram私信线程启动任务（最小化模式）**
> ```bash
> python3 {baseDir}/run-task.py \
>   --task "probe" \
>   --project ~/projects/x \
>   --session "agent:main:main:thread:<THREAD_ID>" \
>   --validate-only
>
> nohup python3 {baseDir}/run-task.py \
>   --task "$(cat /tmp/prompt.txt)" \
>   --project ~/projects/x \
>   --session "agent:main:main:thread:<THREAD_ID>" \
>   --timeout 900 \
>   > /tmp/codex-run.log 2>&1 &
> ```
> - 必需参数：`--task`、`--project`、`--session`。
> - `THREAD_ID`会从会话键中自动提取。
> - 如果路由信息不一致或无法解析，脚本会以`❌ Invalid routing`错误退出。
> - 启动/心跳信号/结果通知都会发送到源线程。

### 长时间运行的任务（超时设置）

```bash
nohup python3 {baseDir}/run-task.py \
  -t "Refactor the entire auth module to use JWT tokens" \
  -p ~/projects/backend \
  -s "agent:main:whatsapp:group:120363425246977860@g.us" \
  --timeout 3600 \
  > /tmp/codex-run.log 2>&1 &
```

## 成本

- Codex任务在OpenClaw的实时对话之外运行。
- 任务执行期间不消耗任何OpenClaw令牌。
- Codex的费用取决于你的认证方式。

## 会话恢复

可以恢复Codex会话以继续之前的对话。这适用于以下情况：
- 在之前的研究基础上继续进行后续任务。
- 在超时或中断后继续执行任务。
- 需要上下文信息的多步骤工作流程。

### 恢复会话的ID——关键规则

`--resume`参数接受**Codex会话ID**，而不是`run_id`或`wake_id`。

**正确的参数格式：**

```text
📝 Session registered: <session-id-here>
```

这就是需要传递的参数格式：`--resume <session-id>`。

### 如何恢复会话

当任务完成时，会话ID会被捕获并保存到`~/.openclaw/codexsessions.json`文件中。

```bash
nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/codex-prompt.txt)" \
  --project ~/projects/my-project \
  --session "SESSION_KEY" \
  --resume <session-id> \
  > /tmp/codex-run.log 2>&1 &
```

### 为会话添加标签

使用`--session-label`为会话添加人类可读的名称，以便于追踪。

### 列出最近的会话

```python
from session_registry import list_recent_sessions, find_session_by_label

recent = list_recent_sessions(hours=72)
for session in recent:
    print(f"{session['session_id']}: {session['label']} ({session['status']})")
```

### 何时恢复会话与重新开始任务

**何时恢复会话：**
- 当你需要之前对话的上下文时。
- 当需要基于之前的研究或分析继续执行任务时。
- 当需要从头开始执行任务时（例如，因为之前的上下文可能导致混淆）。

### 处理恢复失败的情况

如果会话ID无效或已过期：
- 向通道发送错误信息，并建议重新开始任务。
- 进程会干净地退出。
- 检查`/tmp/codex-run.log`文件中的错误日志。

**常见的恢复失败原因：**
- 会话ID无效。
- 会话已过期或无法恢复。
- 会话来自错误的上下文或项目。
- 会话ID不正确。

### 示例工作流程

**步骤1：初始研究**

```bash
write /tmp/research-prompt.txt with "Research the codebase architecture for project X"

nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/research-prompt.txt)" \
  --project ~/projects/project-x \
  --session "agent:main:main:thread:<THREAD_ID>" \
  --session-label "Project X architecture research" \
  > /tmp/codex-run.log 2>&1 &
```

**步骤2：查找会话ID**

```bash
tail /tmp/codex-run.log
cat ~/.openclaw/codex_sessions.json | grep "Project X"
```

**步骤3：执行后续操作**

```bash
write /tmp/implement-prompt.txt with "Based on your research, implement the authentication module"

nohup python3 {baseDir}/run-task.py \
  --task "$(cat /tmp/implement-prompt.txt)" \
  --project ~/projects/project-x \
  --session "SESSION_KEY" \
  --resume <session-id-from-step-1> \
  --session-label "Project X auth implementation" \
  > /tmp/codex-run2.log 2>&1 &
```

## 恢复会话时可能出现的问题

当代理的唤醒/继续操作失败时：
- 确认`sessions_send`功能是否启用。
- 确认会话是否可见（设置为`all`）。
- 使用`--validate-only`参数检查Telegram线程的路由是否正确。
- 检查`/tmp/codex-run.log`文件和输出文件。
- 检查会话注册表和输出文件路径。

**常见的失败原因：**
- 会话键错误。
- 无法解析Telegram目标或会话UUID。
- 由于去重机制，重复或过时的唤醒请求被忽略。
- 恢复会话的ID不正确。
- 在长时间运行的任务中，进度更新请求未被调用。

## 当前的稳定行为

这是Codex当前的预期行为：
- 任务完成后，代理会收到继续执行的提示。
- Telegram线程的路由是严格控制的。
- WhatsApp会直接接收结果并唤醒代理。
- 会话恢复会使用从JSON事件流中捕获的会话ID。

当前在这个仓库中验证过的稳定行为包括：
- 使用`--experimental-json`参数执行Codex。
- 使用`--output-last-message`参数捕获输出。
- 在运行逻辑中实现OpenClaw风格的异步启动/心跳信号/完成流程。