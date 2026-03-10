---
name: compaction-ui
version: 2.3.0
description: "OpenClaw控制界面的背景内存压缩功能支持自动触发、聊天记录摘要显示、可配置的压缩阈值、模型选择器、设置选项卡以及结果存储功能。"
---
# Compaction UI v2.1.0

这是一个用于 OpenClaw 控制界面的内存压缩系统，支持后台执行，并通过通知栏（toast）进行提示。系统会在配置的令牌（token）阈值达到时自动触发压缩操作；压缩后的输出中会包含对话摘要段落；此外，还提供了一个专门的设置页面，用户可以在该页面选择压缩模型并查看压缩结果的历史记录。

## 状态：✅ 已激活

| 组件 | 状态 |
|-----------|--------|
| 上下文指示器按钮 | ✅ 可用 |
| 后台压缩（通知栏） | ✅ 可用 |
| 自动压缩触发 | ✅ 可用 |
| 对话摘要段落 | ✅ 可用 |
| 设置页面（插件注册） | ✅ 可用 |
| 模型选择器 | ✅ 可用 |
| 最后压缩结果存储与查看 | ✅ 可用 |
| 身份验证层级（OAuth → API → 备用） | ✅ 可用 |
| 聊天历史过滤 | ✅ 可用 |
| 完全后台隔离（无聊天干扰） | ✅ 可用 |

## 主要功能

### 1. 上下文指示器按钮 (`app-renderhelpers.ts`)

这是一个圆形的 SVG 进度条，位于聊天工具栏中，同时也可以用于手动触发压缩操作。

- **位置：** 在 `renderChatControls()` 方法中，位于会话选择器下拉框之后。
- **数据来源：** 来自会话行的 `sessionsResult.sessions[].totalTokens` 和 `contextTokens`。
- **颜色表示：** 绿色（<60%），黄色（60-85%），红色（≥85%）。
- **禁用情况：** 当系统利用率低于 20% 或在压缩操作进行中时。
- **工具提示：** 显示“当前上下文中的令牌数量（Z%）”。

### 2. 后台压缩（通知栏）

点击该按钮或系统达到配置的阈值时，压缩操作会在后台启动，并通过底部右侧的通知栏进行提示（不会阻塞用户界面）。用户界面始终保持交互状态。

- **运行中提示：** 显示“内存压缩中”并伴有旋转图标。
- **压缩完成提示：** 显示“压缩完成：XK → YK”，并带有勾选标记（5 秒后自动消失）。
- **错误提示：** 显示错误信息（5 秒后自动消失）。
- 该功能使用与所有其他后台进程（如定时任务、知识提取等）相同的 `backgroundJobToasts` 系统。

### 3. 自动压缩

每次发送聊天回复后，系统会检查令牌使用情况是否超过配置的阈值。如果超过阈值，系统会自动触发压缩操作：

- 通知栏会显示“正在自动压缩（X%）”以及当前的利用率。
- 系统会设置 5 秒的延迟机制，以防止频繁触发压缩操作。
- 压缩成功后，聊天界面会自动刷新。
- 如果没有进行压缩操作，通知栏会自动消失。

### 4. 对话摘要段落

现在，每次压缩操作后的输出都会在结构化的 `## Goal` 部分之前添加一个 `## Conversation Summary` 段落。该段落由 3-6 句自然语言组成，用于：

- 描述对话的整体主题。
- 解释讨论的流程和关键转折点。
- 总结对话的进展。

**实现方式：** 通过 `compact.ts` 将自定义指令注入到压缩操作的 LLM 调用中。这些指令会添加到用户提供的任何自定义指令之前（格式为 `/compact [instructions]`），从而确保两者可以同时生效。

**示例输出：**
```
## Conversation Summary
The conversation began with the user requesting improvements to the compaction
system, specifically moving from a blocking modal to background toasts. Discussion
then shifted to adding a settings tab with auto-compaction controls. After
implementing and testing those features, the user noticed settings weren't
persisting across tab navigations, which led to a fix for the module-level
state cache. Finally, the user requested adding a narrative summary paragraph
to the compaction output for better context.

## Goal
...
```

### 5. 设置页面（插件注册）

这是一个位于 **Agent** 导航组下的专门设置页面，通过插件 UI 架构进行注册。

**注册方式：** 在 `plugins-ui.ts` 文件中，使用以下配置进行注册：
```json
{
  "id": "compaction",
  "group": "agent",
  "position": 7,
  "icon": "archive"
}
```

**页面内容：**

- **自动压缩卡片**：
  - 允许/禁用自动压缩功能。
  - 提供一个滑块，用于设置压缩阈值（10% 到 95%，默认值为 60%）。
  - 通过颜色（绿色、黄色、红色）显示当前的利用率。

- **模型卡片**：
  - 允许用户选择特定的压缩模型，或使用会话默认模型。
  - 模型按提供者进行分组，并显示对应的上下文窗口大小。
  - 如果选择了自定义模型，系统会显示警告提示。
  - 如果自定义模型使用失败，系统会自动回退到会话默认模型。

- **结果存储卡片**：
  - 允许用户选择是否保存压缩后的摘要文本以供查看。

- **最后压缩卡片**：
  - 以两列网格的形式显示压缩前后的令牌数量。
  - 显示保存的令牌数量、减少的百分比、压缩类型、时间戳和会话键。
  - 提供可展开的摘要查看功能（如果启用了结果存储）。
  - 提供“启用结果存储”按钮（当结果存储功能关闭时显示）。

**状态管理：**
- 模块级别的状态会在会话重新加载时保持不变。
- 每次访问设置页面时，系统会从后端重新加载设置（延迟时间为 2 秒）。
- 提供 `resetCompactionSettingsState()` 函数，用于测试和切换页面时使用。

### 6. 身份验证层级

压缩操作使用 `resolveApiKeyForProvider` 和 `getApiKeyForModel` 进行身份验证，与聊天功能使用相同的身份验证流程：

**OAuth → API Key → 备用**

无需单独配置。如果配置了 OAuth（Claude Max）作为主要身份验证方式，压缩操作会自动使用该方式。选择自定义模型时，也会使用相同的身份验证流程。

### 7. 结果存储

当启用结果存储功能时，最新的压缩结果会保存到 `{agentDir}/compaction-config.json` 文件中：
```json
{
  "settings": {
    "autoEnabled": true,
    "autoThresholdPercent": 60,
    "storeLastResult": true,
    "compactionModel": "anthropic/claude-sonnet-4-6"
  },
  "lastResult": {
    "timestamp": 1709283600000,
    "trigger": "manual",
    "tokensBefore": 50614,
    "tokensAfter": 4766,
    "tokensSaved": 45848,
    "percentReduction": 91,
    "sessionKey": "agent:main:main",
    "summary": "## Conversation Summary\nThe conversation focused on...\n\n## Goal\n..."
  }
}
```

当禁用结果存储功能时，虽然元数据（时间戳、令牌数量）仍会被保存，但摘要文本会被忽略。

### 8. 聊天历史过滤

- **忽略特定类型的消息：** 系统会跳过包含特定文本的助手消息。
- **压缩分隔线：** 对于类型为 `__openclaw.kind === "compaction"` 的消息，系统会显示一个分隔线。

## 架构

### 后端 RPC 方法

| 方法 | 描述 |
|--------|-------------|
| `sessions.compact` | 执行压缩操作，并在完成后记录结果。|
| `compaction.getSettings` | 从配置文件中读取设置。|
| `compaction.saveSettings` | 更新设置（阈值范围为 10% 到 95%）。|
| `compaction.getLastResult` | 获取最后一次压缩的结果。|
| `compaction.clearLastResult` | 清除保存的结果。|

### 修改的文件

| 文件 | 修改内容 |
|------|---------|
| `src/gateway/server-methods/compaction.ts` | 修改了与设置相关的 RPC 方法和配置文件读写逻辑。|
| `src/gateway/server-methods/sessions.ts` | 修改了 `sessions.compact` 方法，用于记录压缩后的结果。|
| `src/gateway/server-methods/plugs-ui.ts` | 注册了压缩相关的插件视图。|
| `src/gateway/server-methods.ts` | 修改了相关处理逻辑。|
| `src/gateway/server-methods-list.ts` | 修改了方法注册逻辑。|
| `src/gateway/method-scopes.ts` | 修改了方法的作用域注册逻辑。|
| `src/agents/pi-embedded-runner/compact.ts` | 修改了聊天摘要相关的指令注入逻辑。|
| `ui/src/ui/app-renderhelpers.ts` | 修改了上下文指示器和后台压缩触发逻辑。|
| `ui/src/ui/app-gateway.ts` | 修改了在聊天回复后检查自动压缩功能的逻辑。|
| `ui/src/ui/views/compaction-settings.ts` | 修改了设置页面的显示逻辑。|
| `ui/src/ui/app-render.ts` | 修改了页面的显示逻辑。|
| `ui/src/ui/views/chat.ts` | 修改了聊天历史的过滤逻辑。|

### 配置文件

`{agentDir}/compaction-config.json`：该文件按代理（agent）进行创建，在首次保存设置时生成。

### 已知的常见问题及解决方法

- **设置内容在页面重新加载后丢失**：已在 v2.1.0 中修复。问题是由于模块级别的 `_state.loaded` 标志导致的。现在，每次重新访问设置页面时，系统都会重新加载设置。
- **模型选择器需要 API 密钥**：如果选择了自定义模型，请确保已配置提供者的 API 密钥。系统会显示相应的警告提示。
- **压缩模型的格式要求**：压缩模型必须遵循 “provider/model” 的格式（例如 “anthropic/claude-sonnet-4-6”）。无效的格式会被忽略，并自动回退到会话默认模型。
- **过滤逻辑的限制**：在从 `readSessionMessages` 方法中过滤消息时，只有包含 `message` 字段的记录才会被过滤。对于非消息类型的记录（例如类型为 “custom” 的记录），系统会忽略它们。修复方法：仅检查 `parsed?.message` 字段是否在过滤集合中，并仅将它们的 ID 添加到过滤集合中。
- **禁止阻塞用户界面**：`app-renderhelpers.ts` 中的指示器按钮绝对不能显示全屏覆盖层。压缩操作是后台进行的，所有状态信息都通过底部右侧的通知栏显示。请确保删除所有基于 `compactState(phase` 条件的覆盖层设置。按钮在运行时可能会显示旋转图标，但不得阻塞用户界面。

## 更新日志

### v2.1.0
- **对话摘要段落**：压缩后的输出现在会在结构化部分之前添加一个 `## Conversation Summary` 段落。
- **模型选择器**：允许用户选择特定的压缩模型或使用会话默认模型。
- **设置页面的刷新逻辑**：现在设置页面会每 2 秒从后端重新加载设置，而不是永久缓存。
- **参考文件更新**：`references/` 文件已与当前源代码同步。

### v2.0.0
- **后台压缩**：将阻塞用户界面的全屏模态窗口替换为后台通知栏。
- **自动压缩**：在聊天回复后，如果令牌使用量超过配置的阈值，系统会自动触发压缩操作（可配置，默认阈值为 60%，延迟时间为 5 秒）。
- **设置页面**：压缩功能被注册为插件视图，位于 **Agent** 导航组下。
- **结果记录**：`sessions.compact` 方法现在会记录压缩前后的令牌数量和可选的摘要信息。
- **身份验证层级**：压缩操作使用与聊天功能相同的身份验证流程（OAuth → API → 备用）。
- **RPC 方法更新**：添加了 `compaction.getSettings`、`compaction.saveSettings`、`compaction.getLastResult` 和 `compaction.clearLastResult` 方法。

### v1.0.0
- 首次发布版本：添加了上下文指示器按钮、带有动画效果的阻塞模态窗口、`sessions.compact` 方法用于与 LLM 交互以生成摘要、聊天历史记录的过滤逻辑，以及压缩操作的分隔线。