---
name: plex
description: 控制 Plex 媒体服务器：浏览媒体库、搜索媒体文件、播放媒体内容以及管理播放设置。
homepage: https://plex.tv
metadata: {"clawdis":{"emoji":"🎬","requires":{"bins":["curl"],"env":["PLEX_TOKEN","PLEX_SERVER"]},"primaryEnv":"PLEX_TOKEN"}}
---

# Plex Media Server

使用 Plex API 来控制 Plex Media Server。

## 设置

配置环境变量：
- `PLEX_SERVER`：您的 Plex 服务器地址（例如：`http://192.168.1.100:32400`）
- `PLEX_TOKEN`：您的 Plex 认证令牌（可以在 plex.tv/claim 或 Plex 应用程序的 XML 文件中找到）

## 常用命令

### 获取服务器信息
```bash
curl -s "$PLEX_SERVER/?X-Plex-Token=$PLEX_TOKEN" -H "Accept: application/json"
```

### 浏览媒体库
```bash
curl -s "$PLEX_SERVER/library/sections?X-Plex-Token=$PLEX_TOKEN" -H "Accept: application/json"
```

### 列出媒体库内容
```bash
# Replace 1 with your library section key (from browse above)
curl -s "$PLEX_SERVER/library/sections/1/all?X-Plex-Token=$PLEX_TOKEN" -H "Accept: application/json"
```

### 搜索
```bash
curl -s "$PLEX_SERVER/search?query=SEARCH_TERM&X-Plex-Token=$PLEX_TOKEN" -H "Accept: application/json"
```

### 获取最近添加的媒体文件
```bash
curl -s "$PLEX_SERVER/library/recentlyAdded?X-Plex-Token=$PLEX_TOKEN" -H "Accept: application/json"
```

### 继续观看（Get On Deck）
```bash
curl -s "$PLEX_SERVER/library/onDeck?X-Plex-Token=$PLEX_TOKEN" -H "Accept: application/json"
```

### 查看当前正在播放的内容（Active Sessions）
```bash
curl -s "$PLEX_SERVER/status/sessions?X-Plex-Token=$PLEX_TOKEN" -H "Accept: application/json"
```

### 列出可用的客户端/播放器
```bash
curl -s "$PLEX_SERVER/clients?X-Plex-Token=$PLEX_TOKEN" -H "Accept: application/json"
```

## 媒体库类型

- 电影（通常为第 1 个分类）
- 电视节目（通常为第 2 个分类）
- 音乐
- 照片

## 注意事项

- 添加 `-H "Accept: application/json"` 以获取 JSON 格式的输出（默认为 XML 格式）
- 媒体库的分类键（1、2、3 等）可能因服务器设置而异——请先列出所有分类
- 媒体文件的路径格式为 `/library/metadata/12345`
- 在设备上开始播放前，请务必先确认相关信息
- 获取您的认证令牌：访问 plex.tv → 账户（Account）→ 授权设备（Authorized Devices）→ 查看 XML 链接