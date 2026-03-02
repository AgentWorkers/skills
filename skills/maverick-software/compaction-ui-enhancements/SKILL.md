---
name: compaction-ui
version: 2.1.0
description: "OpenClaw 控制界面的功能包括：  
- **后台内存压缩**：支持自动触发内存压缩机制；  
- **聊天记录摘要**：能够生成聊天记录的简要摘要；  
- **可配置阈值**：用户可以设置内存压缩的触发条件；  
- **模型选择器**：提供多种模型供用户选择；  
- **设置选项卡**：允许用户自定义相关设置；  
- **结果存储**：压缩后的数据会保存到指定的存储位置。"
---
# Compaction UI v2.1.0

这是一个用于 OpenClaw 控制界面的内存压缩系统，支持后台执行，并提供toast通知。系统会在配置的令牌阈值达到时自动触发压缩操作；压缩后的输出中会包含对话摘要段落；此外，还提供了一个专门的设置页面，用于选择压缩模型并查看压缩结果历史记录。

## 状态：✅ 已启用

| 组件 | 状态 |
|-----------|--------|
| 上下文指示器按钮 | ✅ 可用 |
| 后台压缩（toast通知） | ✅ 可用 |
| 自动压缩触发 | ✅ 可用 |
| 对话摘要段落 | ✅ 可用 |
| 设置页面（插件注册） | ✅ 可用 |
| 模型选择器 | ✅ 可用 |
| 最后压缩结果存储与查看器 | ✅ 可用 |
| 设置持久化与重新加载 | ✅ 可用 |
| 认证层级（OAuth → API → 备用） | ✅ 可用 |
| 聊天历史过滤 | ✅ 可用 |
| 压缩分隔线 | ✅ 可用 |

## 特性

### 1. 上下文指示器按钮 (`app-renderhelpers.ts`)

这是一个圆形的 SVG 进度条，位于聊天工具栏中，也可用于手动触发压缩操作。

- **位置：** 在 `renderChatControls()` 方法中，位于会话选择器下拉框之后
- **数据来源：** 来自会话行的 `sessionsResult.sessions[].totalTokens` 和 `contextTokens`
- **颜色：** 绿色（<60%），黄色（60-85%），红色（≥85%）
- **禁用情况：** 当使用率低于 20% 或在压缩操作进行中时
- **工具提示：** 显示“上下文：XK / YK 令牌（Z%）”

### 2. 后台压缩（Toast通知）

点击该按钮或达到配置的阈值时，系统会通过底部右侧的 toast 通知系统在后台执行压缩操作，不会阻塞用户界面。

- **执行中时的 toast：** 显示“内存压缩中”并带有旋转图标
- **压缩完成时的 toast：** 显示“已压缩：XK → YK”并带有勾选标记（5 秒后自动消失）
- **错误时的 toast：** 显示错误信息（5 秒后自动消失）
- 该功能与其他后台进程（如定时任务、知识提取等）使用相同的 `backgroundJobToasts` 系统

### 3. 自动压缩

每次发送聊天回复后，系统会检查令牌使用情况是否超过配置的阈值。如果超过阈值，系统会自动触发压缩操作：

- 显示“正在自动压缩（X%）”的 toast 通知，并显示当前的令牌使用率
- 5 秒的延迟机制防止重复触发压缩操作
- 压缩成功后，聊天界面会自动刷新
- 如果没有进行压缩操作，toast 通知会自动消失

### 4. 对话摘要段落

现在，每次压缩后的输出都会以 `## 对话摘要` 段落开头，该段落会：

- 描述对话的主题
- 解释讨论的流程和关键转折点
- 总结对话的进展
- 采用过去时态进行叙述性总结

**实现方式：** 通过 `compact.ts` 将自定义指令注入到压缩过程中的 LLM 调用中。这些自定义指令会添加在用户提供的任何自定义指令之前。

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

#### 自动压缩卡片
- **切换开关：** 启用/禁用自动压缩功能
- **阈值滑块：** 10% 至 95%（默认值：60%）
- **颜色编码：** 绿色（<60%），黄色（60-85%），红色（≥85%）

#### 模型卡片
- **下拉菜单：** 选择特定的压缩模型或使用会话默认模型
- 按提供者进行分组，并显示对应的上下文窗口大小
- 选择自定义模型时会有警告提示（提醒需要 API 密钥）
- **备用方案：** 如果自定义模型失败，系统会自动切换回会话默认模型

#### 结果存储卡片
- **切换开关：** 是否保存压缩后的摘要文本以供查看

#### 最后压缩卡片
- **压缩前后对比：** 以两列网格的形式显示令牌数量
- **统计信息：** 保存的令牌数量、减少的百分比、触发类型、时间戳、会话键
- **查看结果：** 可展开的摘要查看器（启用存储功能时可用）
- **清除：** 重置存储的结果
- **提示：** 当关闭存储功能时显示“启用结果保存”提示

**状态管理：**
- 模块级别的状态会在会话重新加载时保持不变
- 每次访问设置页面时，系统会从后端重新加载设置（设置过期时间为 2 秒）
- 提供 `resetCompactionSettingsState()` 函数用于测试和切换页面时使用

### 6. 认证层级

压缩操作使用 `resolveApiKeyForProvider` 和 `getApiKeyForModel` 进行认证，与聊天功能使用相同的认证流程：

**OAuth → API 密钥 → 备用**

无需单独配置。如果配置了 OAuth（Claude Max）作为主要认证方式，压缩操作会自动使用该认证方式。选择自定义模型时也会使用相同的认证流程。

### 7. 结果存储

当启用存储功能时，最新的压缩结果会被保存到 `{agentDir}/compaction-config.json` 文件中：
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

当关闭存储功能时，虽然会保存元数据（时间戳、令牌数量），但不会保存摘要文本。

### 8. 聊天历史过滤

- **排除特定消息：** 系统会忽略包含 “NO_REPLY” 或 “HEARTBEAT_OK” 的辅助消息
- **压缩分隔线：** 为类型为 `__openclaw.kind === "compaction"` 的消息显示分隔线

## 架构

### 后端 RPC 方法

| 方法 | 描述 |
|--------|-------------|
| `sessions.compact` | 执行压缩操作（完成后记录结果） |
| `compaction.getSettings` | 从配置文件中读取设置 |
| `compaction.saveSettings` | 更新设置（阈值范围为 10% 至 95%） |
| `compaction.getLastResult` | 获取最后一次压缩的结果 |
| `compaction.clearLastResult` | 清除存储的结果 |

### 修改的文件

| 文件 | 修改内容 |
|------|---------|
| `src/gateway/server-methods/compaction.ts` | 处理设置相关的 RPC 请求和响应 |
| `src/gateway/server-methods/sessions.ts` | 调用 `sessions.compact` 方法记录压缩结果 |
| `src/gateway/server-methods/plugins-ui.ts` | 注册压缩相关的插件视图 |
| `src/gateway/server-methods.ts` | 处理相关的方法调用 |
| `src/gateway/server-methods-list.ts` | 注册相关的方法 |
| `src/gateway/method-scopes.ts` | 注册相关的方法范围 |
| `src/agents/pi-embedded-runner/compact.ts` | 向压缩过程注入聊天摘要指令 |
| `ui/src/ui/app-renderhelpers.ts` | 实现上下文指示器和后台压缩触发功能 |
| `ui/src/ui/app-gateway.ts` | 在聊天回复后检查是否需要自动压缩 |
| `ui/src/ui/views/compaction-settings.ts` | 显示设置页面 |
| `ui/src/ui/app-render.ts` | 组织页面结构 |
| `ui/src/ui/views/chat.ts` | 实现聊天历史过滤功能 |

### 配置文件

`{agentDir}/compaction-config.json` — 每个代理都会生成一个这样的配置文件，首次保存设置时创建。

### 插件注册

压缩功能作为内置插件在 `plugins-ui.ts` 中进行注册：
```typescript
{
  id: "compaction",
  label: "Compaction",
  subtitle: "Memory Management",
  icon: "archive",
  group: "agent",
  position: 7,
  pluginId: "compaction-ui",
}
```

## 已知的常见问题

- **设置信息在页面切换后不持久化：** 在 v2.1.0 中已修复。之前模块级别的 `_state.loaded` 标志会导致设置信息无法在页面切换后保留。现在每次重新访问设置页面时，系统都会在 2 秒后重新加载设置。
- **模型选择器需要 API 密钥：** 如果选择了自定义模型，请确保已配置提供者的 API 密钥。系统会显示相应的警告提示。
- **压缩模型格式：** 必须使用 “provider/model” 的格式（例如 “anthropic/claude-sonnet-4-6”）。无效的格式会被忽略，并自动切换回会话默认模型。

## 更新日志

### v2.1.0
- **对话摘要段落：** 压缩后的输出现在以 `## 对话摘要` 段落开头
- **模型选择器：** 可以选择特定的压缩模型或使用会话默认模型
- **设置重新加载：** 设置页面现在每 2 秒会从后端重新加载设置，而不是永久缓存
- **参考文件更新：** `references/` 文件已与当前代码同步

### v2.0.0
- **后台压缩：** 用 toast 通知替代了阻塞整个界面的全屏弹窗
- **自动压缩：** 在发送聊天回复后，如果令牌使用量超过配置的阈值，系统会自动触发压缩操作（可配置，默认值为 60%，带有 5 秒的延迟机制）
- **设置页面：** 压缩功能作为插件注册在 **Agent** 导航组下
- **结果记录：** `sessions.compact` 方法会记录压缩前后的令牌数量和可选的摘要信息
- **认证层级：** 与聊天功能相同的认证流程（OAuth → API → 备用）
- **设置相关的 RPC 方法：** `compaction.getSettings`、`compaction.saveSettings`、`compaction.getLastResult`、`compaction.clearLastResult`

### v1.0.0
- 首次发布：添加了上下文指示器按钮和带有动画效果的阻塞弹窗；`sessions.compact` 方法用于记录压缩结果；实现了聊天历史的过滤功能；添加了压缩分隔线