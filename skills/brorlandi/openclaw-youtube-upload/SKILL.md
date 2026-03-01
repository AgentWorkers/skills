---
name: youtube-upload
description: "使用官方的 YouTube Data API v3 和 OAuth 2.0 将视频上传到 YouTube。当用户请求将视频上传到 YouTube 时，可以使用此功能。该功能支持设置视频标题、描述以及隐私设置（公开、私有、未公开），并且支持分块上传大文件。需要一个 Google Cloud 的 `client_secret.json` 文件。"
metadata:
  openclaw:
    emoji: "📺"
    requires:
      bins: ["python3", "pip3"]
---
# YouTube 上传功能

此功能允许您通过官方 API 安全地将视频上传到 YouTube，从而避免使用不稳定的浏览器自动化工具。

## 先决条件

1. 必须安装 Google API Python Client 和 OAuth 库：
   ```bash
   pip3 install google-api-python-client google-auth-oauthlib google-auth-httplib2
   ```
2. 需要一个 `client_secret.json` 文件。用户必须从 Google Cloud Console 中为 YouTube Data API v3 启用 OAuth 2.0 客户端 ID（桌面应用）。

## 使用方法

使用提供的 Python 脚本上传视频：

```bash
python3 scripts/upload.py \
  --file "/path/to/video.mp4" \
  --title "My Video Title" \
  --description "My Video Description" \
  --privacy "unlisted" \
  --secrets "/path/to/client_secret.json"
```

### 首次运行（身份验证）
在首次运行时，脚本会输出一个 URL 或在浏览器中打开一个窗口，让用户进行身份验证并授予对其 YouTube 账户的访问权限。请用户完成登录流程。一旦获得批准，系统会在本地生成一个 `token.pickle` 文件，之后的上传操作将自动进行，无需再次输入密码。

## 故障排除

- **令牌过期/被撤销：** 如果令牌失效，请删除 `token.pickle` 文件并重新运行脚本以重新进行身份验证。
- **超出上传配额：** YouTube API 有每日上传配额限制。如果超出配额，用户必须等待配额重置。