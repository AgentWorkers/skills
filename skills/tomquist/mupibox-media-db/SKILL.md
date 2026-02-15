---
name: mupibox-media-db
description: "通过 MuPiBox 后端 API 管理 MuPiBox 媒体数据库（data.json）：可以执行列表查询、添加记录、删除记录、移动记录、编辑记录字段以及恢复记录内容等操作。"
---
# MuPiBox 媒体数据库

通过后端 API 管理 MuPiBox 的媒体数据库（`data.json`）。

## 要求

- 需要访问正在运行的 MuPiBox 后端实例（MuPiBox 的主机地址通常为 `http://mupibox/`，本脚本的 API 默认地址为 `http://mupibox:8200`；可以通过 `--base-url` 参数进行覆盖）
- 需要 Python 3 环境
- 所需脚本位于 `./scripts/mupibox_media_manager.py` 文件中

## API 基础操作

- 读取数据：`GET /api/data`
- 添加数据：`POST /api/add`, `POST /api/edit`, `POST /api/delete`

## 示例命令

> 脚本路径：`./scripts/mupibox_media_manager.py`。默认 API 端点为 `http://mupibox:8200`（可以通过 `--base-url` 参数进行覆盖）。

```bash
# Show list
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> list --limit 30

# Filter (for example spotify + music)
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> list --type spotify --category music --limit 100

# Manual backup
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> backup
```

## 添加条目

```bash
# 1) Raw JSON
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> add \
  --json '{"type":"spotify","category":"audiobook","artist":"Example Artist","id":"SPOTIFY_ID"}'

# 2) Spotify URL with automatic ID extraction
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> add \
  --type spotify --category audiobook --artist "Example Artist" \
  --spotify-url "https://open.spotify.com/album/SPOTIFY_ID"
```

## 删除条目

```bash
# By index
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> remove --index 42

# By Spotify ID
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> remove --spotify-id SPOTIFY_ID
```

## 移动/重新排序条目

```bash
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> move --from 20 --to 3
```

## 更新条目字段

```bash
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> set --index 10 \
  --field artist="New Artist" \
  --field category="audiobook" \
  --field shuffle=true
```

`--field` 参数接受 JSON 格式的值（`true`, `false`, 数字, 字符串）。

## 恢复数据

```bash
python3 ./scripts/mupibox_media_manager.py --base-url <BASE_URL> restore \
  --file ~/.mupibox-db-backups/data-YYYYMMDD-HHMMSS-before-add.json
```

## 代理工作流程

1. 对于 `add` 操作：先解决缺失的 ID 或元数据问题，然后再进行添加。
2. 对于 `remove` 操作：先通过 `list` 操作找到对应的条目，然后再进行删除。
3. 对于 `move` 操作：先确认目标位置，然后再进行移动。
4. 使用 `list` 操作验证更改是否正确。

## 对 Spotify 有声书的质量要求

- 优先使用专辑 ID，而非播放列表 ID（除非明确请求使用播放列表 ID）。
- 当只需要一个官方发布的版本时，避免选择合集或精选集。
- 在存在多个版本的情况下，选择一致的版本。
- 如果不确定如何处理，请先请求澄清，而不是盲目添加数据。

## 安全性

- 不会对 MuPiBox API 之外产生任何外部副作用。
- 所需脚本会在执行修改操作前创建本地备份。
- 只能从可信的备份文件中恢复数据。
- 在操作失败时，会报告最新的备份文件信息。