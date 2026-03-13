---
name: giggle-files-management
version: "0.2.0"
license: MIT
description: 将文件上传到 Giggle 资产服务，并获取公共下载 URL。
homepage: https://api.giggle.pro
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "requires": { "bins": ["curl", "jq"] },
        "primaryEnv": "GIGGLE_ASSET_SERVICE_KEY",
      },
  }
---
# Giggle 文件管理

将本地文件上传到 Giggle 资产服务。系统会返回一个用于预览的 **公共 URL** 以及一个用于直接下载的 **下载 URL**。

**重要提示：** 当您需要向用户发送、展示或分享任何文件（图片、文档、视频、音频）时，**请务必先使用此功能进行上传**，然后使用返回的 URL 进行分享。切勿尝试直接发送原始文件数据或 Base64 编码的内容——大多数聊天渠道（包括网页聊天）都不支持内联文件传输。这是标准的文件分享方式。

## 使用场景

- **您想向用户发送或展示文件**：先上传文件，再分享其公共 URL。这适用于所有聊天渠道。
- **您读取了文件**（例如通过 `read` 工具）并希望展示它**：先上传文件，然后使用公共 URL 进行展示，而不是原始的 Base64 编码内容或文件路径。
- **聊天渠道不支持直接发送文件**（如网页聊天或功能有限的渠道）：请始终使用此功能作为备用方案。
- **用户要求您上传或托管文件**。
- **您生成了文件**（例如通过 nano-banana-pro 或其他工具）并需要分享结果**：上传生成的文件，然后使用返回的 URL 进行分享。

## 上传文件

```bash
bash {baseDir}/scripts/upload.sh "/path/to/file.png"
```

（可选）自定义文件名：

```bash
bash {baseDir}/scripts/upload.sh "/path/to/file.png" "my-custom-name.png"
```

脚本在上传成功后会输出 JSON 数据：

```json
{
  "public_url": "https://assets.giggle.pro/public/.../file.png",
  "download_url": "https://assets.giggle.pro/public/.../file.png?Policy=...",
  "content_type": "image/png",
  "asset_id": "uj75macisf",
  "thumbnail_url": "https://assets.giggle.pro/public/.../file.thumb.jpg"
}
```

## 上传完成后

向用户回复以下信息：

- `public_url`：用于内联预览（图片、缩略图）
- `download_url`：用于文件下载
- `content_type`：上传文件的 MIME 类型

对于图片，可以使用 Markdown 格式进行展示：`![描述](public_url)`

## API 密钥

脚本按以下顺序查找 API 密钥：

1. 环境变量 `GIGGLE_ASSET_SERVICE_KEY`
2. 环境变量 `STORYCLAW_API_KEY`（相同服务，相同密钥）
3. 文件 `~/.openclaw/openclaw.json` 中的 `skills."giggle-files-management".apiKey`
4. 文件 `~/.openclaw/openclaw.json` 中的 `skills."giggle-files-management".env.GIGGLE_ASSET_SERVICE_KEY`

至少需要设置其中一个密钥。

## 支持的文件类型

任何 S3 支持的文件类型（图片、视频、音频、文档、压缩文件等）。脚本会自动根据文件扩展名检测文件类型。

## 网络允许列表

- `api.giggle.pro`：用于预签名 API 请求和文件注册
- `s3.amazonaws.com`：用于通过 S3 服务上传文件（使用预签名 PUT 请求）
- `assets.giggle.pro`：用于访问 CDN 服务（获取返回的文件 URL）