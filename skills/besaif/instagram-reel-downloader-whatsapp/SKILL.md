---
name: instagram-reel-downloader-whatsapp
description: 通过 sssinstagram.com 下载 Instagram 的 Reel（短视频集），并将其转换为适合在 WhatsApp 上使用的视频文件。当提供了 Reel 的 URL，但 yt-dlp 被禁用或不被推荐使用时，可以使用此方法。
---
# 通过 sssinstagram 下载 Instagram Reel 视频

## 要求

- 确保系统安装了 Node.js 18 及更高版本。
- 运行时环境中必须安装了 `playwright-core`。
- 需要有一个兼容 Chromium 的浏览器二进制文件，可以通过以下方式获取：
  - 使用环境变量 `BROWSER_EXECUTABLE_PATH` 指定浏览器路径（推荐）；
  - 或者使用系统默认的 `/usr/bin/brave-browser`。

## 环境变量

- `OPENCLAW_WORKSPACE`（可选）：用于指定输出文件的工作空间路径。
- `REEL_DOWNLOAD_DIR`（可选）：用于指定视频下载的目录。
- `BROWSER_EXECUTABLE_PATH`（可选）：用于指定浏览器二进制文件的路径。

### 功能步骤

1. 验证输入的 Instagram 链接：
   - 仅接受格式为 `https://www.instagram.com/reel/...`（或 `/reels/...`）的链接。

2. 运行下载脚本：
   - 执行命令：`node scripts/download_via_sss.mjs "<instagram-url>"`
   - 如果下载成功，脚本会输出视频文件的绝对路径（`MEDIA_PATH`）。

3. 通过 WhatsApp 将视频文件发送给用户：
   - 使用 WhatsApp 的 `message` 功能，设置 `action=send` 并将 `media` 参数设置为下载到的视频文件路径（`MEDIA_PATH`）。
   - 在消息中添加简短的说明文字，例如：“下载完成 🐾”。

4. 如果网站阻止了自动化操作：
   - 等待片刻后重新尝试下载。
   - 如果仍然无法下载，应友好地提示用户提供另一个有效的链接。

## 注意事项：
- 如果设置了 `BROWSER_EXECUTABLE_PATH`，则会使用该路径指定的浏览器；否则默认使用 `/usr/bin/brave-browser`。
- 视频文件会被保存到 `REEL_DOWNLOAD_DIR` 中；如果未设置该目录，则会保存在 `<workspace>/downloads`（取决于 `OPENCLAW_WORKSPACE` 的值或当前工作目录）。
- 该脚本使用无头模式（headless mode）运行 Playwright（`playwright-core`）。
- 提供了可选的清理脚本 `bash scripts/cleanup_reels.sh`，用于在指定时间后自动删除下载的文件（默认为 30 分钟）。
- 为保护用户隐私，下载完成后会立即删除相关链接，不会保留过久的文件记录。