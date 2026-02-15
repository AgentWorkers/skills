---
name: pinterest
description: Pinterest API v5集成：支持创建和读取Pin（图片或视频），管理Pinterest板（boards），以及获取用户资料和数据分析。当用户需要自动化执行Pinterest相关操作或访问账户数据时，可使用此技能。
---

# Pinterest API v5 技能

本技能提供了用于操作 Pinterest API v5 的工具和说明。

## 快速入门

1. **创建应用**：按照 [references/setup_guide.md](references/setup_guide.md) 中的指南获取您的 `App ID` 和 `App Secret`。
2. **获取令牌**：运行授权脚本：
   ```bash
   python3 scripts/auth.py
   ```
   该脚本将打开浏览器，执行 OAuth 授权，并输出 `Access Token`。

## 核心功能

### 1. 图片钉钉（Pin）管理
- **创建图片钉钉**：`POST /v5/pins`
- **获取图片钉钉信息**：`GET /v5/pins/{pin_id}`
- **删除图片钉钉**：`DELETE /v5/pins/{pin_id}`

### 2. 图板（Board）管理
- **创建图片钉钉所在的板块**：`POST /v5/boards`
- **列出所有板块**：`GET /v5/boards`
- **获取板块上的图片钉钉**：`GET /v5/boards/{board_id}/pins`

### 3. 分析数据
- **账户分析**：`GET /v5/user_account/analytics`
- **图片钉钉分析**：`GET /v5/pins/{pin_id}/analytics`

有关端点和请求示例的详细信息，请参阅 [references/api_reference.md](references/api_reference.md)。

## 使用示例

### 创建图片钉钉
在创建图片钉钉时，必须指定 `board_id` 和 `media_source`。
请求体示例：
```json
{
  "title": "My Awesome Pin",
  "description": "Check this out!",
  "board_id": "123456789",
  "media_source": {
    "source_type": "image_url",
    "url": "https://example.com/image.jpg"
  }
}
```

### 获取所有板块
在创建图片钉钉之前，使用 `GET /v5/boards` 查找所需的 `board_id`。