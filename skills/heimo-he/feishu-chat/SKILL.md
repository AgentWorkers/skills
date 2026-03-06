---
name: feishu-chat
description: "**Feishu（Lark）群聊消息发送指南（适用于OpenClaw）**  
本指南介绍了在Feishu群聊中使用OpenClaw发送消息的各类方式，包括原始文本（Raw）和卡片式（Card）消息格式，以及@提及功能、群组成员管理等内容。适用于需要在Feishu群组中发送消息、@用户或机器人，或使用Markdown格式化文本的场景。  
**主要内容：**  
1. **原始文本（Raw）消息**：直接输入文本进行发送。  
2. **卡片式（Card）消息**：以卡片形式展示信息，包含标题、正文和图片等元素，更美观易读。  
3. **@提及**：通过@符号指定要联系的用户或机器人。  
4. **群组成员管理**：查看/添加/删除群组成员。  
**使用示例：**  
- 使用Markdown格式化群聊消息：  
  ```
  ```markdown
  *这是一条使用Markdown格式化的消息。*
  ```
- @用户：  
  ```
  @用户名
  这是一条@用户的消息。
  ```
- 添加新成员：  
  ```
  /add 用户名
  ```
- 删除成员：  
  ```
  /remove 用户名
  ```"
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

1. 位于Feishu群组中，并且OpenClaw已连接到Feishu。
2. 配置`renderMode`为“card”以确保格式一致。
3. 了解群组成员的ID：
   - 人类用户：`open_id`（格式为`ou_xxx`）
   - 机器人：`App ID`（格式为`cli_xxx`）

---

## 0. 消息格式的稳定性

### 问题：原始文本与卡片格式的混合

如果未正确配置`renderMode`，消息可能会以以下方式显示：
- **原始文本**：纯Markdown格式，无任何格式化效果。
- **卡片格式**：带有语法高亮、表格和链接的渲染后的Markdown。

### 解决方案：明确指定`renderMode`

| 模式 | 行为 | 使用场景 |
|------|----------|----------|
| `auto` | 根据内容自动选择格式（可能为原始文本或卡片格式） | 应避免使用 |
| `raw` | 始终显示为原始文本 | 适用于仅包含纯文本的回复 |
| `card` | 始终显示为卡片格式 | 推荐使用 |

**建议设置：** 在所有生产环境中将`renderMode`设置为“card”。

---

## 1. 消息发送

### ⚠️ 重要提示：** 请仅使用一种发送方式

**切勿对同一条消息同时使用直接回复（direct reply）和消息工具（message tool）！** 这会导致系统发送两条消息。

请选择以下其中一种方式：
- 纯文本 → 仅使用消息工具
- Markdown → 仅使用直接回复

---

### 两种发送方式

| 方法 | 使用工具 | 显示格式 | 使用场景 |
|--------|------|-------------|----------|
| **消息工具（message tool）** | `message` | 原始文本（无格式化） | 适用于发送纯文本或包含@提及的内容 |
| **直接回复（direct reply）** | 会话中的直接回复 | 卡片格式（包含Markdown格式的内容） |

### 原始文本模式

**使用场景：** 发送纯文本消息或包含@提及的内容。

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
- 不支持Markdown格式化（如粗体、斜体、代码块等）。
- 不支持表格和链接。
- @提及功能可以正常使用。

### 卡片格式（Markdown）

**使用场景：** 发送包含代码块、表格和格式化文本的消息。

**发送方法：** 在会话中通过直接回复发送Markdown格式的内容。

**触发卡片格式的条件：** 包含以下任意一项：
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
<at id=ou_xxx></at> 这是一条卡片格式的消息，其中包含@提及。
```

**Markdown内容** 可以正确显示。
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
| Code blocks | ``` code ``` | 支持 |

**卡片格式不支持的内容：**

| 格式 | 语法 | 备注 |
|-------|--------|--------|
| 引用（blockquote） | `> quote` | 不支持 |
| 内联代码（inline code） | ``` `code` `` | 不支持 |
| 水平线（horizontal rule） | `---` | 不支持 |
| 复杂的嵌套结构 | 多层嵌套 | 不支持 |

**卡片格式的最佳实践：**
- 使用`**粗体**来强调重点。
- 使用`*斜体*来表示轻微的强调。
- 使用编号列表（`1.`）或项目符号列表（`-`）。
- 避免使用`---`、`>`和内联代码。
- 保持格式简单。

### 避免使用自动模式

**问题：** 自动模式可能会错误地选择原始文本或卡片格式。

**最佳实践：**
- 纯文本 → 使用消息工具（原始文本模式）。
- Markdown格式的内容 → 使用直接回复（卡片格式）。

**注意：**
- 不要用消息工具发送Markdown格式的内容（因为无法正确显示）。
- 在卡片格式中避免使用复杂的结构，否则可能会导致错误。

---

## 2. 群组成员管理

### ⚠️ 重要提示：** 机器人只能看到被@提及的消息

**机器人只能看到被@提及的消息！** 如果群组成员发送消息时没有@提及机器人，机器人将无法收到该消息。

这意味着：
- 要获取人类用户的`open_id`，需要**@提及机器人并发送消息**。
- 机器人无法查看未被@提及的过往消息。

### 如何获取成员ID

**人类用户的`open_id`（需要被@提及）：**
1. 让人类用户@提及机器人并发送消息。
2. 当消息到达后，系统会显示：
   `[Feishu oc_xxx:ou_xxx 时间戳] 昵称: 消息内容`
   - `ou_xxx` 是发送者的`open_id`。

**机器人的`App ID`（需要用户提供）：**
1. 访问Feishu开发者控制台：https://open.feishu.cn/app
2. 选择你想要查看的机器人。
3. 在“应用凭证”（Application Credentials）中复制`App ID`（格式为`cli_xxx`）。
4. 使用`App ID`@提及机器人并发送消息。

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
| 原始文本（使用消息工具） | `<at user_id="ID">昵称</at>` | `<at user_id="ou_xxx">kk</at>` |
| 卡片格式（直接回复） | `<at id=ID></at>` | `<at id=ou_xxx></at>` |

### 不同的@提及目标类型

| @提及对象 | ID类型 | 原始文本格式 | 卡片格式 |
|----------|---------|------------|-------------|
| 人类用户 | `open_id`（格式为`ou_xxx`） | `<at user_id="ou_xxx">昵称</at>` | `<at id=ou_xxx></at>` |
| 机器人 | `App ID`（格式为`cli_xxx`） | `<at user_id="cli_xxx">机器人名称</at>` | `<at id=cli_xxx></at>` |
| 所有人 | “all” | `<at user_id="all">所有人</at>` | `<at id=all></at>` |

### @提及机器人与人类的区别

**重要提示：**
- **机器人**：**必须被@提及才能收到消息！** 如果没有@提及，机器人将无法收到消息。
- **人类用户**：可以看到所有群组的消息，不需要@提及。

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

### @提及所有人

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

### 常见错误

**原始文本模式下的错误：**
- `@昵称`：仅显示为纯文本，不会触发通知。
- `@{昵称}`：仅显示为纯文本。
- `<at id="ou_xxx"></at>`：在原始文本模式下，`id`属性无效。

**卡片格式下的错误：**
- `<at user_id="ou_xxx">昵称</at>`：在卡片格式下，`user_id`属性无效。

---

## 4. 快速参考

### 消息发送方式的选择流程

```
Need to send message
    │
    ├─ Plain text only?
    │   └─ YES → message tool (Raw mode)
    │
    └─ Need Markdown?
        └─ YES → Direct reply (Card mode)
```

### @提及的使用流程

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
| 人类用户的`open_id` | `ou_xxx` | `ou_example123abc` |
| 机器人的`App ID` | `cli_xxx` | `cli_example456def` |
| 群组聊天ID | `oc_xxx` | `oc_example789ghi` |

---

## 5. 重要注意事项

1. **卡片格式和原始文本模式使用不同的@提及格式**——使用错误的格式会导致@提及失败。
2. **机器人必须被@提及才能收到消息**——人类用户不需要@提及。
3. **机器人之间无法直接通信**——机器人只能接收来自人类用户的消息。
4. **消息工具仅发送原始文本格式的消息**——不支持Markdown格式化。
5. **@提及所有人需要群组权限**。
6. **在卡片格式中避免使用不支持的格式（如引用、内联代码、水平线）**。

---

## 6. 配置参考

### `renderMode`的配置位置

**配置位置：** OpenClaw的配置文件或环境变量。

**快速设置方法：**
```bash
# Set to card mode (recommended)
openclaw config set channels.feishu.renderMode "card"
openclaw gateway restart
```

**针对不同环境的配置：**

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
1. 检查：`openclaw config get channels.feishu.renderMode`。
2. 设置：`openclaw config set channels.feishu.renderMode "card"`。
3. 重启：`openclaw gateway restart`。

**如果消息在原始文本和卡片格式之间切换：**
- 原因：使用了`renderMode: "auto"`。
- 解决方法：将`renderMode`明确设置为“card”或“raw”。

**主动发送的消息不使用卡片格式：**
- **预期行为：** 通过`message`工具发送的主动消息应始终为原始文本格式。
- **解决方法：** 让用户先发送一条消息，然后再进行回复。

---

## 资料来源

- 在OpenClaw与Feishu的集成环境中进行了测试。
- 测试时间：2026-02-27 ~ 2026-02-28。
- 相关源文件：
  - `/home/admin/.openclaw/extensions/feishu/src/bot.ts`
  - `/home/admin/.openclaw/extensions/feishu/src/reply-dispatcher.ts`
  - `/home/admin/.openclaw/extensions/feishu/src/mention.ts`
  - `/home/admin/.openclaw/extensions/feishu/src/send.ts`