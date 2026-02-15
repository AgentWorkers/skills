---
name: sonoscli
description: 控制 Sonos 扬声器（包括发现设备、查看设备状态、播放音乐、调节音量以及分组管理等功能）。
homepage: https://sonoscli.sh
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["sonos"]},"install":[{"id":"go","kind":"go","module":"github.com/steipete/sonoscli/cmd/sonos@latest","bins":["sonos"],"label":"Install sonoscli (go)"}]}}
---

# Sonos CLI

使用 `sonos` 命令来控制本地网络中的 Sonos 音响设备。

**快速入门：**
- `sonos discover`：发现可用的 Sonos 音响设备
- `sonos status --name "Kitchen"`：查看指定设备（例如“Kitchen”）的状态
- `sonos play|pause|stop --name "Kitchen"`：播放、暂停或停止指定设备上的音乐
- `sonos volume set 15 --name "Kitchen"`：将指定设备（例如“Kitchen”）的音量设置为 15

**常见操作：**
- **设备分组：**
  - `sonos group status`：查看设备分组的状态
  - `sonos group join`：加入某个设备组
  - `sonos group unjoin`：退出某个设备组
  - `sonos group party`：将设备加入群组模式
  - `sonos group solo`：将设备设置为独立模式
- **收藏夹：**
  - `sonos favorites list`：查看收藏夹列表
  - `sonos favorites open`：播放收藏夹中的音乐
- **播放列表：**
  - `sonos queue list`：查看播放队列
  - `sonos queue play`：开始播放队列中的音乐
  - `sonos queue clear`：清空播放队列
- **Spotify 搜索（通过 SMAPI）：**
  - `sonos smapi search --service "Spotify" --category tracks "query"`：使用 SMAPI 在 Spotify 中搜索音乐

**注意事项：**
- 如果 SSDP 协议无法使用，请使用 `--ip <speaker-ip>` 参数指定设备的 IP 地址。
- Spotify Web API 搜索是可选的，需要提供 `SPOTIFY_CLIENT_ID` 和 `SPOTIFY_SECRET` 密钥。