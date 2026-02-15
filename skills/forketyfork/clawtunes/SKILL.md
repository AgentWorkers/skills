---
name: managing-apple-music
description: 在 macOS 上，可以通过 `clawtunes` CLI 来控制 Apple Music：播放歌曲/专辑/播放列表、控制播放功能、调节音量、随机播放、重复播放、搜索歌曲、查询音乐目录、使用 AirPlay，以及管理播放列表。当用户需要播放音乐、搜索歌曲、控制音频播放或管理 Apple Music 设置时，可以使用该工具。
homepage: https://github.com/forketyfork/clawtunes
metadata: {"clawdbot":{"emoji":"🎵","os":["darwin"],"requires":{"bins":["clawtunes"]},"install":[{"id":"brew","kind":"brew","tap":"forketyfork/tap","formula":"clawtunes","bins":["clawtunes"],"label":"Install clawtunes via Homebrew"}]}}
---

# Apple Music 命令行工具（CLI）

您可以使用 `clawtunes` 从终端控制 Apple Music。该工具支持搜索和播放音乐、调整音量、管理播放列表、设置随机播放/重复模式、浏览 Apple Music 目录以及连接 AirPlay 设备。

## 设置

- **通过 Homebrew 安装：**  
  ```
  brew tap forketyfork/tap && brew install clawtunes
  ```
- **通过 pip 安装：**  
  ```
  pip install clawtunes
  ```
- **仅适用于 macOS；需要安装 Apple Music 应用程序。**

## 播放音乐

- **播放单首歌曲：**  
  ```
  clawtunes play song "歌曲名称"
  ```
- **播放整张专辑：**  
  ```
  clawtunes play album "专辑名称"
  ```
- **播放播放列表：**  
  ```
  clawtunes play playlist "播放列表名称"
  ```
- **使用 `--non-interactive`（`-N`）标志以避免交互式提示：**  
  ```
  clawtunes -N play song "歌曲名称"
  ```
- **如果命令以代码 1 结束且返回多个匹配结果，请使用更具体的歌曲/专辑/播放列表名称重新尝试。**  
- **如果仍然有多个匹配结果，可以使用 `--first`（`-1`）标志自动选择第一个结果：**  
  ```
  clawtunes -1 play song "歌曲名称"
  ```

## 播放控制

- **暂停：**  
  ```
  clawtunes pause
  ```
- **继续播放：**  
  ```
  clawtunes resume
  ```
- **下一首曲目：**  
  ```
  clawtunes next
  ```
- **上一首曲目：**  
  ```
  clawtunes prev
  ```
- **显示当前正在播放的歌曲：**  
  ```
  clawtunes status
  ```

## 调整音量

- **显示当前音量：**  
  ```
  clawtunes volume
  ```
- **设置音量：**  
  ```
  clawtunes volume 50
  ```
- **增加/减少音量：**  
  ```
  clawtunes volume +10
  clawtunes volume -10
  ```
- **静音/取消静音：**  
  ```
  clawtunes mute
  clawtunes unmute
  ```

## 随机播放和重复模式

- **启用/禁用随机播放：**  
  ```
  clawtunes shuffle on
  clawtunes shuffle off
  ```
- **设置重复模式：**  
  ```
  clawtunes repeat off
  clawtunes repeat all
  clawtunes repeat one
  ```

## 搜索

- **搜索歌曲和专辑：**  
  ```
  clawtunes search "查询"
  ```
- **包含播放列表：**  
  ```
  clawtunes search "查询" -p
  ```
- **仅搜索歌曲：**  
  ```
  clawtunes search "查询" --no-albums
  ```
- **限制搜索结果数量：**  
  ```
  clawtunes search "查询" -n 20
  ```

## 喜欢/不喜欢

- **标记当前歌曲为“喜欢”：**  
  ```
  clawtunes love
  ```
- **标记当前歌曲为“不喜欢”：**  
  ```
  clawtunes dislike
  ```

## 播放列表

- **列出所有播放列表：**  
  ```
  clawtunes playlists
  ```
- **创建播放列表：**  
  ```
  clawtunes playlist create "旅行路线"
  ```
- **将歌曲添加到播放列表：**  
  ```
  clawtunes playlist add "旅行路线" "Kickstart My Heart"
  ```
- **从播放列表中删除歌曲：**  
  ```
  clawtunes playlist remove "旅行路线" "Kickstart My Heart"
  ```

## AirPlay

- **列出可用设备：**  
  ```
  clawtunes airplay
  ```
- **选择设备：**  
  ```
  clawtunes airplay "设备名称"
  ```
- **取消选择设备：**  
  ```
  clawtunes airplay "设备名称" --off
  ```

## Apple Music 目录

- **搜索流媒体目录：**  
  ```
  clawtunes catalog search "Bowie Heroes"
  ```
- **限制搜索结果数量：**  
  ```
  clawtunes catalog search "Bowie Heroes" -n 5
  ```
- **注意：** 目录搜索仅用于浏览。若要将歌曲添加到播放列表中，这些歌曲必须先存在于您的 Apple Music 库中。请使用 Apple Music 应用程序将目录中的歌曲添加到您的库中，然后再使用 `clawtunes` 进行管理。

## 注意事项

- **仅适用于 macOS（通过 AppleScript 与 Apple Music 交互）。**  
- **如果系统请求自动化权限，请在“系统设置 > 隐私与安全 > 自动化”中授予相应权限。**