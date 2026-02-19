---
name: whatsapp-local-router
description: 将传入的 WhatsApp 内容路由到本地的 HTTP 端点，并将端点的 JSON 响应直接返回给用户。当 WhatsApp 消息包含纯文本或随机符号时，应将其发送到 `http://localhost:8080/process`；当 WhatsApp 消息包含 QR 图像时，应将其发送到 `http://localhost:8080/decode-qr`。
---
# WhatsApp 本地路由器

## 概述

该本地路由器支持两种 WhatsApp 输入类型，并将后端响应直接反馈给用户：
- 文本输入 → `/process`
- QR 图像输入 → `/decode-qr`

除非用户特别要求提供额外的格式说明，否则始终以原始格式将后端响应体发送给用户。

## 工作流程

1. 确认消息确实来自 WhatsApp 环境。
2. 选择处理路径：
   - 如果接收到的消息包含图像附件路径（预期为 QR 图像），则调用 `/decode-qr` 路由进行处理。
   - 否则，将用户输入的文本视为普通字符串，并调用 `/process` 路由进行处理。
3. 使用 `scripts/route_whatsapp.sh` 脚本执行相应的处理逻辑。
4. 将脚本的输出结果（stdout）直接发送给用户。
5. 如果后端返回错误或无效的 JSON 数据，返回简短的错误信息，并附上原始的响应内容。

## 命令

在 workspace 的根目录下运行以下命令：

```bash
# Text -> /process
bash skills/whatsapp-local-router/scripts/route_whatsapp.sh process "<any text>"

# Image -> /decode-qr
bash skills/whatsapp-local-router/scripts/route_whatsapp.sh decode "/path/to/image.png"
```

## 路由规则

- 保持文本内容的原样，不要对其进行清洗、截断或重新解释。
- 使用 `image` 作为多部分数据（multipart data）字段名称来处理 QR 图像的上传。
- 请求超时时间为 20 秒。
- 如果同时存在文本和图像，优先处理图像解码；除非用户明确要求处理文本。
- 响应内容应简洁明了：直接将后端返回的 JSON 数据发送给用户。