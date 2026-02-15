---
name: didit-face-search
description: >
  Integrate Didit Face Search standalone API to perform 1:N facial search against all
  previously verified sessions. Use when the user wants to detect duplicate accounts,
  search for matching faces, check if a face already exists in the system, prevent
  duplicate registrations, search against blocklist, or implement facial deduplication
  using Didit. Returns ranked matches with similarity percentages.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🔍"
    homepage: https://docs.didit.me
---

# Didit 面部搜索 API (1:N)

## 概述

该 API 会将参考面部图像与系统中所有已批准的验证记录进行比对，以检测重复账户和被列入黑名单的面部信息，并返回按相似度排序的匹配结果。

**主要限制：**
- 支持的文件格式：JPEG、PNG、WebP、TIFF
- 最大文件大小：5MB
- 仅与系统中所有已批准的验证记录进行比对
- 如果匹配结果来自黑名单中的面部信息，系统会自动拒绝该请求

**相似度评分说明：**

| 相似度范围 | 解释 |
|---|---|
| 90%及以上 | 高度可能为同一人 |
| 70-89% | 可能匹配，需要人工审核 |
| 低于70% | 可能为不同的人 |

**API 参考文档：** https://docs.didit.me/reference/face-search-standalone-api

---

## 认证

所有请求都必须包含 `x-api-key` 头部字段。您可以从 [Didit 商业控制台](https://business.didit.me) 获取 API 密钥。

---

## 端点

```
POST https://verification.didit.me/v3/face-search/
```

### 请求头

| 头部字段 | 值 | 是否必需 |
|---|---|---|
| `x-api-key` | 您的 API 密钥 | 是 |
| `Content-Type` | `multipart/form-data` | 是 |

### 请求参数（multipart/form-data）

| 参数 | 类型 | 是否必需 | 默认值 | 说明 |
|---|---|---|---|
| `user_image` | 文件 | 是 | 需要搜索的面部图像（格式：JPEG/PNG/WebP/TIFF，最大大小 5MB） |
| `rotate_image` | 布尔值 | 否 | `false` | 对非垂直方向的面部图像尝试旋转 0/90/180/270 度 |
| `save_api_request` | 布尔值 | 否 | `true` | 是否将请求结果保存到商业控制台 |
| `vendor_data` | 字符串 | 否 | 用于会话跟踪的唯一标识符 |

### 示例请求

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/face-search/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={"user_image": ("photo.jpg", open("photo.jpg", "rb"), "image/jpeg")},
)
print(response.json())
```

```typescript
const formData = new FormData();
formData.append("user_image", photoFile);

const response = await fetch("https://verification.didit.me/v3/face-search/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### 响应（200 OK）

```json
{
  "request_id": "a1b2c3d4-...",
  "face_search": {
    "status": "Approved",
    "total_matches": 1,
    "matches": [
      {
        "session_id": "uuid-...",
        "session_number": 1234,
        "similarity_percentage": 95.2,
        "vendor_data": "user-456",
        "verification_date": "2025-06-10T10:30:00Z",
        "user_details": {
          "name": "Elena Martinez",
          "document_type": "Identity Card",
          "document_number": "***456"
        },
        "match_image_url": "https://example.com/match.jpg",
        "status": "Approved",
        "is_blocklisted": false
      }
    ],
    "user_image": {
      "entities": [
        {"age": "27.6", "bbox": [40, 40, 120, 120], "confidence": 0.95, "gender": "female"}
      ],
      "best_angle": 0
    },
    "warnings": []
  }
}
```

### 状态码及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Approved"` | 未找到匹配记录 | 继续处理——新用户 |
| `"In Review"` | 匹配结果满足相似度阈值 | 审查 `matches[]` 以确认是否存在重复账户 |
| `"Declined"` | 匹配结果来自黑名单或违反政策 | 检查 `matches[].is_blocklisted` 和 `warnings` |

### 错误响应

| 错误代码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求无效 | 检查文件格式、大小和参数是否正确 |
| `401` | API 密钥无效 | 请验证 `x-api-key` 头部字段 |
| `403` | 信用不足 | 请在 business.didit.me 充值 |

---

## 响应字段说明

### 匹配结果对象

| 字段 | 类型 | 说明 |
|---|---|---|
| `session_id` | 字符串 | 匹配记录的会话 ID |
| `session_number` | 整数 | 会话编号 |
| `similarity_percentage` | 浮点数 | 相似度评分（0-100%） |
| `vendor_data` | 字符串 | 来自匹配记录的标识信息 |
| `verification_date` | 字符串 | ISO 8601 格式的时间戳 |
| `user_details.name` | 字符串 | 对应用户的姓名 |
| `user_details.document_type` | 字符串 | 使用的证件类型 |
| `user_details.document_number` | 字符串 | 部分屏蔽的证件编号 |
| `match_image_url` | 字符串 | 临时 URL（有效期 60 分钟） |
| `status` | 字符串 | 匹配记录的状态 |
| `is_blocklisted` | 布尔值 | 匹配结果是否来自黑名单 |

### 用户面部图像对象

| 字段 | 类型 | 说明 |
|---|---|---|
| `entities[].age` | 字符串 | 估计年龄 |
| `entities[].bbox` | 数组 | 面部边界框 `[x1, y1, x2, y2]` |
| `entities[].confidence` | 浮点数 | 检测置信度（0-1） |
| `entities[].gender` | 字符串 | 性别（`male` 或 `female`） |
| `best_angle` | 整数 | 应用的旋转角度（0, 90, 180, 270） |

---

## 警告标签

### 自动拒绝

| 标签 | 说明 |
|---|---|
| `NO_FACE_DETECTED` | 图像中未检测到面部信息 |
| `FACE_IN_BLOCKLIST` | 匹配结果来自黑名单 |

### 可配置选项

| 标签 | 说明 |
|---|---|
| `MULTIPLE_FACES_DETECTED` | 检测到多个面部——无法确定使用哪个面部信息 |

> 相似度阈值和“允许多个面部”的设置可在商业控制台进行配置。

警告级别：`error`（→ 自动拒绝），`warning`（→ 进入审核），`information`（→ 无影响）。

---

## 常见使用场景

### 重复账户检测

```
1. During new user registration
2. POST /v3/face-search/ → {"user_image": selfie}
3. If total_matches == 0 → new unique user
   If matches found → check similarity_percentage:
     90%+ → likely duplicate, investigate matches[].vendor_data
     70-89% → possible match, flag for manual review
```

### 综合验证 + 重复账户检测

```
1. POST /v3/passive-liveness/ → verify user is real
2. POST /v3/face-search/ → check for existing accounts
3. POST /v3/id-verification/ → verify identity document
4. POST /v3/face-match/ → compare selfie to document photo
5. All Approved → verified, unique, real user
```

> **安全提示：** 匹配结果的临时 URL 有效期为 60 分钟。请仅存储 `session_id` 和 `similarity_percentage`，以减少服务器上的生物特征数据存储量。