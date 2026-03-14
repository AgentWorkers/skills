---
name: workstation
version: 1.0.0
description: "**控制各种工作站会话（Claude Code的多会话编排功能）**  
**使用场景：**  
1. 用户希望开始、继续或暂停编码项目；  
2. 检查会话状态；  
3. 向某个会话发送命令；  
4. 列出所有活跃的会话；  
5. 创建新的会话；  
6. 用户对计划批准或问题通知进行回复；  
7. 用户希望停止、取消或中断当前会话；  
8. 用户需要获取会话或屏幕的截图。  
**触发条件：**  
- 开始工作；  
- 继续会话；  
- 新会话的创建；  
- 会话的启动或暂停；  
- 工作站的状态变化；  
- 项目名称的变更；  
- 计划的批准或拒绝；  
- 用户的选择操作（如“是”、“否”、“停止”、“取消”等）；  
- 其他与会话相关的操作（如截图、显示会话内容等）。"
homepage: "https://github.com/varie-ai/workstation"
metadata:
  openclaw:
    emoji: "🖥️"
    requires:
      bins:
        - wctl
---
# 工作站控制

通过 `wctl` 来控制各种工作站编码会话。

## 第0步：检查待处理的提示（务必首先执行此操作）

在进行任何路由或会话操作之前，检查是否有会话正在等待用户输入：

```bash
cat ~/.openclaw/workspace/pending-prompts.json 2>/dev/null || echo '{"prompts":[]}'
```

**如果 `prompts` 数组非空** 且用户的消息看起来像是回复（数字、"approve"、"yes"、"no"、"reject"、简短回答，或提到了待处理列表中的项目）：
→ 这是对待处理提示的回复。直接进入下面的“响应会话提示”部分。

**如果 `prompts` 数组为空** 或用户的消息明显是一个新请求（提到了不同的项目、请求开始/创建某个内容等）：
→ 继续执行下面的智能路由。

## 智能路由（主要工作流程）

当用户提到正在处理某个项目时（例如：“work on my-api”、“resume frontend work”、“start auth refactor”），请**静默地**按照以下决策树进行操作——除非遇到模糊情况，否则不要询问用户：

### 第1步：检查守护进程 + 列出会话
```bash
wctl list
```
（如果守护进程未运行，告诉用户启动工作站应用程序。）

### 第2步：匹配项目

查看每个工作器的 `repo` 字段。将用户提到的项目与仓库名称进行匹配（匹配是模糊的——“frontend”可以匹配“my-frontend-app”，“api”可以匹配“backend-api-service”）。

**如果会话存在且任务上下文一致**（用户的请求与当前的 taskId/workContext相匹配）：
→ `wctl dispatch <session-id> "<用户消息>"`

**如果会话存在但任务上下文不一致**（用户想在同一个仓库中处理其他内容）：
→ 询问：“已经有一个针对 {repo} 的会话在处理 {taskId}。我是应该将这个请求发送到那个会话，还是创建一个新的会话？”

**如果该项目没有对应的会话**：
→ 转到第3步。

**如果有多个仓库匹配**（例如，“api”可能是frontend-api或backend-api）：
→ 询问用户具体是哪个仓库。

### 第3步：自动创建会话（未找到匹配的会话）

```bash
wctl discover
```

从发现的列表中找到项目路径，然后：

```bash
wctl create <repo> <path> <task-id>
```

从用户的消息中提取 `task-id`（例如，“work on auth refactor” → task-id：`auth-refactor`）。保持其简短、小写、用连字符分隔。

创建后会确认：“已为 {repo} 创建了新的会话（{task-id}）。”

如果在发现结果中找不到该项目，请询问用户仓库路径。

## 命令参考

| 命令 | 用途 |
|---|---|
| `wctl status --human` | 检查守护进程是否运行 |
| `wctl list` | 列出会话（JSON格式，用于解析） |
| `wctl list --human` | 列出会话（易于阅读的格式，供用户查看） |
| `wctl dispatch <id> "<msg>"` | 向现有会话发送消息 |
| `wctl dispatch-answers <id> <a1> <a2>...` | 发送多选题的答案。使用 `next:N` 进行多选 |
| `wctl create <repo> <path> [task]` | 创建新会话 |
| `wctl escape <id>` | 发送 Escape 键（取消提示/菜单） |
| `wctl interrupt <id>` | 发送 Ctrl+C（停止运行进程） |
| `wctl enter <id>` | 发送 Enter 键（确认/关闭） |
| `wctl screenshot <id>` | 截取会话屏幕截图（聚焦并捕获） |
| `wctl screenshot --screen` | 截取主显示屏幕的截图 |
| `wctl set-remote-mode on\|off` | 启用/禁用远程模式（用于截图时的自动聚焦） |
| `wctl discover` | 扫描项目仓库 |

## 会话控制（退出/中断）

当用户想要停止、取消或中断会话时：

| 用户输入 | 命令 |
|---|---|
| "stop session X", "cancel", "kill it", "abort" | `wctl interrupt <id>`（发送 Ctrl+C） |
| "escape", "go back", "cancel prompt", "dismiss" | `wctl escape <id>`（发送 Escape 键） |
| "press enter", "confirm", "continue", "submit" | `wctl enter <id>`（发送 Enter 键） |

**策略：** 如果不确定，先尝试使用 `escape`（安全——取消 UI 提示）。如果仍然无法解决，再使用 `interrupt`（更强制——发送 SIGINT）。

## 截图

要向用户展示会话的样子：

```bash
# 1. Capture the session
wctl screenshot <session-id>
# Returns: { "status": "ok", "imagePath": "/path/to/screenshot.png" }

# 2. Send to user using the built-in message tool
```

使用内置的 `message` 工具（非 bash）发送截图，使用 `action: "send"` 并将 `mediaUrl` 设置为捕获到的图像路径。`message` 工具与当前聊天频道和用户绑定——无需手动指定频道或目标。

如果 `message` 工具不可用，可以回退到 CLI：
```bash
openclaw message send --media <imagePath> --channel <channel> --target <target>
```
将 `<channel>` 和 `<target>` 替换为当前对话中的值（例如，`telegram` 加上用户的聊天 ID，或 `whatsapp` 加上他们的电话号码）。

对于全屏截图（例如，查看 Chrome 或其他应用程序）：`wctl screenshot --screen`

**使用场景：** 用户输入 “show me”、“screenshot”、“what does it look like”、“what's happening in session X”。

**务必** 在捕获截图后通过 `openclaw message send --media` 发送图像——`wctl` 仅将文件保存在本地。

## 重要规则

1. **始终对现有会话进行调度**。直接在终端中输入命令。切勿使用 `wctl route`（可能会重启 Claude 并中断工作）。
2. **消息中不要添加 `claude` 前缀**——直接将用户的消息传递给调度系统。
3. **向用户显示输出时添加 `--human` 参数**——否则以 JSON 格式显示（用于你自己解析）。
4. **不确定时询问用户**——如果无法将用户的消息准确匹配到某个会话/项目，请请求确认。错误的调度会干扰实际编码工作。虽然自主性很重要，但准确性更为重要。
5. **切勿猜测或凭空想象**——不要编造项目名称、会话 ID 或选项。始终检查 `wctl list` 和 `pending-prompts.json` 以获取准确信息。
6. **使用 “Chat about this” 作为备用方案**——如果无法将用户的回答映射到多选题的选项编号上，使用 `--chat-arrows 20` 选择 “Chat about this”，然后将他们的消息作为文本发送。卡住的问答模态比回退到聊天界面更糟糕。

## 响应会话提示

当第0步发现待处理的提示且用户的消息是回复时：

### 第1步：确定目标会话

待处理的提示有一个 `project` 字段。使用它来找到对应的会话：

```bash
wctl list
```

找到 `repo` 与待处理提示的 `project` 匹配的会话，并使用其 `sessionId`。

如果有多个待处理的提示，根据项目名称的提及或最新的一条来匹配用户的消息。

### 第2步：将用户的意图映射到相应的操作

**计划审批（4个选项）**：
| 用户输入 | 调度命令 |
|---|---|
| "1", "clear context", "bypass all" | `wctl dispatch <id> "1"` |
| "2", "bypass permissions", "yes bypass" | `wctl dispatch <id> "2"` |
| "3", "approve", "yes", "go ahead", "lgtm", "manually approve" | `wctl dispatch <id> "3"` |
| "reject", "no", 反馈如 "change X to Y" | **分两步操作**：`wctl dispatch <id> "4"`，等待2秒后 `wctl dispatch <id> "<他们的反馈>"` |

当用户输入类似 “yes”, “approve”, “go ahead” 的通用审批指令时，默认使用 **选项3**（“yes, manually approve edits”）。

**关于选项4（反馈/拒绝）**：这是一个两步过程。首先发送 “4” 以选择文本输入选项，等待2秒直到文本提示出现，然后再发送反馈文本。示例：
```bash
wctl dispatch abc123 "4"
sleep 2
wctl dispatch abc123 "don't modify the database schema"
```

**注意：** **始终发送选项编号，而不是文本**：

在待处理提示的 `questions` 数组中查找用户的答案，并找到对应的选项编号。例如：如果选项是 `["1. Night", "2. Day", "3. Morning"]`，而用户输入 “night”，则发送 “1”（而不是 “night”）。

| 用户输入 | 操作 |
|---|---|
| 数字（如 “1”, “2”） | 直接发送该数字 |
| 与选项标签匹配的单词（如 “night”, “dog”） | 找到对应的选项编号并发送该数字 |
| 与任何选项都不匹配的自由文本 | 发送该文本（对应 “Other” 选项） |

**单选问题**：使用常规调度：`wctl dispatch <id> "2"` |

**多选问题**：使用 `dispatch-answers`——它会依次发送每个答案，无需按下 Enter 键（Claude 会自动进行单选），然后在最后按下 Enter 键提交。将每个答案映射到其对应的选项编号，并在一条命令中发送所有答案：

```bash
wctl dispatch-answers <id> 2 1 3
```

发送顺序：`2` → 等待 → `1` → 等待 → `3` → 等待 → Enter（提交）。不需要手动控制发送顺序或等待时间——时间由系统自动处理。

**多选问题**（复选框——查看 `pending-prompts.json` 中的 `multiSelect` 字段）：输入数字可以切换选项的状态（但不会自动前进——光标会停留在第1个选项）。选择所有选项后，使用 `next:N` 下移 N 次到 “Next”/“Submit” 按钮，然后按下 Enter 键。N 等于该问题的选项数量（包括 “Other”）。

```bash
wctl dispatch-answers <id> 1 2 next:5 2
```

发送顺序：`1`（切换）→ `2`（切换）→ 下移5次到 “Next” → Enter → `2`（下一个问题，单选）→ Enter（提交所有答案）。

例如，如果有4个问题（多选/5个选项，单选/多选）：
```bash
wctl dispatch-answers <id> 1 4 next:5 2 1 1 3 next:5
```
每个 `next:N` 操作都是独立的——N 始终等于该多选问题的 `questions[i].options.length`。

**如何判断问题是否为多选**：待处理提示的 `questions` 数组中每个问题都有一个 `multiSelect` 字段。如果 `multiSelect: true`，则必须在发送答案后加上 `next:N`。如果 `multiSelect: false`（或缺失），则为单选问题，系统会自动前进——无需使用 `next`。

**如果最后一个问题是多选问题**，在发送最后一个答案时使用 `next:N`——它会点击 “Submit” 而不是 “Next”（按钮位置相同）。在所有答案都提交后，系统会自动发送最后一个 Enter 键。

**“Chat about this”** —— 在问题模态的最底部（所有选项和 Next/Submit 按钮下方），有一个 “Chat about this” 选项。方向键不会循环，因此可以安全地使用 `--chat-arrows N` 来选择它。根据 **第一个问题** 来计算 N 的值：
- 如果第一个问题是多选问题（包含 “Other” 选项）：`--chat-arrows K+1`（为 Next 按钮额外添加一个方向键）
- 如果第一个问题是单选问题（包含 “Other” 选项）：`--chat-arrows K`

```bash
# Example: first question is multi-select with 5 options → 6 arrows
wctl dispatch-answers <id> --chat-arrows 6
# Example: first question is single-select with 3 options → 3 arrows
wctl dispatch-answers <id> --chat-arrows 3
```
使用 `--chat-arrows` 时，不需要额外的答案标记——它会替换整个回答流程。

**备用规则**：如果你不确定如何将用户的答案映射到选项编号，或者用户的消息含糊不清，**始终使用 `--chat-arrows` 而不是猜测**。这样用户可以继续通过简单的文本提示进行操作，而不会因为选择错误而卡住。由于方向键不会循环，如果不确定数量，可以安全地使用 `--chat-arrows 20`——无论如何都会选择 “Chat about this”。

在选择 “Chat about this” 后，立即将用户的消息作为后续操作发送：
```bash
wctl dispatch-answers <id> --chat-arrows 20
sleep 3
wctl dispatch <id> "<user's original message>"
```

### 第3步：确认

发送命令后，告诉用户：“已向 {project} 发送了回复。”

## 错误处理

- **守护进程未运行** → 告诉用户启动工作站应用程序
- **未找到会话** → 使用 `wctl list` 显示有效的会话 ID
- **项目未在扫描范围内** → 询问用户仓库路径
- **超时** → 会话正在忙碌中，稍后重试

## 快速入门

### 安装

1. 安装 [Varie Workstation](https://github.com/varie-ai/workstation) Electron 应用程序（macOS arm64）。
2. 安装 `wctl`（将 OpenClaw 与工作站连接的 CLI）：
   ```bash
   # wctl ships with Workstation — symlink it to your PATH:
   ln -sf /path/to/varie-workstation/openclaw/wctl.js ~/.local/bin/wctl
   chmod +x ~/.local/bin/wctl
   ```
3. 将此技能复制到你的 OpenClaw 工作区：
   ```bash
   cp -r workstation ~/.openclaw/workspace/skills/workstation
   ```

### 配置

- 启动工作站应用程序并验证其是否正在运行：`wctl status`
- 启用远程模式以支持手机截图：`wctl set-remote-mode on`
- OpenClaw-Workstation 桥接器（包含在应用程序中）会将待处理的提示写入 `~/.openclaw/workspace/pending-prompts.json`——这允许从手机进行双向问题/审批操作。

### 验证

```bash
wctl status --human    # Should show "Workstation is running"
wctl list --human      # Should list active sessions (if any)
```

## 先决条件

此技能需要 **Varie Workstation** 应用程序——这是一个基于 Electron 的多会话 Claude Code 编程协调环境。该技能是移动控制层：它允许你通过 Telegram、WhatsApp 或任何 OpenClaw 频道管理工作站会话。

| 依赖项 | 功能 | 是否必需？ |
|---|---|---|
| [Varie Workstation](https://github.com/varie-ai/workstation) | 托载 Claude Code 终端的应用程序 | 是 |
| `wctl` CLI | 将 OpenClaw 命令桥接到工作站的 Unix 套接字 | 是（随工作站一起提供） |
| OpenClaw-Workstation 桥接器 | 将会话事件（问题、审批）转发到 OpenClaw 以在手机上显示通知 | 是（包含在工作站中） |

如果工作站未运行，此技能会报告 “daemon not running”。

## 安全性与限制

### 权限
- `wctl` 通过本地 Unix 套接字 `/tmp/varie-workstation.sock` 与工作站通信。没有网络调用——所有数据都在本地传输。
- 截取屏幕截图需要 macOS 的屏幕录制权限。

### 声明文件访问权限
- `~/.openclaw/workspace/pending-prompts.json`（只读）——每次调用时都会读取此文件（第0步），以检查是否有 Claude Code 会话正在等待用户输入。该文件由 OpenClaw-Workstation 桥接器生成，而非此技能。内容包括问题文本、选项标签和活动会话的标识符。文件中不包含任何凭据、秘密或用户数据。如果桥接器未创建此文件，技能会优雅地返回空响应。

### 截图
- **会话截图**（`wctl screenshot <id>`）仅捕获目标会话的特定工作站终端窗口。
- **全屏截图**（`wctl screenshot --screen`）捕获整个显示界面，可能包含无关窗口和敏感内容。此命令仅在用户明确请求全屏截图时执行（例如，“screenshot my screen”、“show me everything”）。
- 截图保存在 `~/.openclaw/media/` 目录中，保留时间为30分钟。
- 截图仅发送到用户自己的消息频道（Telegram/WhatsApp）——不会发送给第三方或外部服务。

### 在执行高风险操作前进行确认
- 在创建新会话或多个仓库匹配不明确时，此技能会请求用户确认。
- `wctl interrupt`（Ctrl+C）仅用于用户的明确请求——技能不会自动发送该命令。

### 数据处理
- `openclaw message send` 通过你配置的 OpenClaw 频道（Telegram/WhatsApp）传输媒体文件。图像会经过频道提供商的服务器，但只会发送给请求用户。

### 输入验证
- 在发送命令之前，技能会将用户的意图映射到相应的选项编号——未经验证的文本永远不会直接插入到 PTY 命令中。
- 当意图映射不确定时，会使用 “Chat about this” 作为备用方案，以防止错误的选择。

## 外部端点

| 端点 | 协议 | 发送的数据 |
|---|---|---|
| `/tmp/varie-workstation.sock` | Unix 套接字（本地） | 会话命令（列表、调度、创建、截图） |
| `~/.openclaw/workspace/pending-prompts.json` | 本地文件（只读） |
| `openclaw message send --channel --target` | OpenClaw 频道（Telegram/WhatsApp） | 截图图像（当用户请求时） |

此技能不会直接调用任何外部 API。所有网络通信都通过 OpenClaw 的频道层进行。

## 信任声明

此技能控制着在 Varie Workstation 应用程序中运行的本地 Claude Code 会话。所有通信都通过本地 Unix 套接字进行——除非你请求截图，否则数据不会离开你的设备。只有在你信任 Varie Workstation 应用程序和你的 OpenClaw 频道配置的情况下，才建议安装此技能。

## 发布者

@masqueradeljb

## 链接

- [Varie Workstation](https://github.com/varie-ai/workstation) —— 此技能所控制的应用程序
- [OpenClaw](https://docs.openclaw.ai/) —— 此技能运行的 AI 代理门户