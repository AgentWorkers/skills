---
name: context-recovery
description: 在会话压缩后，或当需要继续对话但上下文丢失时，能够自动恢复工作状态。该功能支持 Discord、Slack、Telegram、Signal 以及其他受支持的聊天平台。
homepage: https://github.com/PSPDFKit-labs/agent-skills
repository: https://github.com/PSPDFKit-labs/agent-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
      },
  }
---
# 上下文恢复

在会话被压缩后，或者当用户希望继续之前的工作但上下文丢失时，系统会自动恢复可用的工作上下文。该功能支持 Discord、Slack、Telegram、Signal 等支持的聊天平台。

**使用场景**：
- 会话开始时上下文信息被截断；
- 用户提及之前的工作内容但未提供详细信息；
- 出现会话压缩的提示信息。

---

## 安全限制

- 该功能优先使用聊天平台/会话的 API 来恢复上下文。
- 默认情况下，系统不会进行大规模的文件系统扫描或 shell 命令搜索。
- 系统不会将恢复的上下文发送到外部服务。
- 除非用户明确要求，否则系统不会将数据写入磁盘。

## 触发条件

### 自动触发
- 会话以 `<summary>` 标签开始（表明会话被压缩）；
- 用户消息中包含会话压缩的提示信息（如 “Summary unavailable”、“context limits”、“truncated”）。

### 手动触发
- 用户输入 “continue”、“did this happen?”、“where were we?”、“what was I working on?” 等；
- 用户提及 “the project”、“the PR”、“the branch”、“the issue” 等项目/拉取请求/分支/问题的名称，但未具体说明；
- 用户表示之前有工作内容，但上下文不明确；
- 用户询问 “do you remember...?” 或 “we were working on...” 等。

---

## 执行流程

### 第一步：检测当前使用的聊天平台

从运行时上下文中提取以下信息：
- `channel`：Discord、Slack、Telegram、Signal 等聊天平台的名称；
- `channelId`：具体的聊天频道/对话 ID；
- `threadId`：（针对 Slack 和 Discord 的线程对话）对话的唯一标识符。

### 第二步：获取聊天平台的历史记录（自适应深度）

**初始获取**：
```
message:read
  channel: <detected-channel>
  channelId: <detected-channel-id>
  limit: 50
```

**自适应扩展逻辑**：
1. 从返回的消息中解析时间戳；
2. 计算时间跨度：`newest_timestamp - oldest_timestamp`；
3. 如果时间跨度小于 2 小时且消息数量小于或等于预设限制（`limit`），则：
   - 再获取 50 条消息（如果平台支持 `before` 参数，则使用该参数）；
   - 重复此过程，直到时间跨度大于或等于 2 小时或总消息数量大于或等于 100 条；
4. 最大获取消息数量为 100 条（受 token 预算限制）。

**针对线程的上下文恢复（Slack/Discord）**：
```
# If threadId is present, fetch thread messages first
message:read
  channel: <detected-channel>
  threadId: <thread-id>
  limit: 50

# Then fetch parent channel for broader context
message:read
  channel: <detected-channel>
  channelId: <parent-channel-id>
  limit: 30
```

**解析内容**：
- 用户最近提出的请求；
- 辅助系统最近的回复内容；
- URL、文件路径、分支名称、拉取请求（PR）编号；
- 未完成的操作（用户提出但未执行的操作）；
- 项目标识符和工作目录。

### 第三步：获取会话上下文（安全模式）

仅使用聊天平台的 API，避免进行文件系统扫描：
```yaml
# List recent sessions (if tool exists)
sessions_list:
  limit: 5

# Pull last messages from likely matching session
sessions_history:
  sessionKey: <candidate-session-key>
  limit: 80
  includeTools: true
```

如果会话相关的 API 不可用，则跳过此步骤，仅依赖聊天平台的记录。

### 第四步：可选的内存检查（需用户明确授权）

仅当代理的运行时环境提供了内存访问工具或路径时，才进行内存检查。
**严禁** 在用户的个人目录中进行全局文件系统扫描。

### 第五步：合成上下文

生成结构化的上下文摘要：
```markdown
## Recovered Context

**Channel:** #<channel-name> (<platform>)
**Time Range:** <oldest-message> to <newest-message>
**Messages Analyzed:** <count>

### Active Project/Task
- **Repository:** <repo-name>
- **Branch:** <branch-name>
- **PR:** #<number> — <title>

### Recent Work Timeline
1. [<timestamp>] <action/request>
2. [<timestamp>] <action/request>
3. [<timestamp>] <action/request>

### Pending/Incomplete Actions
- ⏳ "<quoted incomplete action>"
- ⏳ "<another incomplete item>"

### Last User Request
> "<quoted request that may not have been completed>"
```

### 第六步：可选的持久化处理（需用户同意）

默认情况下，系统不会将恢复的上下文写入磁盘。如果用户同意持久化处理，系统会先询问用户：
> “我可以将这些恢复的上下文缓存到内存中，以便后续继续使用吗？”

### 第七步：展示恢复的上下文

向用户展示恢复的上下文，并询问：
> “上下文已恢复。您上次的请求是 [X]。该操作 [已完成/未完成]。您希望 [继续/重试/澄清] 吗？”

---

## 各平台特定说明

### Discord
- 使用来自消息元数据的 `channelId`；
- 公会频道可以访问全部历史记录；
- 对于线程对话，需要检查消息元数据中的 `threadId`；
- 私人消息（DM）的历史记录可能有限。

### Slack
- 使用包含 Slack 频道 ID 的 `channel` 参数；
- 恢复线程上下文时需要 `threadId`，请务必先检查；
- 获取父频道的内容可以提供完整的对话上下文；
- 可能需要工作区级别的权限才能访问全部历史记录。

### Telegram / Signal 等平台
- 使用相同的 `message:read` 接口；
- 不同平台的历史记录深度可能有所不同；
- 群组对话与私人消息的上下文可能有所不同。

---

## 限制条件

- 当上下文缺失时，优先使用本协议进行恢复，而不是直接声明 “数据不足”；
- 自适应扩展深度：初始获取 50 条消息，最多扩展到 100 条；
- 努力捕获至少 2 小时的上下文信息；
- 如果恢复失败，需说明尝试了哪些操作以及哪些数据源无法获取；
- 未经用户明确同意，系统避免进行大规模的文件系统扫描或数据写入。

---

## 自动触发机制

在会话开始时，系统会检测会话是否被压缩：
```python
# Pseudocode for trigger detection
if message contains "<summary>":
    trigger_context_recovery()
elif message contains any of ["Summary unavailable", "context limits", "truncated", "compacted"]:
    trigger_context_recovery()
elif message matches continuation_patterns:
    # "continue", "where were we", "did this happen", etc.
    trigger_context_recovery()
```

**无需等待用户询问**——如果检测到会话被压缩，系统会主动恢复上下文并展示给用户。

---

## 示例

**场景**：会话开始时显示压缩提示

```
User message: "<summary>Summary unavailable due to context limits...</summary>"
User message: "did this happen?"
```

**代理执行流程**：
1. 通过 `<summary>` 标签检测到会话被压缩；
2. 调用 `message:read channel=discord channelId=1460342116516364533 limit=50`；
3. 计算时间跨度为 2.5 小时（足够的时间范围，无需进一步扩展）；
4. 解析消息，找到用户的最后一次请求；
5. 使用会话 API 获取用户的请求内容；
6. 向用户展示恢复的上下文，并询问是否继续操作：

> “上下文已恢复。您上次的请求是从 Nexus 存档会话中提取 PR #137（Skills & Agents System）的相关信息。该操作在上下文被截断前未能完成。
>
> **恢复的上下文内容**：
> - PR #137：包含 15,053 个新增内容，91 个文件，存在合并冲突；
> - 相关文件路径：`content/spec-skills-agents-system.md`（共 2,067 行）；
>
> “您是否希望继续提取这些信息？”