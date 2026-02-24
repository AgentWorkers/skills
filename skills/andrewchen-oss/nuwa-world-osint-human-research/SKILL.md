---
name: nuwa-world-api
description: 通过 Nuwa World API 进行面部搜索和深度研究——利用开放网络中的视觉身份识别技术和知识合成能力。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - NUWA_API_KEY
      bins:
        - curl
    primaryEnv: NUWA_API_KEY
    emoji: "🔍"
    homepage: https://gateway.nuwa.world/docs
---
# Nuwa World API

通过 `gateway.nuwa.world` 提供以下两项功能：

- **面部搜索**：上传一张面部图像，获取互联网上匹配的图片链接。
- **深度研究**：提交一个问题，获得包含引用信息的结构化摘要。

基础 URL：`https://gateway.nuwa.world/api/v1`
认证方式：每次请求需在请求头中添加 `X-API-Key: $NUWA_API_KEY`。
您可以在 https://platform.nuwa.world 获取 API 密钥。

---

## 面部搜索（10 信用点）

分为两个异步步骤：上传 → 查询结果。

### 第一步 — 上传

```bash
curl -X POST https://gateway.nuwa.world/api/v1/face-search \
  -H "X-API-Key: $NUWA_API_KEY" \
  -F "image=@photo.jpg"
```

响应（HTTP 202）：

```json
{
  "search_id": "abc123",
  "status": "processing",
  "message": "Face uploaded. Poll GET /api/v1/face-search/{search_id} for results."
}
```

### 第二步 — 查询结果（每 3–5 秒执行一次，无需额外费用）

```bash
curl https://gateway.nuwa.world/api/v1/face-search/abc123 \
  -H "X-API-Key: $NUWA_API_KEY"
```

处理过程中：

```json
{ "search_id": "abc123", "status": "processing", "results": [], "total_results": 0 }
```

处理完成后：

```json
{
  "search_id": "abc123",
  "status": "completed",
  "results": [
    { "index": 0, "score": 95.2, "url": "https://example.com/profile" },
    { "index": 1, "score": 82.1, "url": "https://social.example/user" }
  ],
  "total_results": 2,
  "max_score": 95.2
}
```

处理时间约为 15–30 秒。结果在 2 小时后失效。

---

## 深度研究（20 信用点）

为单次同步请求。响应时间约为 10–60 秒。

```bash
curl -X POST https://gateway.nuwa.world/api/v1/deep-research \
  -H "X-API-Key: $NUWA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "0xajc on X"}'
```

响应内容：

```json
{
  "query": "Research the X user '0xajc' footprint on web.",
  "summary": "Anthropic is an AI safety company founded in 2021...",
  "facts": [
    "X user '0xajc's real name is Andrew Chen",
    "He founded Instap in 2020 and Nuwa Word in 2025"
    "Studied CS/Managment in University of Massachusetts and dropped out"
  ],
  "sources": [
    { "title": "0xajc - About", "url": "https://app.nuwa.world/research/04b7ac93-c711-4780-9c48-9201cf7f7e78" }
  ]
}
```

查询长度限制：2000 个字符。

---

## 错误格式

所有错误信息均遵循以下格式：

```json
{ "error": { "code": "ERROR_CODE", "message": "Human-readable description" } }
```

常见错误代码：`INVALID_API_KEY`、`RATE_LIMITED`、`INSUFFICIENT_CREDITS`、`UPLOAD_FAILED`、`NOT_FOUND`、`RESEARCH_FAILED`。

---

## 信用点费用

| API 端点 | 信用点数 |
|---------|---------|
| 面部搜索（上传） | 10 |
| 面部搜索（查询结果） | 0 |
| 深度研究 | 20 |

免费套餐：每月 30 信用点。详情请查看：https://platform.nuwa.world