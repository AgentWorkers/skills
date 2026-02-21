---
name: libby-book-monitor
version: 1.0.0
description: 在 Libby/OverDrive 图书馆中跟踪图书的可用性。您可以搜索图书馆目录、管理书单，并在图书添加时收到通知。相关命令包括：“libby”、“check libby”、“libby watchlist”、“is book on libby”、“book available”、“overdrive”、“library catalogue”、“ספרייה”、“ספרים”。
author: Alex Polonsky (https://github.com/alexpolonsky)
homepage: https://github.com/alexpolonsky/agent-skill-libby-book-monitor
metadata: {"openclaw": {"emoji": "📚", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# Libby/OverDrive 图书监控工具

该工具用于跟踪 Libby/OverDrive 图书库中的图书可用性。您可以搜索图书目录、管理书单，并在图书被添加到您的图书馆收藏时收到通知。

> **免责声明**：这是一个非官方工具，与 OverDrive/Libby 无关，也未获得其授权或支持。该工具使用的目录数据查询 API 可能无法准确反映图书的实际可用情况。该工具不提供借书或预约服务，按“原样”提供，不附带任何形式的保证。

## 快速入门

```bash
# Search a library catalogue
python3 {baseDir}/scripts/libby-book-monitor.py search telaviv "Project Hail Mary"

# Add a book to your watchlist
python3 {baseDir}/scripts/libby-book-monitor.py watch "Kafka on the Shore" --author "Haruki Murakami"

# Check your watchlist against the API
python3 {baseDir}/scripts/libby-book-monitor.py check

# Show your watchlist
python3 {baseDir}/scripts/libby-book-monitor.py list
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `search <图书馆> <查询>` | 按书名/作者搜索图书馆目录 |
| `watch <书名>` | 将图书添加到书单 |
| `unwatch <书名>` | 从书单中移除图书 |
| `list` | 显示书单及其状态 |
| `check` | 根据 API 检查书单中的所有图书 |

## 选项

| 选项 | 命令 | 描述 |
|--------|----------|-------------|
| `--profile <用户名>` | all | 为不同用户维护独立的书单 |
| `--author <作者>` | watch | 指定图书作者 |
| `--library <图书馆代码>` | watch | 图书馆代码（默认值：从配置文件中获取） |
| `--notify` | check | 仅打印新发现的图书（适用于定时任务） |
| `--data-dir <路径>` | all | 自定义数据目录 |

## 用户配置

使用 `--profile` 为不同用户创建独立的书单：

```bash
python3 {baseDir}/scripts/libby-book-monitor.py --profile jane watch "Dune"
python3 {baseDir}/scripts/libby-book-monitor.py --profile bob check --notify
```

## 配置

默认使用的图书馆是以色列数字图书馆（`telaviv`）。请编辑 `~/.libby-book-monitor/config.json` 文件进行配置：

```json
{
  "default_library": "nypl",
  "libraries": {
    "nypl": "New York Public Library"
  }
}
```

“图书馆代码”是指您图书馆在 OverDrive 网站上的子域名（例如：`nypl.overdrive.com` → `nypl`）。

## 定时任务集成

设置每日检查任务，仅在发现新图书时输出结果：

```bash
python3 {baseDir}/scripts/libby-book-monitor.py --profile jane check --notify
```

如果发现新图书，会将结果发送给用户。

## 注意事项

- 该工具支持非拉丁字母字符集（如希伯来文、阿拉伯文、中文等）。
- 当 API 响应中 `isOwned` 的值为 `true` 时，表示图书已被添加到您的图书馆收藏。
- 在同时检查多本书时，每次 API 调用之间会有 1 秒的延迟。
- 该工具不依赖任何外部库，仅使用 Python 标准库。
- 数据存储在 `~/.libby-book-monitor/` 目录中（可通过 `--data-dir` 或 `$LIBBY_BOOK_MONITOR_DATA` 参数进行配置）。