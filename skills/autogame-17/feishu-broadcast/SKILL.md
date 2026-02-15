# Feishu 广播技能

该技能用于向 Feishu 租户内的所有用户发送消息（包括纯文本和富文本）、图片以及贴纸。

## 功能特点
- **动态用户列表**：通过 Feishu API 获取所有用户信息（不使用硬编码的用户名）。
- **富文本支持**：支持使用 `feishu-post` 标记语言编写富文本内容。
- **媒体文件支持**：支持上传图片和 GIF 动画（通过 `feishu-sticker` 功能）。
- **安全性保障**：具备速率限制机制，并支持“试运行”模式（Dry Run）。

## 使用方法

```bash
# Send text
node skills/feishu-broadcast/index.js --title "Announcement" --text "Hello Everyone!"

# Send text from file (recommended for long messages)
node skills/feishu-broadcast/index.js --title "Weekly Report" --text-file "report.md"

# Send sticker
node skills/feishu-broadcast/index.js --image "media/sticker.webp"

# Combined
node skills/feishu-broadcast/index.js --title "Hi" --text "Check this out" --image "media/cool.gif"
```

## 所需依赖的技能
- `feishu-post` 技能（必须已安装）
- `feishu-sticker` 技能（必须已安装）