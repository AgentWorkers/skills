---
name: readeck
description: 将文章保存到 Readeck（一个自托管的“稍后阅读”应用程序）中。当用户希望保存文章以备日后阅读、将其添加到阅读列表中，或将某页面发送到 Readeck 时，可以使用此功能。
---

# Readeck

将文章保存到自托管的 Readeck 实例中，以便日后阅读。

## 设置

请设置以下环境变量（在您的 shell 配置文件或 Clawdbot 配置文件中）：

```bash
export READECK_URL="https://your-readeck-instance.com"
export READECK_API_TOKEN="your-api-token"
```

要获取 API 令牌，请访问 Readeck → 设置 → API 令牌 → 创建新令牌。

## 保存文章

```bash
{baseDir}/scripts/save.sh "<URL>"
```

示例：
```bash
{baseDir}/scripts/save.sh "https://example.com/interesting-article"
```

## API 详细信息

- **端点：** `POST {READECK_URL}/api/bookmarks`
- **认证方式：** 持证令牌（Bearer token）
- **请求体：** `{"url": "..."}`

## 响应

成功时返回 `{"status": 202, "message": "链接已保存"}`。
Readeck 会自动获取并处理文章内容。