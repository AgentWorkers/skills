---
name: didit-biometric-age-estimation
description: 通过 Didit 独立 API 从面部图像中估算一个人的年龄。适用于实现年龄限制功能（例如判断某人是否超过 18 岁或 21 岁）、进行合规性年龄验证，或检测未成年用户。该服务包含被动式活体检测功能，支持配置不同的阈值、在必要时自动切换到身份验证方式，并且针对不同国家/地区有不同的使用限制。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🎂"
    homepage: https://docs.didit.me
---
# Didit年龄估算API

## 概述

该API利用深度学习技术从面部图像中估算用户的年龄，并同时进行被动式活体检测以防止欺诈行为。

**主要限制：**
- 支持的文件格式：JPEG、PNG、WebP、TIFF
- 文件最大大小：5MB
- 图像中必须包含一张清晰可见的脸部
- 估算准确率：整体MAE误差为±3.5岁；18岁以下用户的误差为±1.5岁

**功能：**
- 提供年龄估算及置信度评分
- 性别估算
- 被动式活体检测
- 可配置的年龄阈值
- 根据国家设置年龄限制
- 自适应模式（在边缘情况下可触发身份验证）

**活体检测方法（工作流程模式）：**

| 方法 | 安全性 | 适用场景 |
|---|---|---|
| `ACTIVE_3D`（动作+闪光） | 最高安全性 | 银行业、政府机构、医疗行业 |
| `FLASHING`（3D闪光） | 高安全性 | 金融服务、身份验证 |
| `PASSIVE`（单帧CNN） | 标准安全性 | 低复杂度的消费类应用 |

**API参考文档：** https://docs.didit.me/standalone-apis/age-estimation
**功能指南：** https://docs.didit.me/core-technology/age-estimation/overview

---

## 认证

所有请求都需要包含`x-api-key`头部信息。您可以从[Didit业务控制台](https://business.didit.me)的API & Webhooks部分获取API密钥，或通过程序化注册方式获取（详见下文）。

## 如何开始（尚未注册账户？）

如果您没有Didit API密钥，可以通过以下两个API调用进行注册：
1. **注册：** `POST https://apx.didit.me/auth/v2/programmatic/register/`，参数为`{"email": "you@gmail.com", "password": "MyStr0ng!Pass"}`
2. **接收6位数的OTP验证码**  
3. **验证：** `POST https://apx.didit.me/auth/v2/programmatic/verify-email/`，参数为`{"email": "you@gmail.com", "code": "A3K9F2"}`，响应中会包含`api_key`

**添加信用额度：** `GET /v3/billing/balance/` 查看余额；`POST /v3/billing/top-up/`，参数为`{"amount_in_dollars": 50}`，以获取Stripe支付链接。

有关平台管理的完整信息（工作流程、会话、用户、计费等），请参阅**didit-verification-management**文档。

---

## 端点

```
POST https://verification.didit.me/v3/age-estimation/
```

### 头部信息

| 头部信息 | 值 | 是否必需 |
|---|---|---|
| `x-api-key` | 您的API密钥 | 是 |
| `Content-Type` | `multipart/form-data` | 是 |

### 请求参数（multipart/form-data）

| 参数 | 类型 | 是否必需 | 默认值 | 说明 |
|---|---|---|---|
| `user_image` | 文件 | 是 | — | 面部图像（格式：JPEG/PNG/WebP/TIFF，最大5MB） |
| `rotate_image` | 布尔值 | 否 | `false` | 对非正立的面部图像尝试旋转0/90/180/270度 |
| `save_api_request` | 布尔值 | 否 | `true` | 是否将请求保存在业务控制台以供手动审核 |
| `vendor_data` | 字符串 | 否 | — | 用于会话跟踪的标识符 |

### 示例

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/age-estimation/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={"user_image": ("selfie.jpg", open("selfie.jpg", "rb"), "image/jpeg")},
    data={"vendor_data": "user-123"},
)
print(response.json())
```

```typescript
const formData = new FormData();
formData.append("user_image", selfieFile);

const response = await fetch("https://verification.didit.me/v3/age-estimation/", {
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
    "score": 89.92,
    "age_estimation": 24.3,
    "reference_image": "https://example.com/reference.jpg",
    "video_url": null,
    "warnings": []
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### 状态码及其含义及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Approved"` | 年龄超过阈值且活体检测通过 | 继续执行后续流程 |
| `"Declined"` | 年龄低于最低要求或活体检测失败 | 查看`warnings`字段获取详细原因 |
| `"In Review"` | 边缘情况，需要人工审核 | 触发身份验证或手动审核 |

### 错误响应

| 错误代码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求无效 | 检查文件格式、大小和参数 |
| `401` | API密钥无效 | 确认`x-api-key`头部信息是否正确 |
| `403` | 信用额度不足 | 在business.didit.me网站上充值 |

---

## 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `status` | 字符串 | `"Approved"`, `"Declined"`, `"In Review"`, `"Not Finished"` |
| `method` | 字符串 | `"ACTIVE_3D"`, `"FLASHING"`, 或 `"PASSIVE"` |
| `score` | 浮点数 | 0-100的活体检测置信度评分 |
| `age_estimation` | 浮点数 | 估算的年龄（单位：岁，例如`24.3`）；若无面部信息则返回`null` |
| `reference_image` | 字符串 | 临时URL（60分钟后失效） |
| `video_url` | 字符串 | 活体检测视频的临时URL；被动检测时返回`null` |
| `warnings` | 数组 | `{"risk", "log_type", "short_description", "long_description}"` |

### 不同年龄段的估算准确率

| 年龄段 | MAE（误差范围，单位：岁） | 置信度 |
|---|---|---|
| 18岁以下 | 1.5 | 高 |
| 18-25岁 | 2.8 | 高 |
| 26-40岁 | 3.2 | 高 |
| 41-60岁 | 3.9 | 中等偏高 |
| 60岁以上 | 4.5 | 中等 |

---

## 警告标签

### 自动拒绝情况

| 标签 | 说明 |
|---|---|
| `NO_FACE_DETECTED` | 图像中未检测到面部 |
| `LIVENESS_FACE_ATTACK` | 检测到欺诈尝试 |
| `FACE_IN_BLOCKLIST` | 面部与黑名单中的信息匹配 |

### 可配置的拒绝/审核/批准规则

| 标签 | 说明 |
|---|---|
| `AGE_BELOW_MINIMUM` | 估算年龄低于配置的最低阈值 |
| `AGE_NOT_DETECTED` | 由于图像质量或光线原因无法估算年龄 |
| `LOW_LIVENESS_SCORE` | 活体检测得分低于阈值 |
| `POSSIBLE_DUPLICATED_FACE` | 与之前验证过的面部高度相似 |

警告的严重程度：`error`（→ 自动拒绝），`warning`（→ 进入审核流程），`information`（→ 无影响）。

---

## 常见工作流程

### 基本年龄验证

```
1. Capture user selfie
2. POST /v3/age-estimation/ → {"user_image": selfie}
3. Check liveness.age_estimation >= your_minimum_age
4. If "Approved" → user meets age requirement
   If "Declined" → check warnings for AGE_BELOW_MINIMUM or liveness failure
```

### 自适应年龄估算（工作流程模式）

使用`workflow_type: "adaptive_age_verification"`，在年龄判断为边缘情况时自动触发身份验证。

```
1. POST /v3/workflows/ → {"workflow_type": "adaptive_age_verification", "is_liveness_enabled": true, "is_age_restrictions_enabled": true}
2. POST /v3/session/ → create session with the workflow_id from step 1
3. User takes selfie → system estimates age
4. Clear pass (well above threshold) → Approved instantly
   Clear fail (well below threshold) → Declined
   Borderline case → automatic ID verification fallback
5. If ID fallback triggered: per-country age restrictions apply
```

### 国家特定的年龄限制

您可以在控制台为每个国家配置年龄限制：

| 国家 | 最低年龄 | 特殊规定 |
|---|---|---|
| 美国 | 18岁 | 密西西比州：21岁，阿拉巴马州：19岁 |
| 韩国 | 19岁 | — |
| 英国 | 18岁 | — |
| 阿联酋 | 21岁 | — |

> 可在控制台使用“Apply age of majority”按钮自动设置默认值。

---

## 实用脚本

**estimate_age.py**：通过命令行从面部图像估算年龄。

```bash
# Requires: pip install requests
export DIDIT_API_KEY="your_api_key"
python scripts/estimate_age.py selfie.jpg
python scripts/estimate_age.py photo.png --threshold 21 --vendor-data user-123
```