---
name: ytmusic-librarian
description: 通过 ytmusicapi 管理 YouTube Music 的音乐库、播放列表以及发现功能。
---

# YTMusic Librarian

该技能使用 `ytmusicapi` Python 库与 YouTube Music 进行交互。

## 先决条件

- Python 3.x
- `ytmusicapi` 包：`pip install ytmusicapi`
- 技能文件夹中包含身份验证文件（`oauth.json` 或 `browser.json`）。

## 设置说明

1. **安装库：**
   ```bash
   pip install ytmusicapi
   ```

2. **生成身份验证信息（“cURL 请求”）：**
   - 打开 **Microsoft Edge** 并访问 [music.youtube.com](https://music.youtube.com)（确保已登录）。
   - 按下 `F12` 打开开发者工具，切换到 **Network** （网络）选项卡。
   - 点击页面上的 **个人资料图标 -> 图书馆**。
   - 在网络请求列表中查找名为 `browse` 的请求。
   - **右键点击** `browse` 请求 -> **复制**，然后选择 **复制为 cURL（bash）**。
   - 将生成的 cURL 命令粘贴到技能文件夹中的 `headers.txt` 文件中。
   - 运行以下 Python 代码片段以生成 `browser.json` 文件：
     ```python
     from ytmusicapi.auth.browser import setup_browser
     with open('headers.txt', 'r') as f:
         setup_browser('browser.json', f.read())
     ```
   - 确保 `browser.json` 文件位于技能文件夹中。

3. **验证：**
   ```bash
   python -c "from ytmusicapi import YTMusic; yt = YTMusic('browser.json'); print(yt.get_library_songs(limit=1))"
   ```

## 工作流程

### 图书馆管理
- 列出歌曲/专辑：`yt.get_library_songs()`、`yt.get_library_albums()`
- 添加/删除歌曲：`yt.rate_song(videoId, 'LIKE')`、`yt.edit_song_library_status(feedbackToken)`

### 播放列表管理
- 创建播放列表：`yt.create_playlist(title, description)`
- 添加曲目：`yt.add_playlist_items(playlistId, [videoIds])`
- 删除曲目：`yt.remove_playlist_items(playlistId, [videoIds])`

### 元数据与发现
- 获取歌词：`yt.get_lyrics(browseId)`
- 获取相关内容：`yt.get_watch_playlist(videoId)` -> `related`