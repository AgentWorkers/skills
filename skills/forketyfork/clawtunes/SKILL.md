---
name: managing-apple-music
description: 在 macOS 上，可以通过 `clawtunes` CLI 来控制 Apple Music：播放歌曲/专辑/播放列表、控制播放进度、调节音量、随机播放、重复播放、搜索歌曲、查询音乐目录、使用 AirPlay 以及管理播放列表。当用户需要播放音乐、搜索歌曲、控制音频播放或管理 Apple Music 设置时，可以使用该工具。
homepage: https://github.com/forketyfork/clawtunes
metadata: {"clawdbot":{"emoji":"🎵","os":["darwin"],"requires":{"bins":["clawtunes"]},"install":[{"id":"brew","kind":"brew","tap":"forketyfork/tap","formula":"clawtunes","bins":["clawtunes"],"label":"Install clawtunes via Homebrew"}]}}
---
# Apple Music 命令行工具（CLI）

使用 `clawtunes` 从终端控制 Apple Music。你可以搜索和播放音乐、控制播放、调整音量、管理播放列表、设置随机播放/重复播放模式、浏览 Apple Music 的曲库，以及连接 AirPlay 设备。

## 设置

- 通过 Homebrew 安装：`brew install forketyfork/tap/clawtunes`
- 仅适用于 macOS；需要安装 Apple Music 应用程序。

## 播放音乐

- 播放一首歌曲：`clawtunes play "歌曲名称"`
- 播放一张专辑：`clawtunes play "专辑名称"`
- 播放一个播放列表：`clawtunes play "播放列表名称"`
- 始终使用 `--non-interactive`（`-N`）标志以避免交互式提示：`clawtunes -N play "歌曲名称"`
- 如果命令以代码 1 结束且返回多个匹配结果，请使用更具体的歌曲/专辑/播放列表名称重新尝试。
- 如果使用更具体的名称仍然返回多个匹配结果，可以使用 `--first`（`-1`）标志自动选择第一个结果：`clawtunes -1 play "歌曲名称"`。

## 播放控制

- 暂停：`clawtunes pause`
- 恢复播放：`clawtunes resume`
- 下一首曲目：`clawtunes next`
- 上一首曲目：`clawtunes prev`
- 显示当前正在播放的歌曲：`clawtunes status`

## 音量控制

- 查看音量：`clawtunes volume`
- 设置音量：`clawtunes volume 50`
- 调整音量：`clawtunes volume +10` 或 `clawtunes volume -10`
- 静音：`clawtunes mute`
- 取消静音：`clawtunes unmute`

## 随机播放和重复播放

- 启用/禁用随机播放：`clawtunes shuffle on` 或 `clawtunes shuffle off`
- 设置重复播放模式：`clawtunes repeat off`、`clawtunes repeat all` 或 `clawtunes repeat one`

## 搜索

- 搜索歌曲和专辑：`clawtunes search "查询内容"`
- 包含播放列表：`clawtunes search "查询内容" -p`
- 仅搜索歌曲：`clawtunes search "查询内容" --no-albums`
- 限制搜索结果数量：`clawtunes search "查询内容" -n 20`

## 喜欢/不喜欢

- 给当前歌曲添加“喜欢”标记：`clawtunes love`
- 给当前歌曲添加“不喜欢”标记：`clawtunes dislike`

## 播放列表

- 列出所有播放列表：`clawtunes playlists`
- 创建一个播放列表：`clawtunes playlist create "旅行路线"`
- 将歌曲添加到播放列表：`clawtunes playlist add "旅行路线" "Kickstart My Heart"`
- 从播放列表中删除歌曲：`clawtunes playlist remove "旅行路线" "Kickstart My Heart"`

## AirPlay

- 列出可连接的 AirPlay 设备：`clawtunes airplay`
- 选择设备：`clawtunes airplay "设备名称"`
- 取消选择设备：`clawtunes airplay "设备名称" --off`

## Apple Music 曲库

- 在流媒体曲库中搜索：`clawtunes catalog search "Bowie Heroes"`
- 限制搜索结果数量：`clawtunes catalog search "Bowie Heroes" -n 5`
- 注意：曲库搜索仅用于浏览。要将歌曲添加到播放列表中，这些歌曲必须先存在于你的音乐库中。请使用 Apple Music 应用程序将曲库中的歌曲添加到你的音乐库中，然后再使用 `clawtunes` 进行管理。

## 注意事项

- 仅适用于 macOS（使用 AppleScript 与 Apple Music 通信）。
- 如果系统请求自动化权限，请在“系统设置” > “隐私与安全” > “自动化”中授予相应权限。