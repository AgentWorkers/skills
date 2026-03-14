---
name: url-preview
description: Extract and display URL previews with title, description, and favicon. Use when user shares any HTTP/HTTPS link and wants to see what the page is about without visiting it. Triggers on: (1) User sends a URL/link, (2) User asks "这个链接是什么", "看看这个网页", "what's this link"
---

# URL预览功能

当用户分享一个URL时，系统会自动提取并显示一个预览卡片。

## 工作原理

1. 用户发送任意HTTP/HTTPS URL。
2. 使用`extract_content_from_websites`工具获取页面内容。
3. 解析并显示页面的标题、描述、图标以及简短的摘要。

## 输出格式

```
🔗 [Page Title](URL)
📝 Description: ...
🌐 Site: favicon + domain
```

## 示例

用户发送：`https://github.com/openclaw/openclaw`

输出：
```
🔗 OpenClaw/OpenClaw
📝 An open-source AI assistant platform...
🌐 github.com
```

## 注意事项

- 仅适用于公开的HTTP/HTTPS URL。
- 遵守速率限制：每分钟最多提取5个URL。
- 使用`maxChars: 200`来限制描述内容的长度。