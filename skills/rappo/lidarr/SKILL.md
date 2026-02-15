---
name: lidarr
version: 1.0.0
description: 在 Lidarr 中搜索并添加音乐。支持艺术家、专辑以及音乐质量设置（优先选择 FLAC 格式的音乐）。
metadata: {"openclaw":{"emoji":"🎵","requires":{"bins":["curl","jq"]}}}
---

# Lidarr

将音乐（艺术家和专辑）添加到您的 Lidarr 图书库中。

## 设置

创建 `~/.clawdbot/credentials/lidarr/config.json` 文件：
```json
{
  "url": "http://192.168.1.50:8686",
  "apiKey": "efbd6c29db184911a7b0f4707ae8f10f",
  "defaultQualityProfile": 2,
  "defaultMetadataProfile": 7
}
```

- `defaultQualityProfile`：音频质量配置文件 ID（FLAC、MP3 等 — 运行 `config` 命令查看可用选项）
- `defaultMetadataProfile`：元数据配置文件 ID（仅适用于专辑信息，如唱片目录等 — 运行 `config` 命令查看可用选项）

## 音频质量配置文件
通常推荐使用 FLAC 格式：
- 无损音频（FLAC）
- 24 位无损音频（FLAC 24-bit）

## 元数据配置文件
- **仅适用于专辑**（推荐） — 仅包含录音室专辑的信息
- 标准配置 — 包含专辑及其他相关信息
- 录片目录 / 全部内容 — 包含所有发布的音乐作品

## 工作流程

### 1. 搜索艺术家
```bash
bash scripts/lidarr.sh search "Artist Name"
```
返回包含 MusicBrainz 链接的编号列表。

### 2. 检查艺术家是否存在
```bash
bash scripts/lidarr.sh exists <foreignArtistId>
```

### 3. 添加艺术家
```bash
bash scripts/lidarr.sh add <foreignArtistId>
```
如果艺术家已经存在，系统将开始监控该艺术家的新作品，而不会报错。

**选项：**
- `--discography` — 添加该艺术家的全部唱片目录（而不仅仅是专辑）
- `--no-search` — 不立即执行搜索操作

### 4. 列出艺术家的专辑
```bash
bash scripts/lidarr.sh list-artist-albums <artistId>
```
显示该艺术家的所有专辑及其对应的 ID 和监控状态。

### 5. 监控特定专辑
```bash
bash scripts/lidarr.sh monitor-album <albumId>
```
监控并可选地搜索特定的专辑。

**选项：**
- `--no-search` — 仅进行监控，不执行搜索操作

## 命令

### 搜索艺术家
```bash
bash scripts/lidarr.sh search "KMFDM"
```

### 检查艺术家是否存在
```bash
bash scripts/lidarr.sh exists 45074d7c-5307-44a8-854f-ae072e1622ae
```

### 添加艺术家（默认情况下仅添加 FLAC 格式的专辑）
```bash
bash scripts/lidarr.sh add 45074d7c-5307-44a8-854f-ae072e1622ae
```

### 添加艺术家的全部唱片目录
```bash
bash scripts/lidarr.sh add 45074d7c-5307-44a8-854f-ae072e1622ae --discography
```

### 列出艺术家的专辑
```bash
bash scripts/lidarr.sh list-artist-albums 382
```

### 监控特定专辑
```bash
bash scripts/lidarr.sh monitor-album 11116
```

### 列出您的音乐库
```bash
bash scripts/lidarr.sh list
```

### 更新艺术家的元数据
```bash
bash scripts/lidarr.sh refresh <artistId>
```

### 删除艺术家
```bash
bash scripts/lidarr.sh remove <artistId>              # keep files
bash scripts/lidarr.sh remove <artistId> --delete-files  # delete files too
```

### 查看配置信息
```bash
bash scripts/lidarr.sh config
```