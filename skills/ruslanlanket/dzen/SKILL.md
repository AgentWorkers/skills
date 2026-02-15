---
name: dzen
description: 将文章和帖子发布到 Dzen.ru（Yandex Zen）平台。支持上传文本、图片和视频。需要登录用户浏览器会话产生的会话cookie以及CSRF令牌。
---

# Dzen 发布器

该技能允许您通过模拟浏览器的方式，以编程方式将内容发布到 Dzen.ru 上。

## 设置

Dzen 并未提供用于发布的公共 API。此技能会使用您当前的浏览器会话。

### 1. 获取认证信息

1. 在浏览器中登录 [dzen.ru](https://dzen.ru)。
2. 打开开发者工具（F12）中的 **网络** 标签页。
3. 转到 [dzen.ru/profile/editor](https://dzen.ru/profile/editor)。
4. 找到任何发送到 `dzen.ru` 的请求（例如 `entry`、`list` 或主页面）。
5. 在 **请求头** 标签页中：
    *   找到 `Cookie` 头部，并复制其值。
    *   找到 `x-csrf-token` 头部，并复制其值。

### 2. 创建配置文件

在工作区中创建一个名为 `dzen_config.json` 的文件，内容如下：

```json
{
  "cookies": {
    "SESSION_ID": "your_session_id_from_cookies",
    "zen_sso_checked": "...",
    "...": "..."
  },
  "csrf_token": "your_csrf_token"
}
```

## 使用方法

### 发布帖子

使用 `publish.py` 脚本来创建帖子。

```bash
python3 scripts/publish.py --title "My Title" --text "My Content" --media image.jpg video.mp4 --config dzen_config.json
```

### 支持的媒体格式

- **图片**：`.jpg`、`.jpeg`、`.png`、`.webp`、`.gif`。
- **视频**：`.mp4`、`.mov`、`.avi`、`.mkv`。

媒体文件会在最终发布前自动上传。

## 提示

- **会话过期**：如果发布失败并显示 403 错误，可能是您的 Cookie 或 CSRF 令牌已过期。请从浏览器中刷新它们。
- **CSRF 令牌**：确保 `X-Csrf-Token` 与配置文件中的值一致。所有 POST 请求都必须使用此令牌。