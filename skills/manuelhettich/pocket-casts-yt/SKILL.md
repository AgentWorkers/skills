---
name: pocket-casts
description: 下载 YouTube 视频，并将其上传到 Pocket Casts 以供离线观看。仅限用于您拥有或有权使用的个人内容。
version: 1.0.0
author: emmanuelem
---

# Pocket Casts YouTube 上传工具

该工具可用于下载 YouTube 视频，并将其上传到 Pocket Casts 以供离线观看。

## 使用方法

```bash
~/skills/pocket-casts/scripts/upload.sh "YOUTUBE_URL"
```

或者使用自定义标题：
```bash
~/skills/pocket-casts/scripts/upload.sh "YOUTUBE_URL" "Custom Title"
```

## 先决条件

### 必需软件：
- **yt-dlp**：YouTube 下载工具（通过 uv 使用：`uvx yt-dlp`)
- **ffmpeg**：视频处理工具（通过 `apt install ffmpeg` 安装）
- **curl**：HTTP 请求工具（通常已预装）
- **jq**：JSON 解析工具（通过 `apt install jq` 安装）

### 推荐软件：
- **deno**：用于处理 yt-dlp 相关任务的 JavaScript 运行时环境：
  ```bash
  curl -fsSL https://deno.land/install.sh | sh
  ```
  将其添加到系统路径中：`export PATH="$HOME/.deno/bin:$PATH"`

## 设置步骤

1. **创建凭据目录：**
   ```bash
   mkdir -p ~/.clawdbot/credentials/pocket-casts
   chmod 700 ~/.clawdbot/credentials/pocket-casts
   ```

2. **获取 Pocket Casts 的刷新令牌：**
   在登录 pocketcasts.com 后，通过浏览器开发者工具获取刷新令牌，然后按照以下步骤操作：
   ```bash
   cat > ~/.clawdbot/credentials/pocket-casts/config.json << 'EOF'
   {
     "refreshToken": "YOUR_REFRESH_TOKEN_HERE"
   }
   EOF
   chmod 600 ~/.clawdbot/credentials/pocket-casts/config.json
   ```

   刷新令牌的有效期约为 1 年。系统会自动获取访问令牌。

3. **添加 YouTube 的 Cookie（大多数视频都需要）：**
   YouTube 的机器人检测机制需要来自已登录浏览器会话的 Cookie。
   - 安装 “Get cookies.txt LOCALLY” 浏览器扩展程序（或类似工具）
   - 登录后访问 youtube.com
   - 通过扩展程序导出 Cookie
   - 将导出的 Cookie 保存到 `~/.clawdbot/credentials/pocket-casts/cookies.txt` 文件中
   ```bash
   chmod 600 ~/.clawdbot/credentials/pocket-casts/cookies.txt
   ```

## 工作原理

1. 使用 `yt-dlp --remux-video mp4` 命令下载视频。
2. 使用存储的刷新令牌更新 Pocket Casts 的访问令牌。
3. 从 Pocket Casts API 获取预签名的上传 URL。
4. 通过预签名的 URL 将文件上传到 S3 云存储服务。
5. 删除本地下载的视频文件。

## 环境变量

- `CLAWDBOT_CREDENTIALS`：用于指定凭据目录（默认值为 `~/.clawdbot/credentials`）

## 注意事项

- 下载的视频会显示在 Pocket Casts 的 “Files” 标签页中。
- 视频可以在 iOS、Android 和 Web 平台上直接播放。
- 文件的最大大小取决于您的 Pocket Casts 订阅套餐（Plus 订阅通常支持最大 2GB 的文件）。
- 如果 YouTube 阻止请求，可能需要重新获取 Cookie。

## ⚠️ 法律声明

**本工具仅用于个人、合法用途。**

- **YouTube 服务条款** 明确禁止通过非官方途径下载视频。根据您所在地区的法律法规及使用目的，下载视频可能违反 YouTube 的服务条款。
- **Pocket Casts 的使用条款** 要求您拥有上传到文件库中的所有媒体的所有权或使用权限。
- **版权法因国家/地区而异。未经许可下载和存储受版权保护的内容可能属于违法行为。**

使用本工具时，您需自行确保您的使用行为符合所有适用的服务条款和法律法规。作者对任何不当使用行为概不负责。

**推荐用途：** 个人录制内容、遵循 Creative Commons 许可协议的内容、您自己制作的内容，或创作者明确允许下载的内容。