# Feishu 发文（富文本）技能

用于向 Feishu 发送富文本（Post）消息。这种格式与卡片（Cards）不同，它支持原生的富文本元素，但在布局上不如卡片灵活。它更适合包含图片/链接的长篇文本。

## 前提条件

- 请先安装 `feishu-common`。
- 该技能通过 `utils/feishu-client.js` 依赖于 `../feishu-common/index.js`。

## 功能特点
- **原生表情符号支持**：会自动将 `[微笑]`、 `[得意]` 等表情符号转换为 Feishu 的原生表情标签。
- **类似 Markdown 的解析**：支持简单的换行符和段落格式。
- **富文本格式**：使用 Feishu 的发文内容结构。

## 使用方法

```bash
node skills/feishu-post/send.js --target "ou_..." --text-file "temp/msg.md" --title "Optional Title"
```

## 参数选项
- `-t, --target <id>`：目标 ID（用户 `ou_...` 或聊天室 `oc_...`）。
- `-x, --text <text>`：文本内容（支持使用 `\n` 表示换行，以及 `[emoji]` 标签）。
- `-f, --text-file <path>`：从文件中读取内容。
- `--title <text>`：帖子的标题。
- `--reply-to <id>`：要回复的消息 ID。

## 表情符号列表
支持的表情符号包括：`[微笑]`、`[色]`、`[亲亲]`、`[大哭]`、`[强]` 等。  
完整的表情符号映射请参见 `emoji-map.js`。