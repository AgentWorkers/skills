---
name: feishu-messaging
description: >
  Feishu（Lark）消息配置与格式化的最佳实践。适用场景包括：  
  (1) 配置 Feishu 的频道设置；  
  (2) 遇到消息格式化问题（如原始文本与卡片式显示之间的差异）；  
  (3) 设置 `renderMode` 以确保消息的稳定显示；  
  (4) 理解自动回复与主动发送消息的区别。  
  这些最佳实践对于确保 Feishu 聊天中消息格式的一致性至关重要。
---
# Feishu 消息配置

## 快速入门

为了在 Feishu 中实现稳定、一致的消息格式，请进行以下配置：

```yaml
channels:
  feishu:
    renderMode: "card"  # Recommended for most use cases
```

这样可以确保所有的自动回复都使用带有正确 Markdown 渲染效果的交互式卡片。

## 消息格式的稳定性

### 问题：原始文本与卡片格式的混合

如果没有正确的配置，Feishu 消息可能会以以下不一致的方式显示：
- **原始文本**：纯 Markdown 源代码，没有格式化
- **卡片格式**：带有语法高亮、表格和链接的渲染后的 Markdown

这会导致用户体验不佳，因为消息的显示效果不可预测。

### 解决方案：明确设置 `renderMode`

请明确设置 `renderMode`，而不是依赖自动检测：

| 模式 | 行为 | 使用场景 |
|------|----------|----------|
| `auto` | 根据内容自动选择格式 | 默认模式，但可能不一致 |
| `raw` | 始终显示为纯文本 | 仅包含简单文本的回复 |
| `card` | 始终显示为交互式卡片 | **推荐** – 格式一致 |

**推荐配置：**

```yaml
channels:
  feishu:
    renderMode: "card"
```

这样可以保证：
- ✅ 消息显示效果一致
- ✅ 正确的 Markdown 渲染（语法高亮、表格、链接）
- ✅ 避免意外的格式切换
- ✅ 专业的、美观的显示效果

## 自动回复与主动消息

### 自动回复（机器人对用户消息的回复）

`renderMode` 的设置会影响自动回复的格式：
- `renderMode: "card"` → 所有自动回复都使用卡片格式
- `renderMode: "raw"` → 所有自动回复都使用纯文本

**示例流程：**
1. 用户：**“展示代码给我”**
2. 机器人自动回复时使用卡片格式（如果 `renderMode: "card"`）

### 主动消息（机器人通过 `message` 工具发送的消息）

主动发送的消息始终使用纯文本格式，通过 `outbound.sendText` 方法实现。

**要主动发送卡片格式的消息：**
1. 首先让用户发送一条消息
2. 机器人再回复该消息（此时使用 `renderMode`）

**示例：**
```
User: "Remind me about the meeting"
Bot (proactive): "OK, reminder set"  # Plain text via message tool

vs

User: "Set up a reminder"
Bot (auto-reply): "OK, reminder set"  # Card format if renderMode: "card"
```

## 配置检查清单

### 基本设置

```yaml
channels:
  feishu:
    enabled: true
    appId: "cli_xxxxx"
    appSecret: "secret"
    renderMode: "card"  # 🔑 Key setting for stable formatting
```

### 高级选项

```yaml
channels:
  feishu:
    # Connection
    connectionMode: "websocket"  # Recommended
    domain: "feishu"  # or "lark" for international

    # Message behavior
    requireMention: true  # Groups: bot only responds when @mentioned
    mediaMaxMb: 30

    # Access control
    dmPolicy: "pairing"  # DM requires approval
    groupPolicy: "allowlist"  # Only allowed groups
```

## 故障排除

### 消息显示为原始 Markdown

**问题：** 用户看到未格式化的 Markdown 源代码

**解决方案：**
1. 检查 `renderMode` 设置：`openclaw config get channels.feishu.renderMode`
2. 将其设置为 "card"：`openclaw config set channels.feishu.renderMode "card"`
3. 重启 OpenClaw：`openclaw gateway restart`

### 格式在原始文本和卡片格式之间切换

**问题：** 有些消息被格式化，有些则没有

**解决方案：**
- 将 `renderMode` 从 "auto" 更改为 "card"
- "auto" 模式会根据内容自动选择格式，从而导致不一致

### 主动消息未使用卡片格式

**预期行为：** 通过 `message` 工具发送的主动消息始终使用纯文本

**解决方法：**
1. 用户先发送一条消息
2. 机器人的自动回复将使用卡片格式

## 最佳实践

### 1. 明确使用 `renderMode`

在生产环境中避免使用 "auto" 模式。请明确选择 "card" 或 "raw"。

```yaml
# ✅ Good - explicit, predictable
renderMode: "card"

# ⚠️ Risky - can be inconsistent
renderMode: "auto"
```

### 2. 在 `USER.md` 中记录配置信息

将用户偏好设置添加到工作区的 `USER.md` 文件中：

```markdown
## Preferences

- **Feishu Message Format:** Configured with `renderMode: "card"`, auto-replies use card format
- **Note:** Proactive messages via `message` tool are still plain text
```

### 3. 测试配置

更改设置后：
1. 重启 OpenClaw：`openclaw gateway restart`
2. 向机器人发送测试消息
3. 确认格式是否一致

### 4. 组群聊天注意事项

在群组中，机器人仅会在被提及时才回复（如果 `requireMention: true` 为真）：

```
User: @bot help me check the data
Bot: [Card format reply with data]

User: Nice weather today
Bot: [No response - not mentioned]
```

## 相关技能

- **feishu-doc**：文档的读写操作
- **feishu-drive**：云存储文件管理
- **feishu-wiki**：知识库导航
- **feishu-perm**：权限管理

## 参考资料

有关详细配置和 API 文档，请参阅：
- [configuration.md](references/configuration.md)：完整的配置选项
- [render-modes.md](references/render-modes.md)：深入了解渲染模式