---
name: publora-bluesky
description: 使用 Publora API 在 Bluesky 上发布或安排内容。当用户希望通过 Publora 在 Bluesky 上发布或安排帖子时，可以使用此技能。
---
# Publora — Bluesky

通过 Publora API 发布和安排 Bluesky 的内容。

> **前提条件：** 需要安装 `publora` 核心插件以进行身份验证设置并获取平台 ID。

## 平台 ID 格式

`bluesky-{did}` — Bluesky 使用基于 **DID（Digital Identifier）** 的 ID，而不是数字 ID。

示例：`bluesky-did:plc:abc123xyz`

您可以通过 `GET /api/v1/platform-connections` 获取您的确切 DID。

## 身份验证

Bluesky 需要：
- **用户名**（例如：`yourname.bsky.social`）
- **应用密码** — **请勿使用您的主账户密码**

您可以在 Bluesky 设置 → **应用密码** 中生成应用密码。

⚠️ 使用主账户密码存在安全风险。在进行 API 集成时，请始终使用应用密码。

## 字符长度限制

**严格限制为 300 个字符**。如果超过此限制，API 会返回错误。

## 支持的内容类型

| 类型 | 是否支持 | 备注 |
|------|-----------|-------|
| 仅文本 | ✅ | 最多 300 个字符 |
| 图片 | ✅ | 每篇文章最多可添加 4 张图片；建议使用 JPEG 格式；WebP 格式的图片会自动转换为 JPEG |
| 视频 | ❌ | 目前不支持 |
| 标签 | ✅ | 标签会自动被检测并变为可点击的链接 |
| URL | ✅ | URL 会自动被检测并变为可点击的链接 |

## 向 Bluesky 发布内容

```python
import requests

response = requests.post(
    'https://api.publora.com/api/v1/create-post',
    headers={
        'Content-Type': 'application/json',
        'x-publora-key': 'sk_YOUR_KEY'
    },
    json={
        'content': 'Dashboard live! #buildinpublic',
        'platforms': ['bluesky-did:plc:abc123xyz']
    }
)
print(response.json())
```

## 发布带有图片的内容

每篇文章最多可以添加 **4 张图片**。每张图片都需要使用相同的 `postGroupId` 调用 `get-upload-url` 方法进行上传。

使用 `altTexts` 数组来提高图片的可访问性 — `altTexts` 的顺序与上传图片的顺序一致。

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post with altTexts
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Dashboard live! #buildinpublic',
    'platforms': ['bluesky-did:plc:abc123xyz'],
    'altTexts': ['Screenshot of analytics dashboard showing user growth charts']
}).json()
post_group_id = post['postGroupId']

# Step 2: Get upload URL (one call per image)
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'dashboard.jpg', 'contentType': 'image/jpeg',
    'type': 'image', 'postGroupId': post_group_id
}).json()

# Step 3: Upload to S3
with open('dashboard.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

### 带有 altText 的多张图片

```python
json={
    'content': 'New features shipping this week! 🚀 #indiedev',
    'platforms': ['bluesky-did:plc:abc123xyz'],
    'altTexts': [
        'Screenshot of the new dashboard with dark mode enabled',
        'Mobile view of the app showing the updated navigation',
        'Code editor integration screenshot'
    ]
}
# Then upload 3 images with same postGroupId
# altTexts map positionally: index 0 → first uploaded image, etc.
```

**关于 WebP 格式的图片：** Publora 会自动将 WebP 格式的图片转换为 JPEG 格式。

## 富文本 — 自动检测

Publora 会自动检测并转换 **标签** 和 **URL** 为可点击的链接：

- `#hashtag` → 变为可点击的标签链接
- `https://example.com` → 变为可点击的 URL 链接

您无需进行任何特殊操作 — 只需将它们包含在内容字符串中即可。Publora 会内部处理 Bluesky AT 协议所需的字节偏移量计算。

## 安排文章发布

```python
json={
    'content': 'Shipping on Friday! Stay tuned 👀 #buildinpublic',
    'platforms': ['bluesky-did:plc:abc123xyz'],
    'scheduledTime': '2026-03-16T10:00:00.000Z'
}
```

## 关于 Bluesky 的使用提示：

- **DID 格式**：平台 ID 的格式为 `bluesky-did:plc:xyz`，而不是数字 ID
- **需要应用密码** — 请勿使用主账户密码
- **字符长度限制**：严格限制为 300 个字符
- **标签会自动链接**：Publora 会自动处理 AT 协议相关的链接
- **提供 altText**：为了提高可访问性，请务必为图片提供 altText；altText 的顺序与上传图片的顺序一致
- **最多 4 张图片**：每张图片都需要单独调用 `get-upload-url` 方法进行上传，且所有图片都需要使用相同的 `postGroupId`