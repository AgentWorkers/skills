---
name: dl
description: 从 YouTube、Bilibili 等平台下载视频/音乐
author: guoqiao
metadata: {"openclaw":{"always":false,"emoji":"🦞","homepage":"https://clawhub.ai/guoqiao/dl","os":["darwin","linux","win32"],"requires":{"bins":["uv"]}}}
triggers:
- "/dl <url>"
- "Download this video ..."
- "Download this music ..."
---

# 媒体下载器

该工具能够智能地从 YouTube、Bilibili、X 等平台下载视频和音乐文件，并将其保存到指定的本地文件夹中：

- **视频文件：** 保存到 `~/Movies/` 或 `~/Videos/` 文件夹中。
- **音乐文件：** 保存到 `~/Music/` 文件夹中。
- **播放列表文件：** 会被保存到一个子文件夹中（例如：`~/Music/<playlist_name>/`）。

该工具专为与本地媒体服务器（如 Universal Media Server、Jellyfin）配合使用而设计，以便用户可以通过电视或设备即时播放下载的媒体文件。

## 代理程序流程

当用户提供下载链接或请求下载媒体文件时，**必须严格遵循以下步骤：**

1. **确认请求：**  
   - 立即回复用户：“正在使用 `dl` 工具下载文件……”

2. **执行下载：**  
   - 运行下载脚本：  
     ```bash
     uv run --script ${baseDir}/dl.py "<url>"
     ```

3. **获取文件路径：**  
   - 脚本执行完成后，输出路径会显示在标准输出（stdout）中，该路径指向单个文件或包含播放列表文件的文件夹。

4. **通过 Telegram 上传文件（仅限 Telegram 用户）：**  
   - 如果用户使用的是 Telegram（通过上下文或会话信息判断），且文件为音频格式（mp3/m4a），则使用 `message` 工具将文件发送给用户：  
     ```json
     {
       "action": "send",
       "filePath": "<filepath>",
       "caption": "Here is your music."
     }
     ```

## 使用方法

将 `dl.py` 作为 uv 脚本运行：  
```bash
# save into default dirs ~/Music or ~/Movies or ~/Videos
uv run --script ${baseDir}/dl.py <url>

# specify your own output dir
uv run --script ${baseDir}/dl.py <url> -o <out_dir>
```  
脚本会输出文件的完整路径（单个文件或文件夹的路径）。

为了提高 `yt-dlp` 的下载稳定性，可以配置一个 cookies 文件，优先使用以下路径之一进行读取：  
- `${baseDir}/.cookies.txt`  
- `$DL_COOKIES_FILE`  
- `$COOKIES_FILE`  
- `~/.cookies.txt`

## 设置（用户端）

若在相同机器上安装了媒体服务器（如 Universal Media Server、Jellyfin），则该工具的使用效果会更加出色，因为下载的媒体文件可以直接在局域网内共享：

1. 安装支持 DLNA/UPnP 协议的媒体服务器（例如 Universal Media Server、miniDLNA、Jellyfin）。
2. 将 `~/Music` 和 `~/Movies`（或 `~/Videos`）文件夹共享出来。
3. 支持 DLNA/UPnP 协议的电视或设备（如 VLC）将能够自动识别并播放下载的媒体文件。

请参考 [示例脚本](https://github.com/guoqiao/skills/blob/main/dl/ums/ums_install.sh) 以在 Mac 上安装 Universal Media Server。