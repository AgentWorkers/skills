---
name: terminal display
description: 通过 Webhook 将消息发送到终端电子墨水显示设备。当用户希望在他们的终端显示设备上显示文本、通知或更新时，可以使用此技能。
argument-hint: [title] [message]
allowed-tools: Bash
---

# TRMNL 显示技能

该技能通过 webhook API 将内容发送到 TRMNL 电子墨水显示设备。

## Webhook 配置

- **端点：** `https://trmnl.com/api/custom_plugins/0d9e7125-789d-46a6-9a51-070ac95364d8`
- **方法：** POST
- **内容类型：** `application/json`

## 如何发送消息

使用 `curl` 发送包含 `merge_variables` 的 JSON 数据：

```bash
curl "https://trmnl.com/api/custom_plugins/0d9e7125-789d-46a6-9a51-070ac95364d8" \
  -H "Content-Type: application/json" \
  -d '{"merge_variables": {"title": "Your Title Here", "text": "Your message content here"}}' \
  -X POST
```

## 可用的合并变量

TRMNL 设备配置了一个支持以下变量的模板：

| 变量 | 描述 |
|----------|-------------|
| `title` | 显示在页面顶部的标题 |
| `text` | 标题下显示的正文内容（支持 Markdown 格式） |
| `image` | 图片的完整 URL（显示在右侧） |

## Markdown 支持

`text` 字段支持 Markdown 格式，以增强内容的可读性：

- **加粗：** `**text**`
- **斜体：** `*text*`
- **列表：** 使用 `- item` 或 `1. item`
- **换行：** 在 JSON 字符串中使用 `\n`
- **标题：** `## Heading`（请谨慎使用，因为标题本身已经很显眼）

## 使用示例

**简单通知：**
```json
{"merge_variables": {"title": "Reminder", "text": "Stand up and stretch!"}}
```

**带格式的状态更新：**
```json
{"merge_variables": {"title": "Build Status", "text": "**All tests passing**\n\nReady to deploy."}}
```

**列表格式：**
```json
{"merge_variables": {"title": "Today's Tasks", "text": "- Review PR #42\n- Update docs\n- Team standup at 10am"}}
```

**天气信息格式：**
```json
{"merge_variables": {"title": "San Francisco", "text": "**Sunny, 72°F**\n\nPerfect day for a walk"}}
```

**带图片的信息：**
```json
{"merge_variables": {"title": "Album of the Day", "text": "**Kind of Blue**\nMiles Davis", "image": "https://example.com/album-cover.jpg"}}

## Instructions for Claude

When the user asks to send something to their TRMNL device:

1. Parse the user's request to extract a title and message
2. If only a message is provided, generate an appropriate short title
3. Keep titles concise (under 30 characters recommended)
4. Keep text brief - e-ink displays work best with short, readable content
5. Use Markdown formatting to enhance readability (bold for emphasis, lists for multiple items)
6. If relevant, include an image URL (must be a fully qualified public URL)
7. Send the webhook using the curl command above
8. Confirm to the user what was sent

If the user provides arguments like `/trmnl Meeting in 5 minutes`, interpret the first few words as a potential title and the rest as the message, or use your judgment to create an appropriate title/text split.

## Response Handling

A successful response looks like:
```json
{"message":null,"merge_variables":{"title":"...","text":"..."}}
```

如果响应中出现错误信息，请及时告知用户。

## 注意事项

- 设备会定期刷新，因此内容可能不会立即显示
- 电子墨水显示屏为单色显示，不支持颜色
- 为保证在小屏幕上的可读性，请保持内容简洁
- 图片必须是完整的公共 URL（例如：`https://example.com/image.png`）
- 图片会以两列布局的形式显示在右侧