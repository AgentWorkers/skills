---
name: qrdex
description: 使用 QRdex.io 的 REST API 来创建、管理和跟踪二维码。适用于需要生成二维码、通过二维码缩短 URL、生成用于 WiFi 连接的二维码、生成用于电子邮件/短信/WhatsApp 的二维码、进行扫描追踪，或执行任何与 QRdex.io 相关的操作的场景。该 API 支持所有类型的二维码（URL、电子邮件、电话号码、短信、WhatsApp），并且允许自定义二维码的颜色和形状。
---

# QRdex

通过 QRdex.io 的 REST API 管理二维码。

## 设置

将 API 密钥设置为环境变量：

```bash
export QRDEX_API_KEY="your-api-key"
```

从以下地址获取密钥：QRdex.io → 团队设置 → API 部分。
API 访问需要 Growth 计划或更高级别的权限。

## 快速参考

基础 URL：`https://qrdex.io/api/v1`

所有请求都需要包含 `Authorization: Bearer $QRDEX_API_KEY` 和 `Content-Type: application/json`。

### 创建二维码

```bash
curl -X POST https://qrdex.io/api/v1/qr_codes \
  -H "Authorization: Bearer $QRDEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "qr_code": {
      "title": "My Website",
      "qr_type": "url",
      "url": "https://example.com"
    }
  }'
```

### 二维码类型及必填字段

| 类型 | 必填字段 |
|------|----------------|
| `url` | `url` |
| `email` | `email_address`（可选：`email_subject`, `message`） |
| `telephone` | `telephone_number` |
| `sms` | `telephone_number`（可选：`message`） |
| `whatsapp` | `telephone_number`（可选：`message`） |
| `wifi` | `wifi_ssid`（可选：`wifi_encryption`, `wifi_password`, `wifi_hidden`） |

### 常见可选字段

- `foreground_color` — 十六进制颜色（默认：`#000000`）
- `background_color` — 十六进制颜色（默认：`#FFFFFF`）
- `shape` — 二维码形状（默认：`rounded`）
- `track_scans` — 启用扫描跟踪（默认：`true`）

### 列出二维码

```bash
curl https://qrdex.io/api/v1/qr_codes \
  -H "Authorization: Bearer $QRDEX_API_KEY"
```

查询参数：`page`, `per_page`（最多 100 条），`qr_type`（筛选条件）。

### 获取 / 更新 / 删除二维码

```bash
# Get
curl https://qrdex.io/api/v1/qr_codes/:id -H "Authorization: Bearer $QRDEX_API_KEY"

# Update (partial — only send changed fields)
curl -X PATCH https://qrdex.io/api/v1/qr_codes/:id \
  -H "Authorization: Bearer $QRDEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"qr_code": {"title": "New Title"}}'

# Delete (soft-delete)
curl -X DELETE https://qrdex.io/api/v1/qr_codes/:id -H "Authorization: Bearer $QRDEX_API_KEY"
```

### 下载二维码图片（SVG 格式）

```bash
curl https://qrdex.io/api/v1/qr_codes/:id/image \
  -H "Authorization: Bearer $QRDEX_API_KEY" -o qr.svg
```

返回的文件格式为 `image/svg+xml`。可以直接使用任何二维码响应中的 `image_url` 字段来插入 `<img>` 标签中。

## 使用 Python 脚本

如需编程使用，请使用 `scripts/qrdex_api.py`：

```bash
# Set API key
export QRDEX_API_KEY="your-key"

# List QR codes
python scripts/qrdex_api.py list

# Create QR codes
python scripts/qrdex_api.py create --title "My Site" --type url --url "https://example.com"
python scripts/qrdex_api.py create --title "WiFi" --type wifi --ssid "Guest" --wifi-password "pass123"
python scripts/qrdex_api.py create --title "Email" --type email --email "hi@example.com"
python scripts/qrdex_api.py create --title "Chat" --type whatsapp --phone "+15551234567" --message "Hello!"

# Get details
python scripts/qrdex_api.py get 123

# Update
python scripts/qrdex_api.py update 123 --title "Updated Title" --fg-color "#FF0000"

# Delete
python scripts/qrdex_api.py delete 123

# Download image
python scripts/qrdex_api.py image 123 -o qr.svg
```

## 错误处理

- `401` — API 密钥无效或缺失
- `403` — 无权限
- `404` — 二维码未找到或属于其他团队
- `422` — 验证错误或达到计划使用限制
- `429` — 每个密钥的请求速率限制（每分钟 100 次）。请查看 `X-RateLimit-Remaining` 标头。

## API 参考

有关所有字段的详细描述和响应格式，请参阅 `references/API_REFERENCE.md`。