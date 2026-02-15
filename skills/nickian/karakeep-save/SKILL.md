---
name: karakeep
description: 将书签保存到 Karakeep（一个自托管的书签管理工具）中。当用户需要保存某个 URL、将链接添加到书签中或将其添加到阅读列表时，可以使用该工具。
---

# Karakeep

将书签保存到自托管的 Karakeep 实例中。

## 设置

请设置以下环境变量（在您的 shell 配置文件或 Clawdbot 配置文件中）：

```bash
export KARAKEEP_URL="https://your-karakeep-instance.com"
export KARAKEEP_API_KEY="your-api-key"
```

要获取您的 API 密钥，请访问 Karakeep → 设置 → API 密钥 → 创建新密钥。

## 保存书签

```bash
{baseDir}/scripts/save.sh "<URL>" ["optional note"]
```

示例：
```bash
{baseDir}/scripts/save.sh "https://example.com/article"
{baseDir}/scripts/save.sh "https://github.com/repo" "Interesting project to check out"
```

## API 详情

- **端点：** `POST {KARAKEEP_URL}/api/v1/bookmarks`
- **认证方式：** 承载令牌（Bearer token）
- **请求体：** `{"type": "link", "url": "...", "note": "..."}`

## 响应

返回包含书签 ID 的 JSON 数据。标签将由 Karakeep 的 AI 自动生成。