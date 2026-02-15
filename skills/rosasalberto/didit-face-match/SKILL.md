---
name: didit-face-match
description: >
  Integrate Didit Face Match standalone API to compare two facial images.
  Use when the user wants to compare faces, verify face identity, implement biometric
  comparison, facial recognition, or selfie-to-document matching using Didit.
  Returns a similarity score (0-100) with configurable decline threshold.
  Supports image rotation and multi-face detection.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "👥"
    homepage: https://docs.didit.me
---

# Didit 面部匹配 API

## 概述

该 API 用于比较两张面部图像，以确定它们是否属于同一个人，并返回一个相似度分数（0-100）。

**主要限制：**
- 支持的格式：JPEG、PNG、WebP、TIFF
- 每张图片的最大文件大小为 5MB
- 如果图片中有多张面部，将使用**最大的面部**进行比较
- `user_image` 和 `ref_image` 都是必填项

**功能：**
- 相似度评分
- 年龄估算
- 性别检测
- 面部边界框提取
- 可配置的拒绝阈值
- 可选的功能：对非正立的面部进行旋转处理

**API 参考文档：** https://docs.didit.me/reference/face-match-standalone-api

---

## 认证

所有请求都需要包含 `x-api-key` 标头。请从 [Didit 商业控制台](https://business.didit.me) → API & Webhooks) 获取您的 API 密钥。

---

## 端点

```
POST https://verification.didit.me/v3/face-match/
```

### 请求头

| 标头 | 值 | 是否必填 |
|---|---|---|
| `x-api-key` | 您的 API 密钥 | 是 |
| `Content-Type` | `multipart/form-data` | 是 |

### 请求参数（multipart/form-data）

| 参数 | 类型 | 是否必填 | 默认值 | 限制 | 说明 |
|---|---|---|---|---|
| `user_image` | 文件 | 是 | — | JPEG/PNG/WebP/TIFF 格式，最大 5MB | 需要验证的用户面部图像 |
| `ref_image` | 文件 | 是 | — | 用于比较的参考图像 |
| `face_match_score_decline_threshold` | 整数 | 否 | `30` | 分数低于此值则拒绝请求 |
| `rotate_image` | 布尔值 | 否 | `false` | — | 尝试将图像旋转 0/90/180/270 度以调整面部方向 |
| `save_api_request` | 布尔值 | 否 | `true` | — | 是否将请求结果保存到商业控制台的手动检查记录中 |
| `vendor_data` | 字符串 | 否 | — | 用于会话跟踪的标识符 |

### 示例

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/face-match/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={
        "user_image": ("selfie.jpg", open("selfie.jpg", "rb"), "image/jpeg"),
        "ref_image": ("id_photo.jpg", open("id_photo.jpg", "rb"), "image/jpeg"),
    },
    data={"face_match_score_decline_threshold": "50"},
)
```

```typescript
const formData = new FormData();
formData.append("user_image", selfieFile);
formData.append("ref_image", referenceFile);
formData.append("face_match_score_decline_threshold", "50");

const response = await fetch("https://verification.didit.me/v3/face-match/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### 响应（200 OK）

```json
{
  "request_id": "a1b2c3d4-...",
  "face_match": {
    "status": "Approved",
    "score": 80,
    "user_image": {
      "entities": [
        {"age": 27.63, "bbox": [40, 40, 100, 100], "confidence": 0.717, "gender": "male"}
      ],
      "best_angle": 0
    },
    "ref_image": {
      "entities": [
        {"age": 22.16, "bbox": [156, 234, 679, 898], "confidence": 0.717, "gender": "male"}
      ],
      "best_angle": 0
    },
    "warnings": []
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### 状态码及其含义及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Approved"` | 分数大于或等于阈值 | 面部匹配成功，可继续处理 |
| `"Declined"` | 分数低于阈值或未检测到面部 | 查看 `warnings` 以获取详细信息（可能需要更清晰的图像） |
| `"In Review"` | 需要人工审核 | 等待审核结果或通过会话 API 获取审核结果 |

### 错误响应

| 错误代码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求无效 | 检查文件格式、大小和参数 |
| `401` | API 密钥无效 | 请验证 `x-api-key` 标头 |
| `403` | 信用不足 | 请在 business.didit.me 充值 |

---

## 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `status` | 字符串 | `"Approved"`, `"Declined"`, `"In Review"` |
| `score` | 整数 | 0-100 的相似度分数（分数越高，相似度越高）；`null` 表示未检测到面部 |
| `entities[].age` | 浮点数 | 估计的年龄 |
| `entities[].bbox` | 数组 | 面部边界框（格式：`[x1, y1, x2, y2]`） |
| `entities[].confidence` | 浮点数 | 面部检测的置信度（0-1） |
| `entities[].gender` | 字符串 | `"male"` 或 `"female"` |
| `best_angle` | 整数 | 最适合显示面部的旋转角度 |
| `warnings` | 数组 | `{risk, log_type, short_description, long_description}` | 报告中的风险信息 |

---

## 警告标签

| 标签 | 说明 | 自动拒绝条件 |
|---|---|---|
| `NO_REFERENCE_IMAGE` | 参考图像或面部图像缺失 | 是 |
| `NO_FACE_DETECTED` | 一张或两张图像中均未检测到面部 | 是 |
| `LOW_FACE_MATCH_SIMILARITY` | 分数低于阈值，可能存在身份不匹配 | 可配置 |

> **安全最佳实践：** 仅存储状态码和相似度分数，尽量减少在服务器上存储生物特征图像数据。在流程模式下，图像链接会在 60 分钟后失效。

---

## 分数解读

| 分数范围 | 解释 | 处理方式 |
|---|---|---|
| 90-100 | 非常高的置信度——同一人 | 自动批准 |
| 70-89 | 高置信度——很可能是同一个人 | 批准（默认阈值：30） |
| 50-69 | 中等置信度——可能存在匹配 | 考虑进行人工审核 |
| 30-49 | 低置信度——很可能是不同的人 | 拒绝（默认阈值） |
| 0-29 | 非常低的置信度——不同的人 | 拒绝 |

---

## 实用脚本

```bash
export DIDIT_API_KEY="your_api_key"

python scripts/match_faces.py selfie.jpg id_photo.jpg
python scripts/match_faces.py selfie.jpg id_photo.jpg --threshold 50 --rotate
```