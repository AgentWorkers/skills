---
name: feishu-chat
description: Feishu (Lark) group chat messaging guide for OpenClaw. Includes Raw/Card message modes, @ mention formatting, and group member management. Use when sending messages in Feishu groups, mentioning users/bots, or formatting messages with Markdown. Trigger words: feishu, lark, chat, mention, at, markdown, group.
---

# Feishu群组聊天指南

## 快速入门：配置renderMode

**⚠️ 重要提示：** 为确保消息格式的稳定性，请明确设置`renderMode`。

```yaml
# Recommended configuration
channels:
  feishu:
    renderMode: "card"  # Always use card format
```

**为什么？** 默认的“auto”模式会导致格式切换不可预测（原始文本或卡片格式），从而影响用户体验。

**配置方法：**
```bash
openclaw config set channels.feishu.renderMode "card"
openclaw gateway restart
```

**验证方法：**
```bash
openclaw config get channels.feishu.renderMode
```

---

## 先决条件

1. **处于Feishu群组中** - 确保OpenClaw已连接到Feishu。
2. **配置renderMode** - 设置为“card”以保持格式的一致性。
3. **了解成员ID**：
   - 人类用户：`open_id`（格式为`ou_xxx`）
   - 机器人：`App ID`（格式为`cli_xxx`）

---

## 0. 消息格式的稳定性

### 问题：原始文本与卡片格式的混合

如果没有正确配置`renderMode`，消息可能会以以下方式显示：
- **原始文本**：纯Markdown格式，没有格式化。
- **卡片格式**：带有语法高亮、表格和链接的渲染后的Markdown。

### 解决方案：明确指定`renderMode`

| 模式 | 行为 | 使用场景 |
|------|----------|----------|
| `auto` | 根据内容自动选择格式 | 应避免使用，因为格式不可预测 |
| `raw` | 始终显示为纯文本 | 适用于简单的纯文本回复 |
| `card` | 始终显示为交互式卡片 | 推荐使用 |

**建议：** 在所有生产环境中将`renderMode`设置为“card”。

---

## 1. 发送消息

### ⚠️ 重要提示：** 只使用一种方法**

**请不要对同一条消息同时使用直接回复（direct reply）和消息工具（message tool）！** 这会导致发送两条消息。

请选择其中一种方式：
- 纯文本 → 仅使用消息工具
- Markdown → 仅使用直接回复

---

### 两种发送方法

| 方法 | 工具 | 显示格式 | 使用场景 |
|--------|------|-------------|----------|
| **消息工具** | `message` | 原始文本（纯文本） | 适用于发送纯文本或@提及其他成员的消息 |
| **直接回复** | 会话中的直接回复 | 卡片格式（包含Markdown） | 适用于发送包含Markdown格式的消息 |

### 原始文本模式

**使用场景：** 发送纯文本消息或@提及其他成员。

**发送方法：**
```javascript
message({
  action: "send",
  channel: "feishu",
  target: "oc_xxx",
  message: "Plain text content"
})
```

**@提及的格式：**
```javascript
message({
  action: "send",
  channel: "feishu",
  target: "oc_xxx",
  message: "<at user_id=\"ou_xxx\">nickname</at> Hello!"
})
```

**原始文本模式的限制：**
- **不可渲染Markdown格式（如粗体、斜体、代码块）**
- **不可渲染表格和链接**
- **@提及功能正常使用**

### 卡片模式（Markdown）

**使用场景：** 发送包含代码块、表格和格式化文本的消息。

**发送方法：** 在会话中直接回复，并使用Markdown格式。

**触发卡片模式的条件：** 包含以下任意一项：
- 代码块
``` ```
- Tables `| table |`
- Bold `**bold**`
- Italic `*italic*`
- Strikethrough `~~text~~`
- Links `[link](url)`
- Headings `# heading`
- Lists `- item` or `1. item`

**@ Mention format**:
```
<at id=ou_xxx></at> 这是一条卡片格式的消息，@提到了用户xx
```

**Markdown内容** 可以正确渲染：
```

**Supported in Card Mode**:

| Style | Syntax | Status |
|-------|--------|--------|
| Bold | `**bold**` | ✅ Supported |
| Italic | `*italic*` | ✅ Supported |
| Strikethrough | `~~text~~` | ✅ Supported |
| Color | `<font color='red'>text</font>` | ✅ Supported |
| Links | `[link](https://xxx)` | ✅ Supported |
| Headings | `# heading` | ✅ Supported |
| Lists | `- item` or `1. item` | ✅ Supported |
| Code blocks | ``` code ``` | 可以正确渲染 |

**卡片模式不支持的格式：**

| 格式 | 语法 | 备注 |
|-------|--------|--------|
| 引用 | `> quote` | 不支持 |
| 内联代码 | ``` `code` `` | 不稳定 |
| 水平线 | `---` | 不支持 |
| 复杂嵌套结构 | 多层嵌套 | 不稳定 |

**卡片模式的最佳实践：**
- 使用`**粗体**来强调内容。
- 使用`*斜体*来表示轻量级强调。
- 使用编号列表`1.`或项目符号列表`-`。
- 避免使用`---`、`>`和内联代码。
- 保持格式简洁。

### 避免使用自动模式

**问题：** 自动模式可能会错误地选择原始文本或卡片格式。

**最佳实践：**
- 纯文本 → 使用消息工具（原始文本模式）。
- Markdown格式的内容 → 使用直接回复（卡片模式）。

**注意：**
- **不要** 使用消息工具发送Markdown格式的内容，因为它们不会被正确渲染。
- **不要** 在卡片模式中使用复杂的结构，否则可能导致格式错误。

---

## 2. 群组成员管理

### ⚠️ 重要提示：** 机器人只能看到被@提及的消息**

**机器人只能看到被@提及的消息！** 如果群组成员发送消息时没有@提及机器人，机器人将无法收到该消息。

这意味着：
- 要获取人类成员的`open_id`，需要**@提及机器人并发送消息**。
- 机器人无法查看未被@提及的过往消息。

### 如何获取成员ID

**人类用户的`open_id`（需要@提及机器人）：**
1. 让人类用户@提及机器人并发送消息。
2. 当消息到达时，系统会显示：
   `[Feishu oc_xxx:ou_xxx 时间戳] 昵称: 消息内容`
   - `ou_xxx`是发送者的`open_id`。

**机器人的`App ID`（需要用户提供）：**
1. 访问Feishu开发者控制台：https://open.feishu.cn/app
2. 点击你想要查看的机器人。
3. 在“应用凭证”（Application Credentials）中复制`App ID`（格式为`cli_xxx`）。
4. 使用`@`提及机器人并发送`App ID`。

### 维护成员列表

将成员信息存储在内存文件中：
```markdown
## Group Members (oc_xxx)
### Humans
- nickname1: `ou_xxx`
- nickname2: `ou_xxx`

### AI Bots
- bot1: `cli_xxx` (must @ to receive messages)
```

---

## 3. @提及技巧

### @提及的格式差异（非常重要！）

| 模式 | @提及格式 | 示例 |
|------|----------|---------|
| 原始文本（消息工具） | `<at user_id="ID">昵称</at>` | `<at user_id="ou_xxx">kk</at>` |
| 卡片模式（直接回复） | `<at id=ID></at>` | `<at id=ou_xxx></at>` |

### 不同的@目标类型

| @目标 | ID类型 | 原始文本格式 | 卡片格式 |
|----------|---------|------------|-------------|
| 人类用户 | `open_id`（ou_xxx） | `<at user_id="ou_xxx">昵称</at>` | `<at id=ou_xxx></at>` |
| 机器人 | `App ID`（cli_xxx） | `<at user_id="cli_xxx">机器人名称</at>` | `<at id=cli_xxx></at>` |
| 所有人 | “all” | `<at user_id="all">所有人</at>` | `<at id=all></at>` |

### @提及机器人与人类的区别

**重要提示：**
- **机器人**：**必须被@提及才能收到消息！** 如果没有@提及，机器人将无法收到消息。
- **人类用户**：可以看到所有群组消息，不需要@提及。

**⚠️ Feishu的限制：** 机器人之间的消息传递：
- 机器人可以发送消息并@提及其他机器人，但**只能接收来自人类用户的消息**。
- 因此，**@提及其他机器人时，该机器人不会收到通知**。

**实际应用建议：**
- 如果需要与其他机器人通信，请让人类用户代为发送消息。
- 在Feishu群组中，机器人之间无法直接通信。

**示例 - @提及机器人：**
```javascript
// Raw mode
message({
  action: "send",
  channel: "feishu",
  target: "oc_xxx",
  message: "<at user_id=\"cli_xxx\">botname</at> Please reply!"
})
```

```
// Card mode
<at id=cli_xxx></at> Please reply!

**Markdown content**
```

### @所有人

**注意：** 需要群组权限（群组设置 > 群组管理 > 谁可以@所有人）。

```javascript
// Raw mode
message({
  action: "send",
  channel: "feishu",
  target: "oc_xxx",
  message: "<at user_id=\"all\">everyone</at> Important announcement!"
})
```

```
// Card mode
<at id=all></at> Important announcement!
```

### 常见@提及错误

**原始文本模式的错误：**
- `@昵称` - 只是纯文本，不会触发通知。
- `@{昵称}` - 只是纯文本。
- `<at id="ou_xxx"></at>` - 在原始文本模式下，`id`属性无效。

**卡片模式的错误：**
- `<at user_id="ou_xxx">昵称</at>` - 在卡片模式下，`user_id`属性无效。

---

## 4. 快速参考

### 消息发送决策流程

```
Need to send message
    │
    ├─ Plain text only?
    │   └─ YES → message tool (Raw mode)
    │
    └─ Need Markdown?
        └─ YES → Direct reply (Card mode)
```

### @提及决策流程

```
Need to @ mention
    │
    ├─ Using message tool?
    │   └─ YES → <at user_id="ID">nickname</at>
    │
    └─ Direct reply (Card mode)?
        └─ YES → <at id=ID></at>
```

### ID格式参考

| 类型 | 格式 | 示例 |
|------|--------|---------|
| 人类用户的`open_id` | ou_xxx | ou_example123abc |
| 机器人的`App ID` | cli_xxx | cli_example456def |
| 群组聊天ID | oc_xxx | oc_example789ghi |

---

## 5. 重要说明

1. **卡片模式和原始文本模式使用不同的@提及格式** - 使用错误的格式会导致@提及失败。
2. **机器人必须被@提及才能收到消息** - 人类用户不需要@提及。
3. **机器人之间无法直接通信** - 机器人只能接收来自人类用户的消息。
4. **消息工具仅发送原始文本格式** - 不支持Markdown格式的渲染。
5. **@所有人`需要群组权限**。
6. **避免在卡片模式中使用不受支持的格式（如引用、内联代码、水平线）**。

---

## 6. 配置参考

### `renderMode`的配置位置

**配置位置：** OpenClaw配置文件或环境变量

**快速设置方法：**
```bash
# Set to card mode (recommended)
openclaw config set channels.feishu.renderMode "card"
openclaw gateway restart
```

**特定环境的配置：**

**开发环境：**
```yaml
channels:
  feishu:
    renderMode: "raw"  # Easier debugging
    dmPolicy: "open"   # Easier testing
```

**生产环境：**
```yaml
channels:
  feishu:
    renderMode: "card"      # Consistent formatting
    dmPolicy: "pairing"     # Security
    requireMention: true    # Avoid spam
```

### 故障排除

**如果消息显示为原始Markdown格式：**
1. 检查：`openclaw config get channels.feishu.renderMode`
2. 设置：`openclaw config set channels.feishu.renderMode "card"`
3. 重启：`openclaw gateway restart`

**如果消息在原始文本和卡片格式之间切换：**
- 原因：使用了`renderMode: "auto"`。
- 解决方法：将`renderMode`明确设置为“card”或“raw”。

**主动发送的消息不使用卡片格式：**
- **预期行为：** 通过`message`工具发送的主动消息应始终为纯文本。
- **解决方法：** 让用户先发送一条消息，然后再进行回复。

---

## 来源

- 在OpenClaw与Feishu的集成环境中进行了测试。
- 测试日期：2026-02-27 ~ 2026-02-28
- 相关源文件：
  - `/home/admin/.openclaw/extensions/feishu/src/bot.ts`
  - `/home/admin/.openclaw/extensions/feishu/src/reply-dispatcher.ts`
  - `/home/admin/.openclaw/extensions/feishu/src/mention.ts`
  - `/home/admin/.openclaw/extensions/feishu/src/send.ts`