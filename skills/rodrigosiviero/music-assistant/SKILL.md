---
name: music-assistant
description: >
  **Control Music Assistant (Home Assistant 音乐服务器)**  
  - 支持播放、调节音量、管理播放列表以及搜索音乐库功能。  
  - 用户可通过该工具播放/暂停音乐、跳过曲目、调整音量、搜索自己的音乐库、查看当前正在播放的内容、管理播放列表，或控制任何与 Music Assistant 集成的音乐播放器。  
  - 兼容 Spotify、Plex、本地文件以及其他与 Music Assistant 集成的音乐服务。
metadata:
  openclaw:
    requires:
      env:
        - MA_URL
        - MA_TOKEN
      env_optional:
        - MA_PLAYER
---
# 音乐助手

通过这个工具，您可以控制音乐助手服务器，实现音乐播放、队列管理和库浏览等功能。

## 设置

在使用此功能之前，您需要配置音乐助手的连接信息：

```bash
# 必需配置
export MA_URL="http://YOUR_SERVER_IP:8095/api"
export MA_TOKEN="YOUR_BEARER_TOKEN"

# 可选配置（未设置时系统会自动检测）
export MAPLAYER="your_player_id"
```

**获取您的访问令牌：**
1. 打开音乐助手的网页界面。
2. 进入“设置” → “安全”。
3. 创建或复制您的长期有效访问令牌（Long-Lived Access Token）。

**获取您的播放器 ID：**
```bash
./scripts/mactl.py players
```

## 快速入门

```bash
# 基本操作
./scripts/mactl.py play          # 播放/暂停
./scripts/mactl.py next          # 跳到下一首歌
./scripts/mactl.py volume 75     # 将音量设置为 75%
./scripts/mactl.py search "nirvana"    # 搜索并播放“Nirvana”乐队的相关歌曲
./scripts/mactl.py play-search "pink floyd"  # 搜索并播放“Pink Floyd”乐队的第一首匹配歌曲
./scripts/mactl.py status         # 查看当前正在播放的歌曲
./scripts/mactl.py queue          # 查看播放队列
```

## 播放控制

```bash
./scripts/mactl.py play          # 播放/暂停
./scripts/mactl.py pause         # 暂停播放
./scripts/mactl.py stop          # 停止播放
./scripts/mactl.py next          # 跳到下一首歌
./scripts/mactl.py prev          # 跳到上一首歌
```

## 音量控制

```bash
./scripts/mactl.py volume 75     # 将音量设置为 75%
./scripts/mactl.py mute          # 静音
./scripts/mactl.py unmute        # 取消静音
```

## 队列管理

```bash
./scripts/mactl.py shuffle true      # 启用随机播放模式
./scripts/mactl.py shuffle false     # 关闭随机播放模式
./scripts/mactl.py repeat all      # 设置重复播放模式（off/all/one）
./scripts/mactl.py clear         # 清空播放队列
./scripts/mactl.py queue-items     # 显示队列中的歌曲列表
```

## 搜索与播放

```bash
./scripts/mactl.py search "pink floyd"    # 搜索“Pink Floyd”乐队
./scripts/mactl.py search "nirvana" --type track   # 搜索“Nirvana”乐队的歌曲（按类型筛选）
./scripts/mactl.py search "metallica" --limit 5    # 搜索“Metallica”乐队并限制结果数量为 5
./scripts/mactl.py play-search "smells like teen spirit"  # 搜索并立即播放搜索结果中的第一首歌
./scripts/mactl.py ps "comfortably numb"   # 快速搜索“comfortably numb”这首歌
./scripts/mactl.py play-uri "spotify://track/4gHnSNHs8RyVukKoWdS99f"  # 通过 URI 播放歌曲
```

## 状态与信息

```bash
./scripts/mactl.py status         # 显示播放器状态及当前正在播放的歌曲
./scripts/mactl.py queue          # 查看播放队列
./scripts/mactl.py recent         # 显示最近播放过的歌曲
./scripts/mactl.py players        # 列出所有可用的播放器
```

## 图书库管理

```bash
./scripts/mactl.py sync          # 同步音乐库数据
```

**示例：**

- **播放 Nirvana 乐队的歌曲：**
  ```bash
  ./scripts/mactl.py play-search "nirvana"
  ```

- **查看当前正在播放的歌曲：**
  ```bash
  ./scripts/mactl.py status
  ```

- **跳过当前歌曲：**
  ```bash
  ./scripts/mactl.py next
  ```

- **将音量设置为 50%：**
  ```bash
  ./scripts/mactl.py volume 50
  ```

- **启用随机播放模式：**
  ```bash
  ./scripts/mactl.py shuffle true
  ```

## 直接使用 API

对于 CLI 未涵盖的操作，可以直接使用 JSON-RPC API：

```bash
curl -s "http://YOUR_SERVER:8095/api" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MA_TOKEN" \
  -d '{"message_id":"1","command":"playerqueues/all"}'
```

API 文档请访问：`http://YOUR_SERVER:8095/api-docs`

### 主要 API 命令

| 命令            | 参数            | 描述                                      |
|-----------------|-----------------|-------------------------------------------|
| players/all       |                | 列出所有播放器                                      |
| playerqueues/all    |                | 列出所有播放队列                                      |
| playerqueues/playPause  | queue_id         | 切换歌曲的播放/暂停状态                        |
| playerqueues/next     | queue_id         | 跳到下一首歌曲                                      |
| playerqueues/previous  | queue_id         | 跳到上一首歌曲                                      |
| playerqueues/stop     | queue_id         | 停止播放                                      |
| playerqueues/shuffle    | queue_id, shuffle_enabled | 启用/禁用随机播放模式                          |
| playerqueues/repeat    | queue_id, repeat_mode    | 设置重复播放模式（off/all/one）                        |
| playerqueues/clear    | queue_id         | 清空播放队列                                      |
| playerqueues/items    | queue_id, limit, offset    | 获取队列中的歌曲列表                              |
| playerqueues/playMedia   | queue_id, uri        | 通过 URI 播放歌曲                                      |
| music/search     | search, media_types, limit    | 搜索音乐库                                    |
| music/recently_played | limit           | 显示最近播放过的歌曲                              |
| music/sync       | media_types, providers    | 同步音乐库数据                                  |
| config/players/get    | player_id         | 获取播放器设置                                    |
```