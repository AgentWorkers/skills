---
name: bluesky
description: "Bluesky/AT 协议用于实现与 Bluesky 社交网络的认证交互功能，支持以下操作：发布帖子、回复评论、点赞、转发帖子、引用帖子、添加书签以及上传媒体文件。"
metadata:
  {
    "openclaw": {
      "emoji": "🦋",
      "env": {
        "BSKY_PDS": "https://bsky.social",
        "BSKY_HANDLE": "<required>",
        "BSKY_APP_PASSWORD": "<required>"
      },
      "secrets": ["BSKY_APP_PASSWORD"],
      "install": [
        {
          "id": "python-atproto",
          "kind": "pip",
          "package": "atproto",
          "label": "Install AT Protocol Python SDK"
        }
      ]
    }
  }
---
# Bluesky 技能

这是一种高级的 Bluesky/AT 协议编排技能，允许用户与 Bluesky 社交网络进行身份验证后的交互，包括对富文本的处理、媒体上传以及线程管理等功能。

## 来源与出处
- **GitHub 仓库**：[https://github.com/Heather-Herbert/openclaw-bluesky](https://github.com/Heather-Herbert/openclaw-bluesky)
- **标准**：遵循 OpenClaw AT 协议的实现规范。

## 配置与身份验证
为了安全运行，需要设置以下环境变量：
- `BSKY_PDS`：PDS 的 URL（默认值：`https://bsky.social`）。
- `BSKY_HANDLE`：您的完整 Bluesky 用户名（例如：`user.bsky.social`）。
- `BSKY_APP_PASSWORD`：通过 Bluesky 设置生成的唯一 **应用密码**。

### 设置步骤
1. **依赖项**：确保已安装 `atproto` Python 库：`pip install atproto`。
2. **生成应用密码**：在 Bluesky 客户端中进入“设置” > “高级” > “应用密码”。
3. **环境变量**：配置您的 shell 或 `OPENCLAW_ENV`，以包含上述变量。请勿将您的主账户密码存储在此处。

## 功能
- `post(text, { reply_to, embed, facets })`：创建新帖子。进行线程操作时需要 `root` 和 `parent` 参考（`uri`+`cid`）。
- `like(uri, cid)`：点赞内容。
- `repost(uri, cid)`：重新发布内容。
- `quote(text, uri, cid)`：通过嵌入内容的强引用（Strong Reference）来引用帖子。
- `bookmark(uri, cid)`：进行私有书签标记（仅适用于应用视图）。
- `upload_blob(bytes, mimetype)`：上传媒体文件（图片大小限制为 1MB），然后才能进行嵌入。

## 实现细节
- **处理用户名与 DIDs**：在执行写入操作之前，始终使用 `resolveHandle` API 将用户名转换为 DIDs。
- **富文本处理**：使用 `TextEncoder` 确保 `byteStart` 和 `byteEnd` 的准确性，避免依赖 UTF-16 字符索引。
- **索引管理**：在交互（点赞/重新发布/引用）之前，务必获取最新的帖子 `cid`，以确保强引用的有效性。

## 官方文档
- [AT 协议文档](https://atproto.com/)
- [Bluesky 开发者文档](https://docs.bsky.app/)

## 作者
- [Jennifer Strategist](https://bsky.app/profile/jenniferstrategist.bsky.social)