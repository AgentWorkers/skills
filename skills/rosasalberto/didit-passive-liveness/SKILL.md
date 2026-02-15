---
name: didit-passive-liveness
description: >
  Integrate Didit Passive Liveness standalone API to verify a user is physically present.
  Use when the user wants to check liveness, detect spoofing attempts, verify real person
  presence, implement anti-spoofing, or perform passive liveness detection using Didit.
  Analyzes a single image without user interaction. Returns liveness score, face quality,
  and luminance metrics. Detects presentation attacks and duplicate faces.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🧑"
    homepage: https://docs.didit.me
---

# Didit 被动式活体检测 API

## 概述

通过分析单张捕获的图像来验证用户是否真实存在——无需用户进行任何明显的动作或交互。

**主要限制：**
- 支持的格式：**JPEG、PNG、WebP、TIFF**
- 文件最大大小：**5MB**
- 图像中必须包含**一个清晰可见的脸部**
- 仅支持原始的实时照片（禁止使用截图或打印的照片）

**准确率：**活体检测准确率为 99.9%，误接受率（FAR）低于 0.1%。

**功能：**活体评分、面部质量评估、亮度分析、年龄/性别估计、欺诈检测（如屏幕截图、打印照片、面具、深度伪造图像）、跨会话的重复面部检测、黑名单匹配。

**活体检测方法：**该独立端点使用 **被动式** 方法（单帧卷积神经网络，PASSIVE）。工作流程模式还支持 **主动式 3D** 方法（需要用户动作和闪光灯，安全性最高）和 **闪光式** 方法（使用闪光灯，安全性也很高）。

**API 参考：** https://docs.didit.me/reference/passive-liveness-api

---

## 认证

所有请求都必须包含 `x-api-key` 标头。请从 [Didit 商业控制台](https://business.didit.me) 获取您的 API 密钥。

---

## 端点

```
POST https://verification.didit.me/v3/passive-liveness/
```

### 标头

| 标头 | 值 | 是否必需 |
|---|---|---|
| `x-api-key` | 您的 API 密钥 | **是** |
| `Content-Type` | `multipart/form-data` | **是** |

### 请求参数（multipart/form-data）

| 参数 | 类型 | 是否必需 | 默认值 | 限制 | 说明 |
|---|---|---|---|---|
| `user_image` | 文件 | **是** | — | JPEG/PNG/WebP/TIFF，最大 5MB | 用户的面部图像 |
| `face_liveness_score_decline_threshold` | 整数 | 否 | — | 0-100 | 低于此分数则拒绝请求 |
| `rotate_image` | 布尔值 | 否 | — | — | 尝试旋转图像以找到正立的面部 |
| `save_api_request` | 布尔值 | 否 | `true` | — | 是否将结果保存到商业控制台 |
| `vendor_data` | 字符串 | 否 | — | — | 用于会话跟踪的标识符 |

### 示例

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/passive-liveness/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={"user_image": ("selfie.jpg", open("selfie.jpg", "rb"), "image/jpeg")},
    data={"face_liveness_score_decline_threshold": "80"},
)
```

```typescript
const formData = new FormData();
formData.append("user_image", selfieFile);
formData.append("face_liveness_score_decline_threshold", "80");

const response = await fetch("https://verification.didit.me/v3/passive-liveness/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### 响应（200 OK）

```json
{
  "request_id": "a1b2c3d4-...",
  "liveness": {
    "status": "Approved",
    "method": "PASSIVE",
    "score": 95,
    "user_image": {
      "entities": [
        {"age": 22.16, "bbox": [156, 234, 679, 898], "confidence": 0.717, "gender": "male"}
      ],
      "best_angle": 0
    },
    "warnings": [],
    "face_quality": 85.0,
    "face_luminance": 50.0
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### 状态码及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Approved"` | 用户真实存在 | 继续执行您的流程 |
| `"Declined"` | 活体检测失败 | 查看 `warnings`（可能为欺诈行为或图像质量不佳） |

### 错误响应

| 错误码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求无效 | 检查文件格式、大小和参数 |
| `401` | API 密钥无效 | 确认 `x-api-key` 标头是否正确 |
| `403` | 信用不足 | 请在 business.didit.me 上充值 |

---

## 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `status` | 字符串 | `"Approved"` 或 `"Declined"` |
| `method` | 字符串 | 该端点的方法始终为 `"PASSIVE"` |
| `score` | 整数 | 0-100 的活体检测置信度（分数越高，真实性越高）；无面部时返回 `null` |
| `face_quality` | 浮点数 | 面部图像质量得分（0-100）；无面部时返回 `null` |
| `face_luminance` | 浮点数 | 面部亮度值；无面部时返回 `null` |
| `entities[].age` | 浮点数 | 估计年龄 |
| `entities[].bbox` | 数组 | 面部边界框 `[x1, y1, x2, y2]` |
| `entities[].confidence` | 浮点数 | 面部检测置信度（0-1） |
| `entities[].gender` | 字符串 | `"male"` 或 `"female"` |
| `warnings` | 数组 | `{风险、日志类型、简短描述、详细描述}` |

---

## 警告标签

### 自动拒绝（始终适用）

| 标签 | 说明 |
|---|---|
| `NO_FACE_DETECTED` | 图像中未检测到面部 |
| `LIVENESS_FACE_ATTACK` | 可能存在欺诈行为（如使用打印照片、屏幕截图或面具） |
| `FACE_IN_BLOCKLIST` | 面部与黑名单中的条目匹配 |
| `POSSIBLE_FACE_IN_BLOCKLIST` | 可能与黑名单中的条目匹配 |

### 可配置的拒绝/审核/批准规则

| 标签 | 说明 | 备注 |
|---|---|---|
| `LOW_LIVENESS_SCORE` | 评分低于阈值 | 可配置审核和拒绝的阈值 |
| `DUPLICATED_FACE` | 与已批准的会话中的面部匹配 | — |
| `POSSIBLE_DUPLICATED_FACE` | 可能与其他用户面部匹配 | 可配置相似度阈值 |
| `MULTIPLE_FACES_DETECTED` | 检测到多个面部（以最大检测到的面部为准） | 仅适用于被动式检测 |
| `LOW_FACE_QUALITY` | 图像质量低于阈值 | 仅适用于被动式检测 |
| `LOW_FACE_LUMINANCE` | 图像过暗 | 仅适用于被动式检测 |
| `HIGH_FACE_LUMINANCE` | 图像过亮/曝光过度 | 仅适用于被动式检测 |

---

## 常见工作流程

### 基本活体检测

```
1. Capture user selfie
2. POST /v3/passive-liveness/ → {"user_image": selfie}
3. If "Approved" → user is real, proceed
   If "Declined" → check warnings:
     - NO_FACE_DETECTED → ask user to retake with face clearly visible
     - LOW_FACE_QUALITY → ask for better lighting/positioning
     - LIVENESS_FACE_ATTACK → flag as potential fraud
```

### 活体检测 + 面部匹配（组合使用）

```
1. POST /v3/passive-liveness/ → verify user is real
2. If Approved → POST /v3/face-match/ → compare selfie to ID photo
3. Both Approved → identity verified
```

---

## 实用脚本

```bash
export DIDIT_API_KEY="your_api_key"

python scripts/check_liveness.py selfie.jpg
python scripts/check_liveness.py selfie.jpg --threshold 80
```