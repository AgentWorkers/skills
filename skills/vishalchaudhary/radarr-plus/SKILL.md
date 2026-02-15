---
name: radarr
description: 通过 Radarr 的 HTTP API 添加和管理电影：支持搜索/查找电影、列出电影的质量信息及存储文件夹信息、根据电影标题/年份或 TMDB ID 添加新电影，以及触发搜索操作。该功能适用于用户通过 Radarr/Plex 添加/请求/下载电影的场景，也可用于自动化基于 Radarr 的媒体处理流程。
---

# Radarr+

您可以通过聊天请求电影，并将这些电影添加到 **Radarr** 中（同时会在同一聊天窗口中显示进度更新）。

## 功能演示（示例）

以下是用户请求电影时收到的信息示例（包含电影海报、预告片和评分）：

![示例电影海报](https://image.tmdb.org/t/p/w185/nrmXQ0zcZUL8jFLrakWc90IR8z9.jpg)

示例信息内容：

> **《肖申克的救赎》（2010年）**
>
> ⭐ IMDb评分：8.2/10
>
> 🎬 预告片：https://www.youtube.com/watch?v=qdPw9x9h5CY
>
> 已添加到 Radarr ✅（格式：Ultra-HD，分类：/movies）。我会在这里更新进度并显示“已导入 ✅”。

## 设置（只需执行一次）

1) 在 `~/.openclaw/.env` 文件中设置以下环境变量（请勿将这些变量提交到代码仓库）：
- `RADARR_URL=http://<host>:7878`
- `RADARR_API_KEY=...`

**推荐设置（可减少后续问题）：**
- `RADARR_DEFAULT_PROFILE=HD-1080p`
- `RADARR_DEFAULT_ROOT=/data/media/movies`

**进阶设置（用于更丰富的功能）：**
- `TMDB_API_KEY=...`（用于获取电影海报和预告片）
- `OMDB_API_KEY=...`（用于获取 IMDb 评分）
- `PLEX_URL=http://<plex-host>:32400`
- `PLEX_TOKEN=...`

2) 验证环境变量和连接是否正常：

```bash
./skills/radarr/scripts/check_env.py
./skills/radarr/scripts/radarr.sh ping
```

如果出现错误，请检查：
- 是否可以从 OpenClaw 主机访问 Radarr
- API 密钥是否正确
- 网址（http 或 https）是否正确

## 常见操作

### 列出可用的电影质量设置

```bash
./skills/radarr/scripts/radarr.sh profiles
```

### 查看已配置的文件存储目录

```bash
./skills/radarr/scripts/radarr.sh roots
```

### 查找/搜索电影

```bash
./skills/radarr/scripts/radarr.sh lookup --compact "inception"
./skills/radarr/scripts/radarr.sh lookup --compact "tmdb:603"
```

### 添加电影（推荐使用 TMDB ID）

```bash
./skills/radarr/scripts/radarr.sh add --tmdb 603 --profile "HD-1080p" --root "/data/media/movies" --monitor --search
```

### 添加电影（按标题；可选：按年份筛选）

```bash
./skills/radarr/scripts/radarr.sh add --term "Dune" --year 2021 --profile "HD-1080p" --root "/data/media/movies" --monitor --search
```

## 聊天操作流程（推荐）

当用户发送“请求/添加 <电影名>”（无论是私信还是群组消息）时，按照以下步骤操作：

### 1) 查找电影信息
运行以下命令：
- `./skills/radarr/scripts/radarr.sh lookup --compact "<电影名>"`

如果找到多个匹配结果，请让用户选择具体的电影（可以通过年份或 TMDB ID 来确定）。

### 2) 从环境变量中获取缺失的配置信息
如果某些配置信息缺失，系统会从环境变量中读取默认值，并提示用户进行选择：
- `options.profiles[]`
- `options.roots[]`

（如果默认值存在，系统会直接使用这些值。）

### 3) 可选的高级功能：生成电影卡片
如果设置了 `TMDB_API_KEY`，系统会生成电影卡片：
```bash
./skills/radarr/scripts/movie_card.py --tmdb <id>
```

- 如果输出中包含 `posterUrl`，您可以下载该海报并将其附加到消息中：

```bash
./skills/radarr/scripts/fetch_asset.py --url "<posterUrl>" --out "./outbound/radarr/<tmdbId>.jpg"
```

如果设置了 `OMDB_API_KEY` 并且已知电影的 IMDb ID，卡片上还会显示 IMDb 评分。

### 4) 将电影添加到 Radarr
尽可能使用 TMDB 的数据来添加电影：

```bash
./skills/radarr/scripts/radarr.sh add --tmdb <id> --profile "<profile>" --root "<root>" --monitor --search
```

### 5) 在同一聊天窗口中跟踪进度并通知用户
该功能会为请求来源的聊天窗口（私信或群组）创建一个进度跟踪队列：

```bash
./skills/radarr/scripts/enqueue_track.py --channel telegram --target "<chatId>" --movie-id <id> --title "<title>" --year <year>
```

### 6) 定期更新进度
系统会定期执行进度更新：
```bash
./skills/radarr/scripts/poll_and_queue.py
```

更新后的进度信息会保存在 `./state/radarr/outbox/` 目录下，OpenClaw 的定时任务脚本可以自动发送这些信息。

### 7) 提供 Plex 链接（可选功能）
如果配置了 Plex，系统会尝试生成对应的 Plex 链接：
```bash
./skills/radarr/scripts/plex_link.py --title "<title>" --year <year>
```

## 参考资料
- 入门指南：`references/onboarding.md`
- 设置指南：`references/setup.md`
- API 使用说明：`references/radarr-api-notes.md`